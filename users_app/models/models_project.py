from django.db import models
from users_app.models.models_user import User


# Managers

class ProjectResourceManager(models.Manager):
    def allocate_project_resource(self, project_name, email, poc):
        project = Project.objects.get(project_name=project_name)
        user = User.objects.get(email=email)
        if ProjectResource.objects.filter(project_id=project, user_id=user).exists():
            return {}
        project = ProjectResource.objects.create(project_id=project, user_id=user, point_of_contact=poc)
        return project


# Models 

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    poc_email = models.EmailField(max_length=100)
    contact_number = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    GST = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    MSA = models.FileField(upload_to='customer/')

    def __str__(self):
        return self.customer_name



class Project(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return self.customer_id.customer_name

    def __str__(self):
        return self.project_name



class ProjectResource(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    point_of_contact = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectResourceManager()

    @property
    def project_name(self):
        return self.project_id.project_name

    @property
    def user_email(self):
        return self.user_id.email

    def __str__(self):
        return f" {self.project_name} {self.user_email}"