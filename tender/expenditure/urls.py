from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',ExpendatureDashboardView.as_view(),name='expenditure_dashboard'),
    path('form-create/',ExpenditureCreateView.as_view(),name='expenditure_form_create'),
    path('form-update/<int:pk>',ExpenditureUpdateView.as_view(),name='expenditure_form_update'),
    path('list/',ExpenditureListView.as_view(),name='expenditure_list'),
    path('delete/<int:pk>',ExpenditureDeleteView.as_view(),name='expenditure_delete'),
    path('details/<int:pk>',ExpenditureDetailView.as_view(),name='expenditure_details'),
    
    # -- SECURITY URLS -- 
    path('security-money/',TenderSecurityCreateView.as_view(),name='expendature_security_money'),
    # -- PG URLS -- 
    path('performance-gurantee/',TenderPgCreateView.as_view(),name='expendature_pg'),
    # -- LOAN PAYS URLS -- 
    path('loan-pay/', LoanPayCreateView.as_view(), name='expendature_loan_pay'),
]
