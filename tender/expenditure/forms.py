from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from ..models import DailyExpendiature

class ProjectExpendiatureForm(forms.ModelForm):
        date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['project'].widget.attrs['class'] ='select2_single form-control'
            self.fields['site_engier'].widget.attrs['class'] ='select2_single form-control'
            self.fields['main_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['sub_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['remarks'].widget.attrs['rows'] ='2'
            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.form_id = 'id_checkout_form'
            self.helper.layout = Layout(
                Row(
                    Column('project', css_class='form-group col-md-4 mb-0'),
                    Column('site_engier', css_class='form-group col-md-4 mb-0'),
                    Column('main_head', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('sub_head', css_class='form-group col-md-4 mb-0'),
                    Column('quantity', css_class='form-group col-md-4 mb-0'),
                    Column('unit', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('paid_method', css_class='form-group col-md-4 mb-0'),
                    Column('expendiature_type', css_class='form-group col-md-4 mb-0'),
                    Column('paid_amount', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('due_amount', css_class='form-group col-md-4 mb-0'),
                    Column('total_amount', css_class='form-group col-md-4 mb-0'),
                    Column('date', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('remarks', css_class='form-group col-md-4 mb-0'),
                    Column('bank_info', css_class='form-group col-md-4 mb-0'),
                    Column('cheque_no', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )
        
        class Meta:
            model = DailyExpendiature
            fields = ('project', 'site_engier','main_head', 'sub_head', 'quantity', 'unit', 'paid_method', 'expendiature_type',
                    'paid_amount', 'due_amount', 'total_amount', 'date', 'remarks', 'bank_info', 'cheque_no')


class SecurityMoneyExpendiatureForm(forms.ModelForm):
        date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['project'].widget.attrs['class'] ='select2_single form-control'
            self.fields['security_money'].widget.attrs['class'] ='select2_single form-control'
            self.fields['main_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['sub_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['remarks'].widget.attrs['rows'] ='2'


class PgExpendiatureForm(forms.ModelForm):
        date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['project'].widget.attrs['class'] ='select2_single form-control'
            self.fields['performance_gurantee'].widget.attrs['class'] ='select2_single form-control'
            self.fields['main_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['sub_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['remarks'].widget.attrs['rows'] ='2'


class LoanExpendiatureForm(forms.ModelForm):
        date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}))
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['project'].widget.attrs['class'] ='select2_single form-control'
            self.fields['loan_info'].widget.attrs['class'] ='select2_single form-control'
            self.fields['main_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['sub_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['remarks'].widget.attrs['rows'] ='2'