from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from ..models import (MoneyReceived, ReceivedOption, TenderPg, SecurityMoney, LoanInformation)


class SecurityReceivedForm(forms.ModelForm):
    class Meta:
        model = MoneyReceived
        fields = ('tender_security','total_amount', 'received_method', 
                'recieved_cheque_no', 'recieved_bank_name', 'check_attachment')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tender_security'] = forms.ModelChoiceField(queryset=SecurityMoney.objects.filter(is_withdraw=False))
        self.fields['tender_security'].widget.attrs['class'] ='select2_single form-control'
        self.fields['tender_security'].label ='Select Tender Project'
        self.fields['received_method'].widget.attrs['class'] ='select2_single form-control'
        
        field_list = self.Meta.fields
        self.helper = FormHelper()
        # self.helper.form_method = 'get' # get or post
        self.helper.layout = Layout()
        # form fields layout.
        column_fields = []
        for field in field_list:
            column_fields.append(Column(f'{field}', css_class='form-group col-md-4 mb-0'))
        self.helper.layout.append(Row(
            *column_fields,
            css_class='row',
        ))
        # submit section btn
        self.helper.layout.append(Row(
            Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
            Column(Submit('submit', 'Update' if self.instance.pk else 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
            css_class='row'
        ))
    
    def clean(self):
            cleaned_data = super().clean()
            received_method = cleaned_data.get('received_method')

            if received_method == ReceivedOption.BANK:
                bank_name = cleaned_data.get('recieved_bank_name')
                cheque_no = cleaned_data.get('recieved_cheque_no')
                if not bank_name:
                    self.add_error('recieved_bank_name', 'Bank name is required for Bank Receive type.')
                    self.fields['recieved_bank_name'].widget.attrs['class'] = 'parsley-error'

                if not cheque_no:
                    self.add_error('recieved_cheque_no', 'Cheque number is required for Bank Receive type.')
                    self.fields['recieved_cheque_no'].widget.attrs['class'] = 'parsley-error'
            return cleaned_data


class PgReceivedForm(forms.ModelForm):
    class Meta:
        model = MoneyReceived
        fields = ('performance_gurantee','total_amount', 'received_method', 
                'recieved_cheque_no', 'recieved_bank_name', 'check_attachment')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['performance_gurantee'] = forms.ModelChoiceField(queryset=TenderPg.objects.filter(is_withdraw=False))
        self.fields['performance_gurantee'].widget.attrs['class'] ='select2_single form-control'
        self.fields['performance_gurantee'].label ='Select Tender Project'
        self.fields['received_method'].widget.attrs['class'] ='select2_single form-control'
        
        field_list = self.Meta.fields
        self.helper = FormHelper()
        # self.helper.form_method = 'get' # get or post
        self.helper.layout = Layout()
        # form fields layout.
        column_fields = []
        for field in field_list:
            column_fields.append(Column(f'{field}', css_class='form-group col-md-4 mb-0'))
        self.helper.layout.append(Row(
            *column_fields,
            css_class='row',
        ))
        # submit section btn
        self.helper.layout.append(Row(
            Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
            Column(Submit('submit', 'Update' if self.instance.pk else 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
            css_class='row'
        ))
    
    def clean(self):
            cleaned_data = super().clean()
            received_method = cleaned_data.get('received_method')

            if received_method == ReceivedOption.BANK:
                bank_name = cleaned_data.get('recieved_bank_name')
                cheque_no = cleaned_data.get('recieved_cheque_no')
                if not bank_name:
                    self.add_error('recieved_bank_name', 'Bank name is required for Bank Receive type.')
                    self.fields['recieved_bank_name'].widget.attrs['class'] = 'parsley-error'

                if not cheque_no:
                    self.add_error('recieved_cheque_no', 'Cheque number is required for Bank Receive type.')
                    self.fields['recieved_cheque_no'].widget.attrs['class'] = 'parsley-error'
            return cleaned_data


class LoanReceivedForm(forms.ModelForm):
    class Meta:
        model = MoneyReceived
        fields = ('loan_info','total_amount', 'received_method', 
                'recieved_cheque_no', 'recieved_bank_name', 'check_attachment')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['loan_info'] = forms.ModelChoiceField(queryset=LoanInformation.objects.filter(amount__gt=0))
        self.fields['loan_info'].widget.attrs['class'] ='select2_single form-control'
        self.fields['loan_info'].label ='Select Loan Borrower'
        self.fields['received_method'].widget.attrs['class'] ='select2_single form-control'
        
        field_list = self.Meta.fields
        self.helper = FormHelper()
        # self.helper.form_method = 'get' # get or post
        self.helper.layout = Layout()
        # form fields layout.
        column_fields = []
        for field in field_list:
            column_fields.append(Column(f'{field}', css_class='form-group col-md-4 mb-0'))
        self.helper.layout.append(Row(
            *column_fields,
            css_class='row',
        ))
        # submit section btn
        self.helper.layout.append(Row(
            Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
            Column(Submit('submit', 'Update' if self.instance.pk else 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
            css_class='row'
        ))
    
    def clean(self):
            cleaned_data = super().clean()
            received_method = cleaned_data.get('received_method')
            loan_obj = cleaned_data.get('loan_info')
            total_amount = cleaned_data.get('total_amount')
            if total_amount > loan_obj.amount:
                self.add_error('total_amount', 'must be less than or equal loan amount.')
                self.fields['total_amount'].widget.attrs['class'] = 'parsley-error'

            if received_method == ReceivedOption.BANK:
                bank_name = cleaned_data.get('recieved_bank_name')
                cheque_no = cleaned_data.get('recieved_cheque_no')
                if not bank_name:
                    self.add_error('recieved_bank_name', 'Bank name is required for Bank Receive type.')
                    self.fields['recieved_bank_name'].widget.attrs['class'] = 'parsley-error'

                if not cheque_no:
                    self.add_error('recieved_cheque_no', 'Cheque number is required for Bank Receive type.')
                    self.fields['recieved_cheque_no'].widget.attrs['class'] = 'parsley-error'
            return cleaned_data