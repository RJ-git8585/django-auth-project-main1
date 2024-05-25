# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)

    # Remove the custom related_name and use the default ones
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)




# Employer_Profile details

class Employer_Profile(models.Model):
    eemployer_id = models.AutoField(primary_key=True)
    employer_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    federal_employer_identification_number = models.CharField(max_length=50)
    street_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    number_of_employer = models.IntegerField()
    department = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.employer_name

class Employee_Details(models.Model):
    employer_id=models.IntegerField(max_length=20)
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=50)
    garnishment_fees  = models.FloatField(max_length=50)
    net_pay=  models.FloatField()
    minimun_wages=  models.CharField(max_length=50)
    pay_cycle=models.FloatField()
    number_of_garnishment= models.CharField(max_length=50)
    location =models.CharField(max_length=50)
  
class Tax_details(models.Model):
    tax_id = models.AutoField(primary_key=True)
    employee_id=models.IntegerField(max_length=20)
    fedral_income_tax =models.FloatField()
    social_and_security =models.FloatField()
    medicare_tax= models.FloatField()
    state_taxes =models.FloatField()


class PDFFile(models.Model):
    name = models.CharField(max_length=255)
    data = models.BinaryField()

    def __str__(self):
        return self.name

