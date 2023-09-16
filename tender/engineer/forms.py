from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from django.contrib.auth import get_user_model
from ..models import (ProjectSiteEngineer,)
User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].help_text = 'Provided email address correct email format'
        self.fields['username'].help_text = 'Must be Unique. Letters, digits and @/./+/-/_ only.'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("User with this Username Already Exists!!")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password('Ksy12345')
        if commit:
            user.save()
        return user


class SiteEngineerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SiteEngineerForm, self).__init__(*args, **kwargs)
        self.fields['balance'].initial ='0'
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.form_id = 'site_engineer_form_id'
        self.helper.layout = Layout(
            Row(
                Column('balance', css_class='form-group col-md-4 mb-0'),
                
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )
    class Meta:
        model = ProjectSiteEngineer
        exclude = ('user', 'created_at','updated_at','created_by','updated_by')