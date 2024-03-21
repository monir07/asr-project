from django.shortcuts import resolve_url, render
from django.http import Http404
from django.views import View, generic
from django.conf import settings
from .forms import *
from django.contrib.auth.models import User
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import (LoginView, PasswordChangeView, LogoutView)
from django.contrib.auth import (login as auth_login, logout as auth_logout)
from django.template import loader
from django.http import HttpResponse
from .log_entry import CustomLogEntry
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import CommonMixin
from asr.utility import format_search_string, get_fields
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class SignUpCreateView(generic.CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'authentication/sign_up.html'
    success_message = "User Registration Success."
    title = "User Registration Form"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        with transaction.atomic():
            self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_default_redirect_url())

    def get_default_redirect_url(self, **kwargs):
        """Return the default redirect URL."""
        get_request = self.request.GET.copy()
        if get_request.get('next', None):
            self.next_page = get_request.get('next')
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
    

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'authentication/login.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Login successfully'
    title = "User Login Form"
    next_page = None

    def get_default_redirect_url(self, **kwargs):
        """Return the default redirect URL."""
        get_request = self.request.GET.copy()
        if get_request.get('next', None):
            self.next_page = get_request.get('next')
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        messages.success(self.request, self.success_message)
        log_obj = CustomLogEntry()
        log_obj.log_addition(self.request, form.get_user(), self.success_message)
        return HttpResponseRedirect(self.get_default_redirect_url())    

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # print("User is authenticated")
            return HttpResponseRedirect(self.success_url)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

class UserLogoutView(View):
    next_page = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Logout successfully'
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.next_page)

class UserPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy(settings.LOGIN_URL)
    template_name = 'authentication/change_password.html'
    title = 'Password change form'
    success_message = 'Password Change successfully'


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    # template_name = 'base_template/dashboard.html'
    template_name="tender/expendature/dashboard.html"
    title = 'ASR Dashboard'
    url_list = {
                'url_1':['all_bill_receive', 'Project', 'fa fa-caret-square-o-right', 'Here all ongoing project list'],
                'url_2':['received_security_money_create', 'Tender Security', 'fa fa-comments-o', 'Here all ongoing pg list'],
                'url_3':['received_pg_create', 'Tender PG', 'fa fa-sort-amount-desc', 'Here all ongoing sq list'],
                'url_4':['collection_loan_create', 'Loan Collection', 'fa fa-check-square-o', 'Here all ongoing loan list'],
                'url_5':['received_loan_create', 'Loan Received', 'fa fa-cart-arrow-down', 'Here all ongoing retention list'],
                'url_6':['all_received_list', 'Received List', 'fa fa-list', 'Here all ongoing received list'],
            }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['url_list'] = self.url_list
        return context


class UserListView(LoginRequiredMixin, generic.ListView):
    title = 'All User List'
    model = User
    context_object_name = 'items'
    # paginate_by = 9
    template_name = 'authentication/user_profile/list.html'
    list_display = ['username', 'first_name', 'last_name']
    url_list = ['user_profile_details']
    # queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['fields'] = get_fields(self.model, self.list_display)
        context['details_url'] = self.url_list[0]
        return context    

def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))    