from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from ..models import (DailyExpendiature, PaidMethodOption, TenderPg, SecurityMoney, LoanInformation)


class ProjectExpendiatureForm(forms.ModelForm):
        date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}), initial=timezone.now())
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['project'].widget.attrs['class'] ='select2_single form-control'
            self.fields['site_engier'].widget.attrs['class'] ='select2_single form-control'
            self.fields['main_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['sub_head'].widget.attrs['class'] ='select2_single form-control'
            self.fields['paid_method'].widget.attrs['class'] ='select2_single form-control'
            self.fields['bank_info'].widget.attrs['class'] ='select2_single form-control'
            self.fields['cash_balance'].widget.attrs['class'] ='select2_single form-control'
            self.fields['cash_balance'].label ='Select Cash Balance'
            self.fields['bank_info'].label ='Select Bank'
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
                    Column('total_amount', css_class='form-group col-md-4 mb-0'),
                    Column('due_amount', css_class='form-group col-md-4 mb-0'),
                    Column('paid_amount', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('paid_method', css_class='form-group col-md-4 mb-0'),
                    Column('bank_info', css_class='form-group col-md-4 mb-0'),
                    Column('cheque_no', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                
                Row(
                    Column('cash_balance', css_class='form-group col-md-4 mb-0'),
                    Column('date', css_class='form-group col-md-4 mb-0'),
                    Column('remarks', css_class='form-group col-md-4 mb-0'),
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
            fields = ('project', 'site_engier','main_head', 'sub_head', 'quantity', 'unit', 'paid_method',
                    'total_amount', 'due_amount', 'paid_amount', 'date', 'remarks', 'bank_info', 'cheque_no',
                    'cash_balance')

        def clean(self):
            cleaned_data = super().clean()
            paid_method = cleaned_data.get('paid_method')

            if paid_method == PaidMethodOption.BANK:
                bank_info = cleaned_data.get('bank_info')
                cheque_no = cleaned_data.get('cheque_no')
                paid_amount = cleaned_data.get('paid_amount')

                if bank_info.balance < paid_amount:
                    self.add_error('bank_info', 'Dont have sufficient Balance')
                    self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'                     
                if not bank_info:
                    self.add_error('bank_info', 'Deposit Bank is required for Bank Paid type.')
                    self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'
                if not cheque_no:
                    self.add_error('cheque_no', 'Cheque no is required for Bank Paid type.')
                    self.fields['cheque_no'].widget.attrs['class'] = 'parsley-error'

            elif paid_method == PaidMethodOption.CASH:
                cash_obj = cleaned_data.get('cash_balance')
                paid_amount = cleaned_data.get('paid_amount')

                if not cash_obj:
                    self.add_error('cash_balance', 'Cash Balance is required for Cash Paid type.')
                    self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
                
                if cash_obj:
                    if cash_obj.balance < paid_amount:
                        self.add_error('cash_balance', 'Dont have sufficient Balance')
                        self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
            elif paid_method == PaidMethodOption.DUE:
                due_amount = cleaned_data.get('due_amount')
                if not due_amount:
                    self.add_error('due_amount', 'Due Amount is required for Due Paid type.')
                    self.fields['due_amount'].widget.attrs['class'] = 'parsley-error'
            return cleaned_data
        

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


class LoanPayForm(forms.ModelForm):
        date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}), initial=timezone.now())

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['paid_method'].widget.attrs['class'] ='select2_single form-control'
            self.fields['loan_info'].widget.attrs['class'] ='select2_single form-control'
            self.fields['loan_info'].label = 'Select Borrower'
            self.fields['cash_balance'].widget.attrs['class'] ='select2_single form-control'
            self.fields['cash_balance'].label = 'Select Cash Balance'
            self.fields['bank_info'].widget.attrs['class'] ='select2_single form-control'
            self.fields['bank_info'].label = 'Select Bank'
            self.fields['remarks'].widget.attrs['rows'] ='2'


            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('loan_info', css_class='form-group col-md-12 mb-0'),
                ),
                Row(
                    Column('total_amount', css_class='form-group col-md-4 mb-0'),
                    Column('due_amount', css_class='form-group col-md-4 mb-0'),
                    Column('paid_amount', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('paid_method', css_class='form-group col-md-4 mb-0'),
                    Column('bank_info', css_class='form-group col-md-4 mb-0'),
                    Column('cheque_no', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('cash_balance', css_class='form-group col-md-4 mb-0'),
                    Column('date', css_class='form-group col-md-4 mb-0'),
                    Column('remarks', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Continue', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )
            
        class Meta:
            model = DailyExpendiature
            fields = ('loan_info', 'total_amount', 'due_amount',   
                    'paid_amount', 'date', 'remarks', 'paid_method', 
                    'bank_info', 'cheque_no',
                    'cash_balance')
        
        def clean(self):
            cleaned_data = super().clean()
            paid_method = cleaned_data.get('paid_method')

            if paid_method == PaidMethodOption.BANK:
                bank_info = cleaned_data.get('bank_info')
                cheque_no = cleaned_data.get('cheque_no')
                paid_amount = cleaned_data.get('paid_amount')

                if not bank_info:
                    self.add_error('bank_info', 'Deposit Bank is required for Bank Paid type.')
                    self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'
                if not cheque_no:
                    self.add_error('cheque_no', 'Cheque no is required for Bank Paid type.')
                    self.fields['cheque_no'].widget.attrs['class'] = 'parsley-error'
                elif bank_info.balance < paid_amount:
                    self.add_error('bank_info', 'Dont have sufficient Balance')
                    self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'                     
            elif paid_method == PaidMethodOption.CASH:
                cash_obj = cleaned_data.get('cash_balance')
                paid_amount = cleaned_data.get('paid_amount')

                if not cash_obj:
                    self.add_error('cash_balance', 'Cash Balance is required for Cash Paid type.')
                    self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
                
                elif cash_obj.balance < paid_amount:
                    self.add_error('cash_balance', 'Dont have sufficient Balance')
                    self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
            
            elif paid_method == PaidMethodOption.DUE:
                due_amount = cleaned_data.get('due_amount')
                if not due_amount:
                    self.add_error('due_amount', 'Due Amount is required for Due Paid type.')
                    self.fields['due_amount'].widget.attrs['class'] = 'parsley-error'
            return cleaned_data


class CashInForm(forms.ModelForm):
        date = forms.DateField(widget=forms.DateInput(
            attrs={'type': 'date'}), initial=timezone.now())

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['bank_info'].widget.attrs['class'] ='select2_single form-control'
            self.fields['bank_info'].label = 'Select Bank'
            self.fields['bank_info'].required = True
            self.fields['cheque_no'].required = True
            self.fields['paid_amount'].label = 'Total Amount'
            self.fields['remarks'].widget.attrs['rows'] ='2'


            self.helper = FormHelper()    
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                
                Row(
                    Column('bank_info', css_class='form-group col-md-4 mb-0'),
                    Column('cheque_no', css_class='form-group col-md-4 mb-0'),
                    Column('paid_amount', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column('date', css_class='form-group col-md-4 mb-0'),
                    Column('remarks', css_class='form-group col-md-4 mb-0'),
                    css_class='row'
                ),
                Row(
                    Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                    Column(Submit('submit', 'Continue', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                    css_class='row'
                ),
            )
            
        class Meta:
            model = DailyExpendiature
            fields = ('paid_amount', 'date', 'remarks', 'bank_info', 'cheque_no')
        
        def clean(self):
            cleaned_data = super().clean()
            bank_info = cleaned_data.get('bank_info')
            paid_amount = cleaned_data.get('paid_amount')

            if bank_info.balance < paid_amount:
                self.add_error('bank_info', 'Dont have sufficient Balance')
                self.add_error('paid_amount', 'Dont have sufficient Balance')
                self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'
                self.fields['paid_amount'].widget.attrs['class'] = 'parsley-error'
                
            return cleaned_data