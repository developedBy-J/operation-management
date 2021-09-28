from django.db import models
from users_app.models.models_user import User


class Timesheet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    billable_hours = models.IntegerField()
    invoice_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    timesheets = models.FileField(upload_to='timesheets/')

    def __str__(self):
        return f"{self.user_id.email} | {self.start_date} | {self.end_date} "



class SkillTracking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    experience = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id.email} | {self.skill}"