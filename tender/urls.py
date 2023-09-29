from django.urls import path, include
from .views import *
from .models import (ProjectSiteEngineer, RetensionMoney, SecurityMoney, TenderPg, CostMainHead, CostSubHead, DailyExpendiature, BankInformation)
from .forms import (SiteEngineerForm, BankInformationForm, SecurityMoneyForm, TenderPgForm,
                    get_form, get_cost_head_form)
from .engineer import urls as engineer_urls
from .expenditure import urls as expenditure_urls
urlpatterns = [
    path("engineers/", include(engineer_urls)),
    path("expendature/", include(expenditure_urls)),
    path('site-engineer-create/', TenderProjectCreateView.as_view(
    title = 'Site Engineer Create Form',
    model = ProjectSiteEngineer,
    form_class = SiteEngineerForm,
    success_url = "site_engineer_list",
    ), name='site_engineer_create'),
    path('site-engineer-update/<int:pk>', TenderProjectUpdateView.as_view(
    form_class = SiteEngineerForm,
    model = ProjectSiteEngineer,
    success_url = "site_engineer_list",
    ), name='site_engineer_update'),
    path('site-engineer-list/', TenderProjectListView.as_view(
    title = 'All Site Engineer List',
    model = ProjectSiteEngineer,
    queryset = ProjectSiteEngineer.objects.all(),
    search_fields = ['user',],
    list_display = ['user', 'balance'],
    url_list = ['site_engineer_update', 'site_engineer_delete', 'site_engineer_details'],
    ), name='site_engineer_list'),
    path('site-engineer-details/<int:pk>', TenderProjectDetailView.as_view(
    model = ProjectSiteEngineer,
    title = "Project Site Engineer details"
    ), name='site_engineer_details'),
    path('site-engineer-delete/<int:pk>', TenderProjectDeleteView.as_view(
    model = ProjectSiteEngineer,
    success_url = 'site_engineer_list',
    ), name='site_engineer_delete'),
    
    # --- Tender Project Urls ---
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
    form_class = SecurityMoneyForm,
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
    form_class = SecurityMoneyForm,
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
    form_class = TenderPgForm,
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
    form_class = TenderPgForm,
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

    # --- COST MAIN HEAD Urls ---
    path('cost-main-head-create/', MainHeadCreateView.as_view(
    title = 'Cost Main Head Create Form',
    form_class = get_cost_head_form(CostMainHead),
    model = CostMainHead,
    success_url = 'main_head_list',
    ), name='main_head_create'),
    
    path('cost-main-head-update/<int:pk>', CostHeadUpdateView.as_view(
    title = 'Cost Main Head Update Form',
    form_class = get_cost_head_form(CostMainHead),
    model = CostMainHead,
    success_url = 'main_head_list',
    ), name='main_head_update'),
    
    path('cost-main-head-list/', TenderProjectListView.as_view(
    model = CostMainHead,
    queryset = CostMainHead.objects.all(),
    search_fields = ['name',],
    list_display = ['name', 'balance'],
    url_list = ['main_head_update', 'main_headt_delete', 'main_head_details'],
    title = 'Cost Main Head List',
    ), name='main_head_list'),

    path('cost-main-head-details/<int:pk>', TenderProjectDetailView.as_view(
    model = CostMainHead,
    title = "Cost Main Head details"
    ), name='main_head_details'),

    path('cost-main-head-delete/<int:pk>', TenderProjectDeleteView.as_view(
    model = CostMainHead,
    success_url = 'main_head_list',
    ), name='main_headt_delete'),

    # -- COST SUB-HEAD URLS --
    path('cost-sub-head-create/', MainHeadCreateView.as_view(
    title = 'Cost Sub Head Create Form',
    form_class = get_cost_head_form(CostSubHead),
    model = CostSubHead,
    success_url = 'sub_head_list',
    ), name='sub_head_create'),

    path('cost-sub-head-update/<int:pk>', CostHeadUpdateView.as_view(
    title = 'Cost Sub Head Update Form',
    form_class = get_cost_head_form(CostSubHead),
    model = CostSubHead,
    success_url = 'sub_head_list',
    ), name='sub_head_update'),

    path('cost-sub-head-list/', TenderProjectListView.as_view(
    model = CostSubHead,
    queryset = CostSubHead.objects.all(),
    search_fields = ['name',],
    list_display = ['name', 'balance'],
    url_list = ['sub_head_update', 'sub_headt_delete', 'sub_head_details'],
    title = 'Cost Sub Head List',
    ), name='sub_head_list'),

    path('cost-sub-head-details/<int:pk>', TenderProjectDetailView.as_view(
    model = CostSubHead,
    title = "Cost Sub Head details"
    ), name='sub_head_details'),
    path('cost-sub-head-delete/<int:pk>', TenderProjectDeleteView.as_view(
    model = CostSubHead,
    success_url = 'sub_head_list',
    ), name='sub_headt_delete'),

    # -- BANK INFORMATION URLS -- 
    path('bank-info-create/', TenderProjectCreateView.as_view(
    title = 'Bank Information Create Form',
    model = BankInformation,
    form_class = BankInformationForm,
    success_url = "bank_info_list",
    ), name='bank_info_create'),    
    
    path('bank-info-list/', TenderProjectListView.as_view(
    model = BankInformation,
    queryset = BankInformation.objects.all(),
    search_fields = ['account_no', 'bank_name'],
    list_display = ['account_no', 'bank_name', 'branch_name', 'balance'],
    url_list = ['bank_info_update', 'bank_info_delete', 'bank_info_details'],
    title = 'Bank Information List',
    ), name='bank_info_list'),
    
    path('bank-info-update/<int:pk>', TenderProjectUpdateView.as_view(
    form_class = BankInformationForm,
    model = BankInformation,
    success_url = "bank_info_list",
    ), name='bank_info_update'),
    
    path('bank-info-details/<int:pk>', TenderProjectDetailView.as_view(
    model = BankInformation,
    title = "Bank Information details"
    ), name='bank_info_details'),
    
    path('bank-info-delete/<int:pk>', TenderProjectDeleteView.as_view(
    model = BankInformation,
    success_url = 'bank_info_list',
    ), name='bank_info_delete'),

    # Make pdf urls
    path('make-pdf/', render_pdf_view, name='generate_pdf'),
]