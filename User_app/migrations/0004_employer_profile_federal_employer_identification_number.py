# Generated by Django 5.0.4 on 2024-05-14 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0003_employer_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer_profile',
            name='federal_employer_identification_number',
            field=models.CharField(default=345, max_length=50),
            preserve_default=False,
        ),
    ]