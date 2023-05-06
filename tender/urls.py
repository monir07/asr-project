from django.urls import path, include
from .views import *
from .models import (TenderProject, RetensionMoney, SecurityMoney, TenderPg, CostMainHead, CostSubHead, DailyExpendiature)
from .forms import (TenderProjectForm, get_form, MainHeadForm, SubHeadForm)

urlpatterns = [
    path('project-create/', TenderProjectCreateView.as_view(), name='tender_project_create'),
    path('project-update/<int:pk>', TenderProjectUpdateView.as_view(), name='tender_project_update'),
    path('project-list/', TenderProjectListView.as_view(), name='tender_project_list'),
    path('project-details/<int:pk>', TenderProjectDetailView.as_view(), name='tender_project_details'),
    path('project-delete/<int:pk>', TenderProjectDeleteView.as_view(), name='tender_project_delete'),

    # ----Retension Money----
    path('retension-create/', TenderProjectCreateView.as_view(
    title = 'Retension Money Create Form',
    model = RetensionMoney,
    form_class = get_form(RetensionMoney),
    success_url = "retension_list",
    ), name='retension_create'),    
    
    path('retension-list/', TenderProjectListView.as_view(
    model = RetensionMoney,
    queryset = RetensionMoney.objects.all(),
    search_fields = ['tender__project_name',],
    list_display = ['tender', 'amount', 'is_withdraw', 'maturity_date', 'remarks'],
    url_list = ['retension_update', 'retension_delete', 'retension_details'],
    title = 'Retension Money List',
    ), name='retension_list'),
    
    path('retension-update/<int:pk>', TenderProjectUpdateView.as_view(
    form_class = get_form(RetensionMoney),
    model = RetensionMoney,
    success_url = "retension_list",
    ), name='retension_update'),
    
    path('retension-details/<int:pk>', TenderProjectDetailView.as_view(
    model = RetensionMoney,
    title = "Retension Money details"
    ), name='retension_details'),
    
    path('retension-delete/<int:pk>', TenderProjectDeleteView.as_view(
    model = RetensionMoney,
    success_url = 'retension_list',
    ), name='retension_delete'),

    # ----Tender Security----
    path('security-money-create/', TenderProjectCreateView.as_view(
    title = 'Security Money Create Form',
    model = SecurityMoney,
    form_class = get_form(SecurityMoney),
    success_url = "security_money_list",
    ), name='security_money_create'),    
    
    path('security-money-list/', TenderProjectListView.as_view(
    model = SecurityMoney,
    queryset = SecurityMoney.objects.all(),
    search_fields = ['tender__project_name',],
    list_display = ['tender', 'amount', 'is_withdraw', 'maturity_date', 'remarks'],
    url_list = ['security_money_update', 'security_money_delete', 'security_money_details'],
    title = 'Security Money List',
    ), name='security_money_list'),
    
    path('security-money-update/<int:pk>', TenderProjectUpdateView.as_view(
    title = 'Tender Security Money Update Form',
    form_class = get_form(SecurityMoney),
    model = SecurityMoney,
    success_url = "security_money_list",
    ), name='security_money_update'),
    
    path('security-money-details/<int:pk>', TenderProjectDetailView.as_view(
    model = SecurityMoney,
    title = "Security Money details"
    ), name='security_money_details'),
    
    path('security-money-delete/<int:pk>', TenderProjectDeleteView.as_view(
    model = SecurityMoney,
    success_url = 'security_money_list',
    ), name='security_money_delete'),

    # ----Tender PG----
    path('pg-create/', TenderProjectCreateView.as_view(
    title = 'PG(Performance Gurranty) Create Form',
    model = TenderPg,
    form_class = get_form(TenderPg),
    success_url = "pg_list",
    ), name='pg_create'),    
    
    path('pg-list/', TenderProjectListView.as_view(
    model = TenderPg,
    queryset = TenderPg.objects.all(),
    search_fields = ['tender__project_name',],
    list_display = ['tender', 'amount', 'is_withdraw', 'maturity_date', 'remarks'],
    url_list = ['pg_update', 'pg_delete', 'pg_details'],
    title = 'Performance Gurranty List',
    ), name='pg_list'),
    
    path('pg-update/<int:pk>', TenderProjectUpdateView.as_view(
    title = 'Performance Gurranty Update Form',
    form_class = get_form(TenderPg),
    model = TenderPg,
    success_url = "pg_list",
    ), name='pg_update'),
    
    path('pg-details/<int:pk>', TenderProjectDetailView.as_view(
    model = TenderPg,
    title = "Performance Gurranty details"
    ), name='pg_details'),
    
    path('pg-delete/<int:pk>', TenderProjectDeleteView.as_view(
    model = TenderPg,
    success_url = 'pg_list',
    ), name='pg_delete'),
]