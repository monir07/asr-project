from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from .models import (ProjectSiteEngineer, TenderProject, 
                    RetensionMoney, SecurityMoney, TenderPg, CostMainHead,
                    CostSubHead, DailyExpendiature, BankInformation, 
                    LoanInformation, PaidMethodOption, SecurityOption, UserProfile)
from custom_auth.validator import MyValidator

class SiteEngineerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SiteEngineerForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] ='select2_single form-control'
        self.fields['balance'].initial ='0'
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.form_id = 'site_engineer_form_id'
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-4 mb-0'),
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
        exclude = ('created_at','updated_at','created_by','updated_by')


class BankInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BankInformationForm, self).__init__(*args, **kwargs)
        self.fields['account_no'].help_text = 'Must be unique.'
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.form_id = 'bank_info_form_id'
        self.helper.layout = Layout(
            Row(
                Column('account_no', css_class='form-group col-md-6 mb-0'),
                Column('bank_name', css_class='form-group col-md-6 mb-0'),
                
                css_class='row'
            ),
            Row(
                Column('branch_name', css_class='form-group col-md-6 mb-0'),
                Column('balance', css_class='form-group col-md-6 mb-0'),
                
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )
    class Meta:
        model = BankInformation
        exclude = ('created_at','updated_at','created_by','updated_by')


class TenderProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['engineer'].widget.attrs['class'] ='select2_single form-control'
        self.fields['infrastructure_description'].widget.attrs= {'rows': 2}
        self.fields['short_description'].widget.attrs = {'rows': 2}
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.form_id = 'demo-form2'
        self.helper.layout = Layout(
            Row(
                Column('engineer', css_class='form-group col-md-4 mb-0'),
                Column('project_name', css_class='form-group col-md-4 mb-0'),
                Column('job_no', css_class='form-group col-md-4 mb-0'),
                
                css_class='row'
            ),
            Row(
                Column('project_location', css_class='form-group col-md-4 mb-0'),
                Column('procuring_entity_name', css_class='form-group col-md-4 mb-0'),
                Column('contact_value', css_class='form-group col-md-4 mb-0'),

                css_class='row'
            ),
            Row(
                
                Column('number_of_infrastructure', css_class='form-group col-md-4 mb-0'),
                Column('short_description', css_class='form-group col-md-4 mb-0'),
                Column('infrastructure_description', css_class='form-group col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )
    class Meta:
        model = TenderProject
        exclude = ('created_at','updated_at','created_by','updated_by', 'project_complete')


def get_form(model_class):
    class RetensionMoneyForm(forms.ModelForm):
        maturity_date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tender'].widget.attrs['class'] ='select2_single form-control'
            self.fields['remarks'].widget.attrs['rows'] ='2'
            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.form_id = 'id_checkout_form'
            self.helper.layout = Layout(
                Row(
                    Column('tender', css_class='form-group col-md-6 mb-0'),
                    Column('amount', css_class='form-group col-md-6 mb-0'),
                    
                    css_class='row'
                ),
                Row(
                    
                    Column('remarks', css_class='form-group col-md-6 mb-0'),
                    Column('maturity_date', css_class='form-group col-md-3 mb-0'),
                    Column('is_withdraw', css_class='form-group col-md-3 mb-0'),
                    
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )
        
        class Meta:
            model = model_class
            exclude = ('created_by', 'updated_by')
    return RetensionMoneyForm

class SecurityMoneyForm(forms.ModelForm):
        maturity_date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tender'].widget.attrs['class'] ='select2_single form-control'
            self.fields['security_type'].widget.attrs['class'] ='select2_single form-control'
            self.fields['tender'].label ='Select Tender Project'
            self.fields['bank_details'].widget.attrs['rows'] ='2'
            self.fields['remarks'].widget.attrs['rows'] ='2'
            self.fields['is_withdraw'].help_text ='Checked, when received security money.'
            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.form_id = 'id_checkout_form'
            self.helper.layout = Layout(
                Row(
                    Column('tender', css_class='form-group col-md-6 mb-0'),
                    Column('amount', css_class='form-group col-md-6 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('paid_amount', css_class='form-group col-md-4 mb-0'),
                    Column('security_type', css_class='form-group col-md-4 mb-0'),
                    Column('maturity_date', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('bank_details', css_class='form-group col-md-4 mb-0'),
                    Column('remarks', css_class='form-group col-md-4 mb-0'),
                    Column('is_withdraw', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )
        
        class Meta:
            model = SecurityMoney
            fields = ('tender', 'amount', 'paid_amount', 'security_type', 'is_withdraw', 'maturity_date', 'remarks', 'bank_details')

        def clean(self):
            cleaned_data = super().clean()
            security_type = cleaned_data.get('security_type')

            if security_type == SecurityOption.BANK:
                bank_details = cleaned_data.get('bank_details')
                if not bank_details:
                    self.add_error('bank_details', 'Bank details is required for Bank type.')
                    self.fields['bank_details'].widget.attrs['class'] = 'parsley-error'
            return cleaned_data


class TenderPgForm(forms.ModelForm):
        maturity_date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tender'].widget.attrs['class'] ='select2_single form-control'
            self.fields['pg_type'].widget.attrs['class'] ='select2_single form-control'
            self.fields['tender'].label ='Select Tender Project'
            self.fields['remarks'].widget.attrs['rows'] ='2'
            self.fields['bank_details'].widget.attrs['rows'] ='2'
            self.fields['is_withdraw'].help_text ='Checked, when received PG.'
            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.form_id = 'id_checkout_form'
            self.helper.layout = Layout(
                Row(
                    Column('tender', css_class='form-group col-md-6 mb-0'),
                    Column('amount', css_class='form-group col-md-6 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('paid_amount', css_class='form-group col-md-4 mb-0'),
                    Column('pg_type', css_class='form-group col-md-4 mb-0'),
                    Column('maturity_date', css_class='form-group col-md-4 mb-0'),
                    
                    css_class='row'
                ),
                Row(
                    Column('bank_details', css_class='form-group col-md-4 mb-0'),
                    Column('remarks', css_class='form-group col-md-4 mb-0'),
                    Column('is_withdraw', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Continue', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )
        
        class Meta:
            model = TenderPg
            fields = ('tender', 'pg_type','amount', 'paid_amount', 'is_withdraw', 
                    'maturity_date', 'remarks', 'bank_details')
        
        def clean(self):
            cleaned_data = super().clean()
            pg_type = cleaned_data.get('pg_type')

            if pg_type == SecurityOption.BANK:
                bank_details = cleaned_data.get('bank_details')
                if not bank_details:
                    self.add_error('bank_details', 'Bank details is required for Bank type.')
                    self.fields['bank_details'].widget.attrs['class'] = 'parsley-error'
            return cleaned_data



def get_cost_head_form(model_class):
    class CostHeadForm(forms.ModelForm):
        balance = forms.CharField(label='', widget=forms.TextInput(
            attrs={'type': 'hidden'}), initial='0')
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.form_id = 'id_cost_head_form'
            if model_class == CostSubHead:
                self.fields['main_head'].widget.attrs['class'] ='select2_single form-control'
                self.helper.layout = Layout(
                    Row(
                        Column('main_head', css_class='form-group col-md-6 mb-0'),
                        Column('name', css_class='form-group col-md-6 mb-0'),
                        Column('balance',),
                        
                        css_class='row'
                    ),
                    Row(
                        Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                        Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                        css_class='row'
                    ),
                )
            else:
                self.helper.layout = Layout(
                    Row(
                        Column('name', css_class='form-group col-md-6 mb-0'),
                        Column('balance',),
                        
                        css_class='row'
                    ),
                    Row(
                        Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                        Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                        css_class='row'
                    ),
                )
        
        class Meta:
            model = model_class
            exclude = ('created_at','updated_at','slug')
    return CostHeadForm


class UserProfileForm(forms.ModelForm):
        date_of_birth = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        date_of_join = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        profile_img = forms.ImageField(#widget=forms.ClearableFileInput(), required=False, 
            validators=[MyValidator(allowed_extensions=['jpg', 'png', 'jpeg'],  
            allowed_size=2, 
            message=None, code=None)], 
            help_text="File size should be less than 2MB with ().jpg .png .jpeg) extension. size 300x300 px")
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['religion'].widget.attrs['class'] ='select2_single form-control'
            self.fields['marital_status'].widget.attrs['class'] ='select2_single form-control'
            self.fields['gender'].widget.attrs['class'] ='select2_single form-control'
            self.fields['blood_group'].widget.attrs['class'] ='select2_single form-control'
        
        class Meta:
            model = UserProfile
            fields = ('profile_img', 'father_name', 'mother_name', 
                      'designation', 'nid_no', 'phone_no', 'religion', 
                      'marital_status', 'gender', 'blood_group', 'date_of_birth',
                      'date_of_join', 'address',
                      )


class LoanBorrowerForm(forms.ModelForm):
        class Meta:
            model = LoanInformation
            fields = ('borrower_name', 'phone_no', 'address', 'balance')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['address'].widget.attrs['rows'] ='2'

            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('borrower_name', css_class='form-group col-md-6 mb-0'),
                    Column('phone_no', css_class='form-group col-md-6 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('address', css_class='form-group col-md-6 mb-0'),
                    Column('balance', css_class='form-group col-md-6 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )        
