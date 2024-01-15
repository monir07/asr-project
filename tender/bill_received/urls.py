from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',BillReceivedDashboardView.as_view(),name='received_dashboard'),
]