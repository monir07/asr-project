from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from .models import (TenderProject, RetensionMoney, SecurityMoney, TenderPg, CostMainHead, CostSubHead, DailyExpendiature)


class TenderProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        model_name = RetensionMoney
        maturity_date = forms.DateField(label='', required=False, widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            input_model = kwargs.get('model_name')
            RetensionMoneyForm.model_name = input_model
            self.fields['tender'].widget.attrs['class'] ='select2_single form-control'
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
                    Column('is_withdraw', css_class='form-group col-md-6 mb-0'),
                    Column('maturity_date', css_class='form-group col-md-6 mb-0'),
                    
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Continue', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )
        
        class Meta:
            model = model_class
            exclude = ('created_by', 'updated_by')
    return RetensionMoneyForm


class MainHeadForm(forms.ModelForm):
    balance = forms.FloatField(widget=forms.TextInput(attrs={'type': 'hidden'}), initial=0)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.form_id = 'id_cost_head_form'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('balance',),
                
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Continue', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )
    class Meta:
        model = CostMainHead
        fields = ('name', 'balance')


class SubHeadForm(forms.ModelForm):
    balance = forms.FloatField(widget=forms.TextInput(attrs={'type': 'hidden'}), initial=0)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.form_id = 'id_cost_head_form'
        self.helper.layout = Layout(
            Row(
                Column('main_head', css_class='form-group col-md-6 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('balance',),
                
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Continue', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )
    class Meta:
        model = CostSubHead
        fields = ('main_head', 'name', 'balance')