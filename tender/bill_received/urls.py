from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',BillReceivedDashboardView.as_view(),name='received_dashboard'),
    
    path('all-bill-receive/',BillReceivedCreateView.as_view(),name='all_bill_receive'),
    path('security-money/',SecurityMoneyReceivedCreateView.as_view(),name='received_security_money_create'),
    path('performance-guarantee/',PgReceivedCreateView.as_view(),name='received_pg_create'),
    path('loan/',LoanReceivedCreateView.as_view(),name='received_loan_create'),
]