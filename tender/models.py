import os
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify 
User = get_user_model()

ignore_fields = ['id', 'project_complete', 'created_at', 'updated_at', 'created_by', 'updated_by', 'basemodel_ptr']


class PaidMethodOption(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE """
    CASH = 'cash', 'Cash'
    BANK = 'bank', 'Bank'
    DUE = 'due', 'Due'

class ReceivedOption(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE """
    CASH = 'cash', 'Cash'
    BANK = 'bank', 'Bank'

class ExpendiatureOption(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE """
    CREDIT = 'credit', 'Credit'
    DEBIT = 'debit', 'Debit'


class LoanOption(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE """
    PAY = 'pay', 'Pay'
    RECEIVE = 'receive', 'Received'
    COLLECTION = 'collection', 'Collection'

class SecurityOption(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE """
    CASH = 'cash', 'Cash'
    BANK = 'bank', 'Bank'
    PAY_ORDER = 'pay_order', 'Pay Order'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='updated_%(class)ss', null=True, blank=True)


class ProjectSiteEngineer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='site_engineer')
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.user}'


class TenderProject(BaseModel):
    engineer = models.ForeignKey(ProjectSiteEngineer, on_delete=models.PROTECT, related_name="tender_project")
    project_name = models.CharField(max_length=200)
    short_description = models.TextField(null=True, blank=True)

    job_no = models.CharField(max_length=200, null=True, blank=True)
    project_location = models.CharField(max_length=200)
    procuring_entity_name = models.CharField(max_length=200)
    contact_value = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_infrastructure = models.PositiveIntegerField()
    infrastructure_description = models.TextField()

    project_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_name}"

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in TenderProject._meta.fields if field.name not in ignore_fields]


class RetensionMoney(BaseModel):  # as like security  money.
    tender = models.ForeignKey(TenderProject, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_withdraw = models.BooleanField(default=False)
    maturity_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in RetensionMoney._meta.fields if field.name not in ignore_fields]


class SecurityMoney(BaseModel):
    tender = models.OneToOneField(TenderProject, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    security_type = models.CharField(max_length=20, choices=SecurityOption.choices)
    is_withdraw = models.BooleanField(default=False)
    maturity_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    bank_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tender.project_name
    class Meta:
        ordering = ('-created_at',)


class TenderPg(BaseModel):  # Pg = performance gurantee
    tender = models.OneToOneField(TenderProject, on_delete=models.CASCADE)
    pg_type = models.CharField(max_length=30, choices=SecurityOption.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_withdraw = models.BooleanField(default=False)
    maturity_date = models.DateField()  # Expire date of pg
    remarks = models.TextField(null=True, blank=True)
    bank_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tender.project_name
    class Meta:
        ordering = ('-created_at',)


class CostMainHead(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(default="", null=False)
    balance = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.name}"

    def get_main_head(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class CostSubHead(models.Model):
    main_head = models.ForeignKey(CostMainHead, on_delete=models.CASCADE, related_name='sub_head')
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="", null=False)
    balance = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.name}"

    def get_sub_head(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)        


class BankInformation(BaseModel):
    account_no = models.CharField(max_length=150, unique=True)
    bank_name = models.CharField(max_length=150)
    branch_name = models.CharField(max_length=150)
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.account_no} : {self.bank_name}"

class CashBalance(BaseModel):
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.balance}"

class LoanInformation(BaseModel):
    borrower_name = models.CharField(max_length=150)
    payment_option = models.CharField(max_length=30, choices=PaidMethodOption.choices)
    # loan_type = models.CharField(max_length=20, choices=LoanOption.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.TextField(null=True, blank=True)
    
    # if loan type is banking system then fill bank and cheque no.
    account_no = models.CharField(max_length=40, null=True, blank=True)
    bank_name = models.CharField(max_length=80, null=True, blank=True)
    cheque_no = models.CharField(max_length=50, null=True, blank=True)
    

    def __str__(self):
        return f"{self.borrower_name} : {self.amount}"


class DailyExpendiature(BaseModel):
    project = models.ForeignKey(TenderProject, on_delete=models.PROTECT, related_name='project_expendiature', null=True, blank=True)
    site_engier = models.ForeignKey(ProjectSiteEngineer, on_delete=models.PROTECT, related_name='site_engier_expendiature', null=True, blank=True)
    # office_entry = blank ture
    security_money = models.ForeignKey(SecurityMoney, on_delete=models.PROTECT, related_name='security_money_expendiature', null=True, blank=True)
    performance_gurantee = models.ForeignKey(TenderPg, on_delete=models.PROTECT, related_name='pg_expendiature', null=True, blank=True)
    loan_info = models.ForeignKey(LoanInformation, on_delete=models.PROTECT, related_name='loan_expendiature', null=True, blank=True)
    cash_balance = models.ForeignKey(CashBalance, on_delete=models.PROTECT, related_name='cash_expendiature', null=True, blank=True)
    
    main_head = models.ForeignKey(CostMainHead, on_delete=models.PROTECT, related_name='main_head_expendiature', null=True, blank=True)
    sub_head = models.ForeignKey(CostSubHead, on_delete=models.PROTECT, related_name='sub_head_expendiature', null=True, blank=True)

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # total amount = paid + due.
    """ if paid method is due then it does not increse cash balance or bank balance """
    paid_method = models.CharField(max_length=30, choices=PaidMethodOption.choices)
    # expendiature_type = models.CharField(max_length=30, choices=ExpendiatureOption.choices)
    date = models.DateField(default=timezone.now)
    remarks = models.TextField(null=True, blank=True)
    """ if paid method is bank then it does decrese bank balance """
    bank_info = models.ForeignKey(BankInformation, on_delete=models.PROTECT, related_name='bank_expendiature', null=True, blank=True)
    cheque_no = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['-created_at',]

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in DailyExpendiature._meta.fields if field.name not in ignore_fields]
    

class MoneyReceived(BaseModel):
    project = models.ForeignKey(TenderProject, on_delete=models.PROTECT, related_name='project_money_received', blank=True, null=True)
    retention_money = models.ForeignKey(RetensionMoney, on_delete=models.PROTECT, blank=True, null=True)  # as like security  money.
    bank_info = models.ForeignKey(BankInformation, on_delete=models.PROTECT, related_name='bank_money_received', blank=True, null=True)

    tender_security = models.ForeignKey(SecurityMoney, on_delete=models.PROTECT, related_name='security_money_received', null=True, blank=True)
    performance_gurantee = models.ForeignKey(TenderPg, on_delete=models.PROTECT, related_name='pg_received', null=True, blank=True)
    loan_info = models.ForeignKey(LoanInformation, on_delete=models.PROTECT, related_name='loan_received', null=True, blank=True)
    loan_type = models.CharField(max_length=20, choices=LoanOption.choices,  null=True, blank=True)
    cash_balance = models.ForeignKey(CashBalance, on_delete=models.PROTECT, related_name='cash_received', null=True, blank=True)
    
    """ if received method is bank then it does increse bank balance and need revceived cheque and bank name. """
    received_method = models.CharField(max_length=30, choices=ReceivedOption.choices)
    total_amount = models.DecimalField(max_digits=13, decimal_places=2)
    recieved_cheque_no = models.CharField(max_length=150, null=True, blank=True)
    recieved_bank_name = models.CharField(max_length=150, null=True, blank=True)
    account_no = models.CharField(max_length=40, null=True, blank=True)
    check_attachment = models.FileField(upload_to='check_attachment/', blank=True, null=True)
    
    deduction_of_vat = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    deduction_of_tax = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    deduction_of_ld = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    misc_deduction = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    security_money = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)  # retension money amount.
    
    received_amount = models.DecimalField(max_digits=13, decimal_places=2)  # total_amount - all_decution

