from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from users_app.models.managers import UserManager


class User(AbstractUser):

    class Types(models.TextChoices):
        CONTRACT_BASED = "CONTRACT BASED", "contract based"
        FULL_TIME = "FULL_TIME", "full time"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    employee_type =  models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.FULL_TIME
    )
    role_designation = models.CharField(max_length=100)
    onboarding_date = models.DateTimeField(null=True)
    issue_laptop = models.BooleanField(default=False)
    timesheets_access = models.BooleanField(default=False)
    resigned = models.BooleanField(default=False)
    relieving_date = models.DateTimeField(null=True)

    # values to satisfy djangos User model constraints
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=40, unique=False, default='')
    REQUIRED_FIELDS = []

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email



class ContractUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CONTRACT_BASED)

class CONTRACT_BASED(User):
    employee_type = User.Types.CONTRACT_BASED
    timesheets_access = True
    objects = ContractUserManager()

    class Meta:
        proxy = True



class FullTimeUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.FULL_TIME)

class FULL_TIME(User):
    employee_type = User.Types.FULL_TIME
    timesheets_access = False
    objects = FullTimeUserManager()

    class Meta:
        proxy = True









    



