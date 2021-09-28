from django.urls import path

from users_app.api.views import (CreateUserView, AddUserGroupView, ListGroupUserView, 
CustomerView, ProjectView, UserToProjectView, TimesheetsView, SkillTrackingView, TimesheetsDetailView,
SkillTrackingDetailView, DocumentView, DocumentDetailView, MyDocumentView)


urlpatterns = [
    # User urls 
    path('create-user/', CreateUserView.as_view(), name='create_user'),

    # Group urls 
    path('add-user-to-group/', AddUserGroupView.as_view(), name='add_user_to_group'),
    path('list-group-users/<str:pk>/', ListGroupUserView.as_view(), name='list_group_users'),

    # customer urls
    path('create-customer/', CustomerView.as_view(), name='create_customer'),
    path('create-project/', ProjectView.as_view(), name='create_project'),
    path('add-user-to-project/', UserToProjectView.as_view(), name='add_user_to_project'),

    #timesheets urls
    path('timesheets/', TimesheetsView.as_view(), name='create_timesheets'),
    path('timesheets/<int:pk>/', TimesheetsDetailView.as_view(), name='timesheet_detail'),

    #skill tracking urls
    path('skill-set/', SkillTrackingView.as_view(), name='add_skills'),
    path('skill-set/<int:pk>/', SkillTrackingDetailView.as_view(), name='skill_detail'),

    #Document urls
    path('document/', DocumentView.as_view(), name='upload_document'),
    path('document/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('my-document/', MyDocumentView.as_view(), name='my_document'),
]
