# Generated by Django 3.2.21 on 2024-03-06 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tender', '0005_moneyreceived_account_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyreceived',
            name='loan_type',
            field=models.CharField(blank=True, choices=[('pay', 'Pay'), ('receive', 'Received'), ('collection', 'Collection')], max_length=20, null=True),
        ),
    ]
