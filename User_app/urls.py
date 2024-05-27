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
    path('employee_details/<int:employee_id>/', views.EmployeeDetailsUpdateAPIView, name='employee_details'),
    path('<str:username>/', UserUpdateAPIView.as_view()),
    path('employer-profile/<int:profile_id>/',EmployerProfileEditView.as_view()),
    path('delete/<str:username>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('upload', views.upload_pdf, name='upload_pdf'),
    path('getemployeedetails/<int:employer_id>/', views.get_employee_by_employer_id, name='employee-by-employer-id'),
    path('getemployerdetails/<int:employer_id>/', views.get_employer_details, name='employer-detail-by-employer-id'),
    path('DashboardData',views.get_dashboard_data, name='iwo_dashboard'),
    path('IWO_Data',views.insert_iwo_detail, name='iwo_pdf_data'),



]



