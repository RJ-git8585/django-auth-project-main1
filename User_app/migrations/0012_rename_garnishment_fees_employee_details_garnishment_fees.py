# Generated by Django 5.0.6 on 2024-05-18 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0011_rename_pay_employee_details_pay_cycle_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee_details',
            old_name='Garnishment_fees',
            new_name='garnishment_fees',
        ),
    ]
