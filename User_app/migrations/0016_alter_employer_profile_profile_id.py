# Generated by Django 5.0.6 on 2024-05-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0015_employer_profile_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer_profile',
            name='profile_id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
