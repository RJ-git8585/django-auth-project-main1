# Generated by Django 5.0.6 on 2024-05-18 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0012_rename_garnishment_fees_employee_details_garnishment_fees'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee_details',
            old_name='minimunwages',
            new_name='minimun_wages',
        ),
    ]
