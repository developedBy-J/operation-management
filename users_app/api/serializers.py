from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users_app.models.models_project import Customer, Project, ProjectResource
from users_app.models.models_misc import Timesheet, SkillTracking
from users_app.models.models_documents import Document

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'role_designation', 'employee_type')
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            role_designation = validated_data['role_designation'],
            employee_type = UserModel.Types.FULL_TIME if validated_data['employee_type'] in ["FULL_TIME", "full time"] else UserModel.Types.CONTRACT_BASED
        )
        user.save()

        return user



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'user_email')
        extra_kwargs = {
            'name': {'validators': [], 'write_only': True},
            'user_email': {'write_only': True},
        }

    user_email = serializers.CharField(write_only=True)

    def validate(self, data):
        if not Group.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Group not found")

        if not UserModel.objects.filter(email=data['user_email']).exists():
            raise serializers.ValidationError("Email not found")

        return data

    def create(self, validated_data):

        group = Group.objects.get(name=validated_data['name'])
        user = UserModel.objects.get(email=validated_data['user_email'])

        user.groups.add(group)

        return {}



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('id', 'created_at', 'updated_at', )



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('project_name', 'customer', 'customer_name')


    customer = serializers.CharField(write_only=True)
    customer_name = serializers.ReadOnlyField()

    def validate_customer(self, value):
        # check if customer name is valid
        if not Customer.objects.filter(customer_name=value).exists():
            raise serializers.ValidationError("Customer not found")
        return value

    def create(self, validated_data):

        customer = Customer.objects.get(customer_name=validated_data['customer'])
        project = Project.objects.create(customer_id=customer, project_name=validated_data['project_name'])

        return project


class ResourceSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField()
    class Meta:
        model = ProjectResource
        fields = ('user_email', )


class ProjectResourceSerializer(serializers.ModelSerializer):
    user_email_id = serializers.CharField(write_only=True)
    project = serializers.CharField(write_only=True)
    project_name = serializers.ReadOnlyField()
    resource_allocated =  serializers.SerializerMethodField()

    class Meta:
        model = ProjectResource
        fields = ('project_name', 'project', 'user_email_id', 'point_of_contact', 'resource_allocated')

    # Get the list of users working in the specified project
    def get_resource_allocated(self, obj):
        resources = ProjectResource.objects.filter(project_id=obj.project_id)
        return ResourceSerializer(resources, many=True).data

    # Check if project name is valid
    def validate_project(self, value):
        if not Project.objects.filter(project_name=value).exists():
            raise serializers.ValidationError("Project not found")
        return value

    # check if user email exists
    def validate_user_email(self, value):
        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found")
        return value

    def create(self, validated_data):

        project_resource = ProjectResource.objects.allocate_project_resource(validated_data['project'], 
                                validated_data['user_email_id'], validated_data['point_of_contact'])

        if not len(project_resource):
            raise serializers.ValidationError("User is already a project member")

        return project_resource



class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = ('id', 'start_date', 'end_date', 'billable_hours', 'invoice_sent', 'timesheets', 'email', 'user_id')
        read_only_fields = ('user_id', 'id')

    email = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date cannot be greater than end date")

        return data

    def create(self, validated_data):

        user = UserModel.objects.get(email=validated_data['email'])

        validated_data.pop('email')
        validated_data['user_id'] = user

        timesheet = Timesheet.objects.create(**validated_data)

        return timesheet



class SkillTackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTracking
        fields = ('id', 'skill', 'experience', 'email', 'user_id')
        read_only_fields = ('user_id', 'id')

    email = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.get(email=validated_data['email'])

        validated_data.pop('email')
        validated_data['user_id'] = user

        skill = SkillTracking.objects.create(**validated_data)

        return skill



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'user_id', 'document_type_id', 'document_name', 'email', 'document', )

    email = serializers.SerializerMethodField('get_email')

    def get_email(self, obj):
        return obj.user_id.email
        