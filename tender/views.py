import datetime
from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader
from django.http import HttpResponse
from asr.utility import format_search_string, get_fields
from .forms import (TenderProjectForm, LoanInformationsForm)
from .models import (TenderProject, RetensionMoney, SecurityMoney, TenderPg, CostMainHead, CostSubHead, DailyExpendiature, LoanInformation)


# Create your views here.
class TenderProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = TenderProject
    form_class = TenderProjectForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Created Successfully."
    title = 'Tender Project Create Form'
    success_url = "tender_project_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        with transaction.atomic():
            form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class TenderProjectUpdateView(generic.UpdateView):
    form_class = TenderProjectForm
    model = TenderProject
    context_object_name = 'instance'
    template_name = 'tender/tender_project/form.html'
    success_message = 'Data updated successfully'
    success_url = "tender_project_list"
    title = 'Tender Project Update Form'


    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()

        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ''
        context['title'] = self.title
        return context
    

class TenderProjectListView(generic.ListView):
    # permission_required = 'eshop.view_product'
    title = 'Tender Project List'
    model = TenderProject
    context_object_name = 'items'
    # paginate_by = 9
    template_name = 'tender/tender_project/list.html'
    queryset = TenderProject.objects.all()
    search_fields = ['project_name', 'job_no']
    list_display = ['project_name', 'job_no', 'project_location', 'contact_value', 'number_of_infrastructure', 'procuring_entity_name']
    url_list = ['tender_project_update', 'tender_project_delete', 'tender_project_details']

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
        context['product_count'] = self.get_queryset().count()
        context['title'] = self.title
        context['fields'] = get_fields(self.model, self.list_display)
        context['update_url'] = self.url_list[0]
        context['delete_url'] = self.url_list[1]
        context['details_url'] = self.url_list[2]
        return context


class TenderProjectDetailView(generic.DetailView):
    model = TenderProject
    context_object_name = 'instance'
    pk_url_kwarg = 'pk'
    # template_name = 'pdf-template/sample.html'
    template_name = 'tender/tender_project/details.html'
    title = "project details"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ''
        context['title'] = self.title
        return context


class TenderProjectDeleteView(generic.edit.DeleteView):
    model = TenderProject
    success_url = 'tender_project_list'
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


class MainHeadCreateView(generic.CreateView):
    model = CostMainHead
    form_class = None
    template_name = 'tender/tender_project/form.html'
    success_message = "Created Successfully."
    title = 'Cost Head Create Form'
    success_url = "tender_project_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        with transaction.atomic():
            form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        context['title'] = self.title
        return context


class CostHeadUpdateView(generic.UpdateView):
    form_class = None
    model = CostMainHead
    context_object_name = 'instance'
    template_name = 'tender/tender_project/form.html'
    success_message = 'Data updated successfully'
    success_url = "tender_project_list"
    title = 'Cost Head Update Form'


    def form_valid(self, form, *args, **kwargs):
        form.save()
        
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy(self.success_url))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ''
        context['title'] = self.title
        return context






import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def render_pdf_view(request):
    template_path = 'pdf-template/sample.html'
    context = {'title': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    # pisa_status = pisa.CreatePDF(
    #    html, dest=response)
    result = BytesIO()
    pisa_status = pisa.pisaDocument(
        src=BytesIO(html.encode("ISO-8859-1")),
        dest=result,
        # encoding='UTF-8'
    )
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response
    return HttpResponse(result.getvalue(), content_type='application/pdf')