# Generated by Django 5.0.6 on 2024-05-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0016_alter_employer_profile_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer_profile',
            name='federal_employer_identification_number',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='employer_profile',
            name='location',
            field=models.CharField(max_length=40),
        ),
    ]