from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',BillReceivedDashboardView.as_view(),name='received_dashboard'),
    
    path('all-bill-receive/',BillReceivedCreateView.as_view(),name='all_bill_receive'),
    path('list/',MoneyReceivedListView.as_view(),name='all_received_list'),
    path('details/<int:pk>',MoneyReceivedDetailView.as_view(),name='received_details'),

    path('security-money/',SecurityMoneyReceivedCreateView.as_view(),name='received_security_money_create'),
    path('performance-guarantee/',PgReceivedCreateView.as_view(),name='received_pg_create'),
    
    path('loan-collection-list/',LoanCollectionListView.as_view(),name='loan_collection_list'),
    path('loan-collection/',LoanCollectionCreateView.as_view(),name='collection_loan_create'),
    path('loan-received/',LoanReceivedCreateView.as_view(),name='received_loan_create'),
    path('loan-received-list/',LoanReceivedListView.as_view(),name='loan_received_list'),
]