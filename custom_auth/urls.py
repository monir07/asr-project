from django.urls import path, include
from .views import *

urlpatterns = [
    path('user-list/', UserListView.as_view(), name='all_user_list'),
    path('', index, name='index'),
]