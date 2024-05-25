import datetime
from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader
from django.http import HttpResponse
from ..models import (DailyExpendiature, TenderPg, SecurityMoney, 
                      LoanInformation, CashBalance, PaidMethodOption)
from .forms import *
from ..forms import (SecurityMoneyForm, TenderPgForm)
from asr.utility import format_search_string, get_fields


class ExpendatureDashboardView(generic.TemplateView):
    title = 'Expendature Dashboard'
    template_name="tender/expendature/dashboard.html"
    url_list = {
                'url_1':['expenditure_form_create', 'Daily Expendature', 'fa fa-caret-square-o-right'],
                'url_2':['expendature_security_money', 'Tender Security', 'fa fa-comments-o'],
                'url_3':['expendature_pg', 'Tender PG', 'fa fa-sort-amount-desc'],
                'url_4':['expendature_loan_pay', 'Loan Pay', 'fa fa-check-square-o'],
                'url_5':['expenditure_list', 'Expendature List', 'fa fa-list'],
            }

    def get_context_data(self, **kwargs):
        kwargs['url_list'] = self.url_list
        kwargs['title'] = self.title
        return super().get_context_data(**kwargs)
    

class ExpenditureCreateView(generic.CreateView):
    model = DailyExpendiature
    form_class = ProjectExpendiatureForm
    template_name = 'tender/expendature/form.html'
    success_message = "Created Successfully."
    title = 'New Expenditure Form'
    success_url = "expenditure_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        bank_obj = form.cleaned_data['bank_info']
        cash_obj = form.cleaned_data['cash_balance']
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
        
        if bank_obj:
            bank_obj.balance -= form.cleaned_data['paid_amount']
            bank_obj.updated_by = self.request.user
            bank_obj.save()
        
        if cash_obj:
            cash_obj.balance -= form.cleaned_data['paid_amount']
            cash_obj.updated_by = self.request.user
            cash_obj.save()

        messages.success(self.request, self.success_message)
        return self.get_success_url()

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ExpenditureUpdateView(generic.UpdateView):
    model = DailyExpendiature
    form_class = ProjectExpendiatureForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Created Successfully."
    title = 'Expenditure Update Form'
    success_url = "expenditure_list"
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.updated_by = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ExpenditureListView(generic.ListView):
    title = 'Daily Expenditure List'
    model = DailyExpendiature
    context_object_name = 'items'
    # paginate_by = 10
    template_name = 'tender/tender_project/list.html'
    queryset = DailyExpendiature.objects.filter()
    search_fields = ['project_name', 'job_no']
    list_display = ['total_amount', 'paid_method', 'date']
    url_list = ['expenditure_form_update', 'expenditure_delete', 'expenditure_details']

    def get_queryset(self):
        queryset = super().get_queryset()
        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['new_form'] = 'expenditure_form_create'
        context['fields'] = get_fields(self.model, self.list_display)
        context['update_url'] = self.url_list[0]
        context['delete_url'] = self.url_list[1]
        context['details_url'] = self.url_list[2]
        return context


class ExpenditureDetailView(generic.DetailView):
    model = DailyExpendiature
    context_object_name = 'instance'
    pk_url_kwarg = 'pk'
    # template_name = 'pdf-template/sample.html'
    template_name = 'tender/tender_project/details.html'
    title = "Expenditure Details"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ''
        context['title'] = self.title
        return context


class ExpenditureDeleteView(generic.edit.DeleteView):
    model = DailyExpendiature
    success_url = 'expenditure_list'
    template_name = 'components/delete_confirm.html'
    success_message = 'Deleted Successfully!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        else:
            self.object = self.get_object()
            self.object.delete()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(reverse_lazy(self.success_url))


class TenderSecurityCreateView(generic.CreateView):
    model = SecurityMoney
    form_class = SecurityMoneyForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Created Successfully."
    title = 'Security Money Create Form'
    success_url = "security_money_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        expendature_obj = DailyExpendiature()
        expendature_obj.security_money = self.object
        expendature_obj.quantity = 1
        expendature_obj.unit = 'None'
        expendature_obj.total_amount = form.cleaned_data['amount']
        expendature_obj.due_amount = form.cleaned_data['amount'] - form.cleaned_data['paid_amount']
        expendature_obj.paid_amount = form.cleaned_data['paid_amount']
        expendature_obj.paid_method = form.cleaned_data['security_type']
        expendature_obj.created_by = self.request.user
        with transaction.atomic():
            form.save()
            expendature_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class TenderPgCreateView(generic.CreateView):
    model = TenderPg
    form_class = TenderPgForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Created Successfully."
    title = 'Tender Performance Gurantee Create Form'
    success_url = "pg_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        expendature_obj = DailyExpendiature()
        expendature_obj.performance_gurantee = self.object
        expendature_obj.quantity = 1
        expendature_obj.unit = 'None'
        expendature_obj.total_amount = form.cleaned_data['amount']
        expendature_obj.due_amount = form.cleaned_data['amount'] - form.cleaned_data['paid_amount']
        expendature_obj.paid_amount = form.cleaned_data['paid_amount']
        expendature_obj.paid_method = form.cleaned_data['pg_type']
        expendature_obj.created_by = self.request.user
        with transaction.atomic():
            form.save()
            expendature_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class LoanPayCreateView(generic.CreateView):
    model = DailyExpendiature
    form_class = LoanPayForm
    template_name = 'tender/expendature/form.html'
    success_message = "Created Successfully."
    title = 'Loan Pay Create Form'
    success_url = "expenditure_dashboard"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.quantity = 1
        self.object.unit = 'None'
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
        
        bank_obj = form.cleaned_data['bank_info']
        cash_obj = form.cleaned_data['cash_balance']
        loan_obj = form.cleaned_data['loan_info']
        
        if loan_obj:
            loan_obj.balance += form.cleaned_data['paid_amount']
            loan_obj.save()
        if bank_obj:
            bank_obj.balance -= form.cleaned_data['paid_amount']
            bank_obj.updated_by = self.request.user
            bank_obj.save()
        
        if cash_obj:
            cash_obj.balance -= form.cleaned_data['paid_amount']
            cash_obj.updated_by = self.request.user
            cash_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class CashInCreateView(generic.CreateView):
    model = DailyExpendiature
    form_class = CashInForm
    template_name = 'tender/expendature/form.html'
    success_message = "Successfully Cash IN."
    title = 'Cash In Form'
    success_url = "cash_balance_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        bank_obj = form.cleaned_data['bank_info']
        # cash_obj = get_object_or_404(CashBalance, pk=1)
        
        self.object.paid_method = PaidMethodOption.BANK
        self.object.total_amount = form.cleaned_data['paid_amount']
        self.object.due_amount = 0
        self.object.quantity = 1
        self.object.unit = 'None'
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
        
        if bank_obj:
            bank_obj.balance -= form.cleaned_data['paid_amount']
            bank_obj.updated_by = self.request.user
            bank_obj.save()
        
        cash_obj = CashBalance.objects.first()
        cash_obj.balance += form.cleaned_data['paid_amount']
        cash_obj.updated_by = self.request.user
        cash_obj.save()

        messages.success(self.request, self.success_message)
        return self.get_success_url()

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context