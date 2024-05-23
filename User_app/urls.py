from django.urls import path
from . import views
from .views import UserUpdateAPIView,EmployerProfileEditView,UserDeleteAPIView,TaxDetails
from django.urls import include, path
from rest_framework import routers


urlpatterns = [
    path("register", views.register, name="register"),
    path("login",views.login, name="login"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout',views.logout,name='logout'),
    path('employer-profile/', views.EmployerProfile, name='employer_profile'),
    path('TaxDetails/', views.TaxDetails, name='Tax_details'),
    path('employee_details/', views.EmployeeDetails, name='employee_details'),
    path('<str:username>/', UserUpdateAPIView.as_view()),
    path('employer-profile/<int:profile_id>/',EmployerProfileEditView.as_view()),
    path('delete/<str:username>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('upload', views.upload_pdf, name='upload_pdf'),


]



