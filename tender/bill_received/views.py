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
from ..models import MoneyReceived
from .forms import *

class BillReceivedDashboardView(generic.TemplateView):
    title = 'Received Money Dashboard'
    template_name="tender/expendature/dashboard.html"
    url_list = {
                'url_1':['tender_project_create', 'Bill Received', 'fa fa-caret-square-o-right'],
                'url_2':['received_security_money_create', 'Tender Security', 'fa fa-comments-o'],
                'url_3':['received_pg_create', 'Tender Performance Guarantee', 'fa fa-sort-amount-desc'],
                'url_4':['received_loan_create', 'Loan Received', 'fa fa-check-square-o'],
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
        security_obj.is_withdraw = True
        self.object.received_amount = form.cleaned_data['total_amount']
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
            security_obj.save()
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
        pg_obj.is_withdraw = True
        self.object.received_amount = form.cleaned_data['total_amount']
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
            pg_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class LoanReceivedCreateView(generic.CreateView):
    model = MoneyReceived
    form_class = LoanReceivedForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Loan Received Success."
    title = 'Loan Receive Form'
    success_url = "received_dashboard"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        loan_obj = form.cleaned_data['loan_info']
        loan_obj.amount -= form.cleaned_data['total_amount']
        self.object.received_amount = form.cleaned_data['total_amount']
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
            loan_obj.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context