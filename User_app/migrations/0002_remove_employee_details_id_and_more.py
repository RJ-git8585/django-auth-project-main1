# Generated by Django 5.0.6 on 2024-05-25 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_details',
            name='id',
        ),
        migrations.RemoveField(
            model_name='employer_profile',
            name='employer_id',
        ),
        migrations.RemoveField(
            model_name='employer_profile',
            name='id',
        ),
        migrations.AddField(
            model_name='employee_details',
            name='employee_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer_profile',
            name='eemployer_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
