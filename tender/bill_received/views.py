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
from ..models import MoneyReceived, LoanOption
from .forms import *
from asr.utility import format_search_string, get_fields

class BillReceivedDashboardView(generic.TemplateView):
    title = 'Received Money Dashboard'
    template_name="tender/expendature/dashboard.html"
    url_list = {
                'url_1':['all_bill_receive', 'Bill Received', 'fa fa-caret-square-o-right'],
                'url_2':['received_security_money_create', 'Tender Security', 'fa fa-comments-o'],
                'url_3':['received_pg_create', 'Tender PG', 'fa fa-sort-amount-desc'],
                'url_4':['collection_loan_create', 'Loan Collection', 'fa fa-check-square-o'],
                'url_5':['received_loan_create', 'Loan Received', 'fa fa-cart-arrow-down'],
                'url_6':['all_received_list', 'Received List', 'fa fa-list'],
            }

    def get_context_data(self, **kwargs):
        kwargs['url_list'] = self.url_list
        kwargs['title'] = self.title
        return super().get_context_data(**kwargs)


class SecurityMoneyReceivedCreateView(generic.CreateView):
    model = MoneyReceived
    form_class = SecurityReceivedForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Tender Security Money Received Success."
    title = 'Tender Security Receive Form'
    success_url = "tender_project_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        security_obj = form.cleaned_data['tender_security']
        deposit_bank_obj = form.cleaned_data['bank_info']
        cash_obj = form.cleaned_data['cash_balance']
        security_obj.is_withdraw = True
        self.object.received_amount = form.cleaned_data['total_amount']
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
            security_obj.save()
        
        if deposit_bank_obj:
            deposit_bank_obj.balance += form.cleaned_data['total_amount']
            deposit_bank_obj.updated_by = self.request.user
            deposit_bank_obj.save()
        if cash_obj:
            cash_obj.balance += form.cleaned_data['total_amount']
            cash_obj.updated_by = self.request.user
            cash_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class PgReceivedCreateView(generic.CreateView):
    model = MoneyReceived
    form_class = PgReceivedForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Tender Performance Guarantee Received Success."
    title = 'Tender Performance Guarantee Receive Form'
    success_url = "tender_project_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        pg_obj = form.cleaned_data['performance_gurantee']
        deposit_bank_obj = form.cleaned_data['bank_info']
        cash_obj = form.cleaned_data['cash_balance']
        pg_obj.is_withdraw = True
        self.object.received_amount = form.cleaned_data['total_amount']
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
            pg_obj.save()
        
        if deposit_bank_obj:
            deposit_bank_obj.balance += form.cleaned_data['total_amount']
            deposit_bank_obj.updated_by = self.request.user
            deposit_bank_obj.save()
        if cash_obj:
            cash_obj.balance += form.cleaned_data['total_amount']
            cash_obj.updated_by = self.request.user
            cash_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class LoanCollectionCreateView(generic.CreateView):
    model = MoneyReceived
    form_class = LoanCollectionForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Loan Collection Success."
    title = 'Loan Collection Form'
    success_url = "received_dashboard"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        loan_obj = form.cleaned_data['loan_info']
        deposit_bank_obj = form.cleaned_data['bank_info']
        cash_obj = form.cleaned_data['cash_balance']
        loan_obj.amount -= form.cleaned_data['total_amount']
        self.object.received_amount = form.cleaned_data['total_amount']
        self.object.loan_type = LoanOption.COLLECTION
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
            loan_obj.save()
        
        if deposit_bank_obj:
            deposit_bank_obj.balance += form.cleaned_data['total_amount']
            deposit_bank_obj.updated_by = self.request.user
            deposit_bank_obj.save()
        if cash_obj:
            cash_obj.balance += form.cleaned_data['total_amount']
            cash_obj.updated_by = self.request.user
            cash_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class LoanReceivedCreateView(generic.CreateView):
    model = MoneyReceived
    form_class = LoanCollectionForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Loan Received Success."
    title = 'Loan Received Form'
    success_url = "received_dashboard"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        loan_obj = form.cleaned_data['loan_info']
        deposit_bank_obj = form.cleaned_data['bank_info']
        cash_obj = form.cleaned_data['cash_balance']
        loan_obj.amount = form.cleaned_data['total_amount']
        self.object.received_amount = form.cleaned_data['total_amount']
        self.object.loan_type = LoanOption.RECEIVE
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
            loan_obj.save()
        
        if deposit_bank_obj:
            deposit_bank_obj.balance += form.cleaned_data['total_amount']
            deposit_bank_obj.updated_by = self.request.user
            deposit_bank_obj.save()
        if cash_obj:
            cash_obj.balance += form.cleaned_data['total_amount']
            cash_obj.updated_by = self.request.user
            cash_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context

class BillReceivedCreateView(generic.CreateView):
    model = MoneyReceived
    form_class = BillReceivedForm
    template_name = 'tender/bill_received/form.html'
    success_message = "Bill Received Success."
    title = 'Bill Receive Form'
    success_url = "received_dashboard"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        deposit_bank_obj = form.cleaned_data['bank_info']
        cash_obj = form.cleaned_data['cash_balance']
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
        
        if deposit_bank_obj:
            deposit_bank_obj.balance += form.cleaned_data['total_amount']
            deposit_bank_obj.updated_by = self.request.user
            deposit_bank_obj.save()
        if cash_obj:
            cash_obj.balance += form.cleaned_data['total_amount']
            cash_obj.updated_by = self.request.user
            cash_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class MoneyReceivedListView(generic.ListView):
    title = 'Money Received List'
    model = MoneyReceived
    context_object_name = 'items'
    paginate_by = 10
    template_name = 'tender/tender_project/list.html'
    queryset = MoneyReceived.objects.filter()
    search_fields = ['project', 'received_method']
    list_display = ['total_amount', 'received_method', 'received_amount']
    url_list = ['expenditure_form_update', 'expenditure_delete', 'received_details']

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
        context['fields'] = get_fields(self.model, self.list_display)
        context['update_url'] = self.url_list[0]
        context['delete_url'] = self.url_list[1]
        context['details_url'] = self.url_list[2]
        return context


class MoneyReceivedDetailView(generic.DetailView):
    model = MoneyReceived
    context_object_name = 'instance'
    pk_url_kwarg = 'pk'
    # template_name = 'pdf-template/sample.html'
    template_name = 'tender/tender_project/details.html'
    title = "Money Reveived Details"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ''
        context['title'] = self.title
        return context