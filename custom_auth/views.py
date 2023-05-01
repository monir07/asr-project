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
from django.contrib.auth.views import (LoginView, LogoutView)
from django.contrib.auth import (login as auth_login)
from .log_entry import CustomLogEntry
from .mixin import CommonMixin
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/form.html'
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

class Dashboard(generic.TemplateView):
    template_name = 'base_template/dashboard.html'
    title = 'ASR Dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context    