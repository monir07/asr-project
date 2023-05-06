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


class SiteEngineerPayments(BaseModel):
    engineer = models.ForeignKey(ProjectSiteEngineer, on_delete=models.CASCADE, related_name='site_engineer_pay')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    paid_method = models.CharField(max_length=30, choices=PaidMethodOption.choices)



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


class RetensionMoney(BaseModel):
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
    is_withdraw = models.BooleanField(default=False)
    maturity_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)


class TenderPg(BaseModel):  # Pg = performance gurantee
    tender = models.OneToOneField(TenderProject, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_withdraw = models.BooleanField(default=False)
    maturity_date = models.DateField()  # Expire date of pg
    remarks = models.TextField(null=True, blank=True)


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


class DailyExpendiature(BaseModel):
    project = models.ForeignKey(TenderProject, on_delete=models.PROTECT, related_name='daily_expendiature')
    main_head = models.ForeignKey(CostMainHead, on_delete=models.PROTECT, related_name='main_head_expendiature')
    sub_head = models.ForeignKey(CostSubHead, on_delete=models.PROTECT, related_name='sub_head_expendiature', null=True, blank=True)

    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # total amount = paid + due.
    paid_method = models.CharField(max_length=30, choices=PaidMethodOption.choices)
    date = models.DateField(default=timezone.now)
    remarks = models.TextField(null=True, blank=True)

    bank_info = models.ForeignKey(BankInformation, on_delete=models.PROTECT, related_name='bank_expendiature', null=True, blank=True)
    cheque_no = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['-created_at',]

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in DailyExpendiature._meta.fields if field.name not in ignore_fields]