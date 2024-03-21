from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from ..models import (MoneyReceived, ReceivedOption, TenderPg, SecurityMoney, LoanInformation)


class SecurityReceivedForm(forms.ModelForm):
    class Meta:
        model = MoneyReceived
        fields = ('tender_security','total_amount', 'received_method', 
                'recieved_cheque_no', 'recieved_bank_name', 'check_attachment', 'bank_info', 'cash_balance')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tender_security'] = forms.ModelChoiceField(queryset=SecurityMoney.objects.filter(is_withdraw=False))
        self.fields['tender_security'].widget.attrs['class'] ='select2_single form-control'
        self.fields['tender_security'].label ='Select Tender Project'
        self.fields['bank_info'].label ='Select deposit bank'
        self.fields['cash_balance'].label ='Select Cash balance'
        self.fields['received_method'].widget.attrs['class'] ='select2_single form-control'
        self.fields['bank_info'].widget.attrs['class'] ='select2_single form-control'
        self.fields['cash_balance'].widget.attrs['class'] ='select2_single form-control'
        
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
            bank_info = cleaned_data.get('bank_info')
            bank_name = cleaned_data.get('recieved_bank_name')
            cheque_no = cleaned_data.get('recieved_cheque_no')
            if not bank_info:
                self.add_error('bank_info', 'Deposit Bank is required for Bank Receive type.')
                self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'
            if not bank_name:
                self.add_error('recieved_bank_name', 'Bank name is required for Bank Receive type.')
                self.fields['recieved_bank_name'].widget.attrs['class'] = 'parsley-error'

            if not cheque_no:
                self.add_error('recieved_cheque_no', 'Cheque number is required for Bank Receive type.')
                self.fields['recieved_cheque_no'].widget.attrs['class'] = 'parsley-error'
        elif received_method == ReceivedOption.CASH:
            cash_obj = cleaned_data.get('cash_balance')
            if not cash_obj:
                self.add_error('cash_balance', 'Cash Balance is required for Cash Receive type.')
                self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
        return cleaned_data


class PgReceivedForm(forms.ModelForm):
    class Meta:
        model = MoneyReceived
        fields = ('performance_gurantee', 'total_amount', 'received_method', 
                'recieved_cheque_no', 'recieved_bank_name', 'check_attachment', 'bank_info', 'cash_balance')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['performance_gurantee'] = forms.ModelChoiceField(queryset=TenderPg.objects.filter(is_withdraw=False))
        self.fields['performance_gurantee'].widget.attrs['class'] ='select2_single form-control'
        self.fields['performance_gurantee'].label ='Select Tender Project'
        self.fields['bank_info'].label ='Select Deposit Bank'
        self.fields['cash_balance'].label ='Select cash balance'
        self.fields['bank_info'].widget.attrs['class'] ='select2_single form-control'
        self.fields['received_method'].widget.attrs['class'] ='select2_single form-control'
        self.fields['cash_balance'].widget.attrs['class'] ='select2_single form-control'
        
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
            bank_info = cleaned_data.get('bank_info')
            bank_name = cleaned_data.get('recieved_bank_name')
            cheque_no = cleaned_data.get('recieved_cheque_no')
            if not bank_info:
                self.add_error('bank_info', 'Deposit Bank is required for Bank Receive type.')
                self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'
            
            if not bank_name:
                self.add_error('recieved_bank_name', 'Bank name is required for Bank Receive type.')
                self.fields['recieved_bank_name'].widget.attrs['class'] = 'parsley-error'

            if not cheque_no:
                self.add_error('recieved_cheque_no', 'Cheque number is required for Bank Receive type.')
                self.fields['recieved_cheque_no'].widget.attrs['class'] = 'parsley-error'
        elif received_method == ReceivedOption.CASH:
            cash_obj = cleaned_data.get('cash_balance')
            if not cash_obj:
                self.add_error('cash_balance', 'Cash Balance is required for Cash Receive type.')
                self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
        return cleaned_data


class LoanCollectionForm(forms.ModelForm):
    class Meta:
        model = MoneyReceived
        fields = ('loan_info','total_amount', 'received_method', 'account_no',
                'recieved_cheque_no', 'recieved_bank_name', 'bank_info', 'cash_balance', 'check_attachment')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['loan_info'] = forms.ModelChoiceField(queryset=LoanInformation.objects.filter(amount__gt=0))
        self.fields['loan_info'].widget.attrs['class'] ='select2_single form-control'
        self.fields['loan_info'].label ='Select Loan Borrower'
        self.fields['bank_info'].label ='Select deposit bank'
        self.fields['cash_balance'].label ='Select cash balance'
        self.fields['account_no'].label ='Received Account No'
        self.fields['received_method'].widget.attrs['class'] ='select2_single form-control'
        self.fields['bank_info'].widget.attrs['class'] ='select2_single form-control'
        self.fields['cash_balance'].widget.attrs['class'] ='select2_single form-control'
        
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
        bank_info = cleaned_data.get('bank_info')
        loan_obj = cleaned_data.get('loan_info')
        total_amount = cleaned_data.get('total_amount')
        if total_amount > loan_obj.amount:
            self.add_error('total_amount', 'must be less than or equal loan amount.')
            self.fields['total_amount'].widget.attrs['class'] = 'parsley-error'

        if received_method == ReceivedOption.BANK:
            bank_name = cleaned_data.get('recieved_bank_name')
            cheque_no = cleaned_data.get('recieved_cheque_no')
            
            if not bank_info:
                self.add_error('bank_info', 'Deposit Bank is required for Bank Receive type.')
                self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'
            if not bank_name:
                self.add_error('recieved_bank_name', 'Bank name is required for Bank Receive type.')
                self.fields['recieved_bank_name'].widget.attrs['class'] = 'parsley-error'

            if not cheque_no:
                self.add_error('recieved_cheque_no', 'Cheque number is required for Bank Receive type.')
                self.fields['recieved_cheque_no'].widget.attrs['class'] = 'parsley-error'
        elif received_method == ReceivedOption.CASH:
            cash_obj = cleaned_data.get('cash_balance')
            if not cash_obj:
                self.add_error('cash_balance', 'Cash Balance is required for Cash Receive type.')
                self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
        return cleaned_data


class BillReceivedForm(forms.ModelForm):
    retension_receive_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), 
                            label="Retention Receive Date", help_text="Expected date to receive retention money")
    class Meta:
        model = MoneyReceived
        fields = ('project', 'received_method', 'bank_info', 'recieved_cheque_no', 
                  'recieved_bank_name', 'check_attachment', 'cash_balance', 
                  'total_amount','deduction_of_vat', 'deduction_of_tax', 
                  'deduction_of_ld', 'misc_deduction', 'security_money', 'received_amount',)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['class'] ='select2_single form-control'
        self.fields['project'].label ='Select project'
        self.fields['total_amount'].label ='Total Received Amount'
        self.fields['bank_info'].label ='Select deposit bank'
        self.fields['cash_balance'].label ='Select cash balance'
        self.fields['received_method'].widget.attrs['class'] ='select2_single form-control'
        self.fields['bank_info'].widget.attrs['class'] ='select2_single form-control'
        self.fields['cash_balance'].widget.attrs['class'] ='select2_single form-control'
        
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
            bank_info = cleaned_data.get('bank_info')
            bank_name = cleaned_data.get('recieved_bank_name')
            cheque_no = cleaned_data.get('recieved_cheque_no')
            
            if not bank_info:
                self.add_error('bank_info', 'Deposit Bank is required for Bank Receive type.')
                self.fields['bank_info'].widget.attrs['class'] = 'select2_single form-control parsley-error'
            if not bank_name:
                self.add_error('recieved_bank_name', 'Bank name is required for Bank Receive type.')
                self.fields['recieved_bank_name'].widget.attrs['class'] = 'parsley-error'

            if not cheque_no:
                self.add_error('recieved_cheque_no', 'Cheque number is required for Bank Receive type.')
                self.fields['recieved_cheque_no'].widget.attrs['class'] = 'parsley-error'
        elif received_method == ReceivedOption.CASH:
            cash_obj = cleaned_data.get('cash_balance')
            if not cash_obj:
                self.add_error('cash_balance', 'Cash Balance is required for Cash Receive type.')
                self.fields['cash_balance'].widget.attrs['class'] = 'select2_single form-control parsley-error'
        return cleaned_data