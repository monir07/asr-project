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
from ..models import DailyExpendiature

class BillReceivedDashboardView(generic.TemplateView):
    title = 'Received Money Dashboard'
    template_name="tender/expendature/dashboard.html"
    url_list = {
                'url_1':['tender_project_create', 'Bill Received', 'fa fa-caret-square-o-right'],
                'url_2':['tender_project_create', 'Tender Security', 'fa fa-comments-o'],
                'url_3':['tender_project_create', 'Tender Performance Guarantee', 'fa fa-sort-amount-desc'],
                'url_4':['tender_project_create', 'Loan Received', 'fa fa-check-square-o'],
            }

    def get_context_data(self, **kwargs):
        kwargs['url_list'] = self.url_list
        kwargs['title'] = self.title
        return super().get_context_data(**kwargs)