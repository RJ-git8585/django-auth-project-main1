# Generated by Django 5.0.6 on 2024-05-26 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0003_iwo_details_pdf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iwo_details_pdf',
            name='IWO_Status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='iwo_details_pdf',
            name='employee_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='iwo_details_pdf',
            name='employer_id',
            field=models.IntegerField(),
        ),
    ]
