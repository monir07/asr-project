import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from ..models import ProjectSiteEngineer, UserProfile
from .forms import (SiteEngineerForm, UserRegisterForm)
from ..forms import UserProfileForm
from formtools.wizard.views import SessionWizardView


class SiteEngineerCreateView(SessionWizardView):
    login_url = 'login'
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'files'))
    template_name = 'authentication/registration_final.html'
    success_message = "Profile Created Successfully!"
    title = "Create Site Engineer Profile."
    form_list = [UserRegisterForm, UserProfileForm]

    def done(self, form_list, **kwargs):
        with transaction.atomic():
            if form_list[0].is_valid():
                user_obj = form_list[0].save()
                user_inform_form = form_list[1].save(commit=False)
                user_inform_form.user = user_obj
                user_inform_form.created_by = self.request.user
                user_inform_form.save()
                # user = form_list[0].save()
                # ProjectSiteEngineer.objects.create(user=user, balance=0, created_by=self.request.user)
                messages.success(self.request, self.success_message)
            else:
                messages.error(self.request, 'Something Went Wrong!')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = "base_template/base_site.html"
        context['title'] = self.title
        return context


class UserProfileDetailView(generic.DetailView):
    model = UserProfile
    context_object_name = 'instance'
    pk_url_kwarg = 'pk'
    # template_name = 'pdf-template/sample.html'
    template_name = 'authentication/user_profile/details.html'
    title = "Profile details"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ''
        context['title'] = self.title
        return context