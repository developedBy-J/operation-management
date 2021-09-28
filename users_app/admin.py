from django.contrib import admin
from users_app.models.models_user import User
from users_app.models.models_project import Customer, Project, ProjectResource
from users_app.models.models_documents import DocumentClassification, DocumentType, Document
from users_app.models.models_misc import Timesheet, SkillTracking


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Project)
admin.site.register(ProjectResource)
admin.site.register(DocumentClassification)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(Timesheet)
admin.site.register(SkillTracking)