from django.urls import path
from .views import SiteEngineerCreateView
from .forms import (SiteEngineerForm, UserRegisterForm)
urlpatterns = [
    # path('project-create/', TenderProjectCreateView.as_view(), name='tender_project_create'),
    path('create/', SiteEngineerCreateView.as_view(),
        name='create_new_user'),
]