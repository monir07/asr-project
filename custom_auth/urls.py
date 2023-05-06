from django.urls import path, include
from .views import *

urlpatterns = [
    # path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('', index, name='index'),
]