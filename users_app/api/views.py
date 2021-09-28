from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users_app.api.serializers import (UserSerializer, GroupSerializer, CustomerSerializer, ProjectSerializer, 
                                        ProjectResourceSerializer, TimesheetSerializer, SkillTackingSerializer, 
                                        DocumentSerializer)
from users_app.models.models_project import Customer, Project, ProjectResource
from users_app.models.models_misc import Timesheet, SkillTracking
from users_app.models.models_documents import Document


UserModel = get_user_model()


class CreateUserView(CreateAPIView):
    """
    Create a new user.
    TBD : only users from selected groups can create users. 
    required_groups = {
         'POST': ['HR', 'CTO'],
     }
    """

    model = UserModel
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class AddUserGroupView(CreateAPIView):
    """
    Assign a user to a specific group
    """
    model = Group
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = GroupSerializer


class ListGroupUserView(ListAPIView):
    """
    List all the users under a specific group
    """
    model = UserModel
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.filter(groups__name=self.kwargs['pk'])


class CustomerView(ListCreateAPIView):
    """
    Create a new customer.
    List all the exsiting customers
    """
    queryset         = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]


class ProjectView(ListCreateAPIView):
    """
    Create a new project.
    List all the exsiting projects
    """
    queryset         = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]


class UserToProjectView(ListCreateAPIView):
    """
    Add an existing user to an existing project.
    """
    queryset         = ProjectResource.objects.all()
    serializer_class = ProjectResourceSerializer
    permission_classes = [permissions.AllowAny]


class TimesheetsView(ListCreateAPIView):
    """
    Add a timesheet for a period of time
    """
    queryset         = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [permissions.AllowAny]


class TimesheetsDetailView(RetrieveUpdateDestroyAPIView):
    """
    get or update or delete a particular timesheet 
    """
    queryset         = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [permissions.AllowAny]


class SkillTrackingView(ListCreateAPIView):
    """
    Add a skill for a specific user
    """
    queryset         = SkillTracking.objects.all()
    serializer_class = SkillTackingSerializer
    permission_classes = [permissions.AllowAny]


class SkillTrackingDetailView(RetrieveUpdateDestroyAPIView):
    """
    get or update or delete a particular skill for an user
    """
    queryset         = SkillTracking.objects.all()
    serializer_class = SkillTackingSerializer
    permission_classes = [permissions.AllowAny]


class DocumentView(ListCreateAPIView):
    """
    Add a document for a specific user
    """
    queryset         = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]


class DocumentDetailView(RetrieveUpdateDestroyAPIView):
    """
    get or update or delete a particular document of an user
    """
    queryset         = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]


class MyDocumentView(ListAPIView):
    """
    View all my documents
    """
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(user_id=user)