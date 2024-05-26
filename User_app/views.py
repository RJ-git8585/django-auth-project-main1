from rest_framework import status
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser,Profile , Employer_Profile,Employee_Details,Tax_details
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login 
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
import json
from rest_framework.generics import DestroyAPIView
from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserUpdateSerializer,EmployerProfileSerializer ,GetEmployeeDetailsSerializer,GetEmployerDetailsSerializer
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import PDFUploadForm
from .models import PDFFile
from django.db import transaction
from rest_framework.decorators import api_view


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON', 'status_code':status.HTTP_400_BAD_REQUEST})

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'success': False, 'message': 'email and password are required','status_code':status.HTTP_400_BAD_REQUEST})

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid credentials','status_code':status.HTTP_400_BAD_REQUEST})

        if check_password(password, user.password):
            auth_login(request, user) 
            user_data = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
            }
            refresh = RefreshToken.for_user(user)
            response_data = {
                'success': True,
                'message': 'Login successful',
                'user_data': user_data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'code': status.HTTP_200_OK,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials','status_code':status.HTTP_400_BAD_REQUEST})
    else:
        return JsonResponse({'message': 'Please use POST method for login','status_code':status.HTTP_400_BAD_REQUEST})



# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             first_name = data.get('first_name')
#             last_name = data.get('last_name')
#             username = data.get('username')
#             email = data.get('email')
#             gender = data.get('gender')
#             contact_number = data.get('contact_number')
#             password1 = data.get('password1')
#             password2 = data.get('password2')
#             # first_name = request.POST.get('first_name')
#             # last_name = request.POST.get('last_name')
#             # username = request.POST.get('username')
#             # email = request.POST.get('email')
#             # gender = request.POST.get('gender')
#             # contact_number = request.POST.get('contact_number')
#             # password1 = request.POST.get('password1')
#             # password2 = request.POST.get('password2')
#             if password1 == password2:
#                 User = get_user_model()
#                 if User.objects.filter(username=username).exists():
#                     return JsonResponse({'error': 'Username Taken'}, status=status.HTTP_400_BAD_REQUEST)
#                 elif User.objects.filter(email=email).exists():
#                     return JsonResponse({'error': 'Email Taken'}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, gender=gender, contact_number=contact_number, username=username, password=password1)
#                     user.save()
#                     return JsonResponse({'message': 'Successfully Registered'})
#             else:
#                 return JsonResponse({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return render(request, 'register.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON','status_code':status.HTTP_400_BAD_REQUEST})

        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if not all([name, username, email, password1, password2]):
            return JsonResponse({'error': 'All fields are required', 'status_code':status.HTTP_400_BAD_REQUEST})

        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match', 'status_code':status.HTTP_400_BAD_REQUEST})

        if not (len(password1) >= 8 and any(c.isupper() for c in password1) and any(c.islower() for c in password1) and any(c.isdigit() for c in password1) and any(c in '!@#$%^&*()_+' for c in password1)):
            return JsonResponse({'error': 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character', 'status_code':status.HTTP_400_BAD_REQUEST})

        User = get_user_model()
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username taken', 'status_code':status.HTTP_400_BAD_REQUEST})
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email taken', 'status_code' :status.HTTP_400_BAD_REQUEST})

        try:
            user = CustomUser.objects.create_user(name=name, email=email, username=username, password=password1)
            user.save()
            return JsonResponse({'message': 'Successfully registered', 'status_code':status.HTTP_201_CREATED})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR})
    else:
        return JsonResponse({'message': 'Please use POST method for registor', 'status_code':status.HTTP_400_BAD_REQUEST})



#new


def dashboard(request):
    return render( 'dashboard.html')

def logout(request):
    logout(request)
    return redirect('login')




@csrf_exempt
def EmployerProfile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['employer_name', 'street_name', 'federal_employer_identification_number', 'city', 'state', 'country', 'zipcode', 'email', 'number_of_employer', 'department', 'location']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            if missing_fields:
                return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}','status_code':status.HTTP_400_BAD_REQUEST})
            
            # Validate length of federal_employer_identification_number
            if len(str(data['federal_employer_identification_number'])) != 9:
                return JsonResponse({'error': 'Federal Employer Identification Number must be exactly 9 characters long', 'status_code':status.HTTP_400_BAD_REQUEST})
            
            if Employer_Profile.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'Email already registered', 'status_code':status.HTTP_400_BAD_REQUEST})
            
            user = Employer_Profile.objects.create(**data)
            return JsonResponse({'message': 'Employer Detail Successfully Registered'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    else:
        return JsonResponse({'message': 'Please use POST method','status_code':status.HTTP_400_BAD_REQUEST})


@csrf_exempt
def EmployeeDetails(request):
    if request.method == 'POST' :
        try:
            data = json.loads(request.body)
            required_fields = ['employee_name', 'garnishment_fees', 'net_pay', 'minimun_wages', 'pay_cycle', 'number_of_garnishment', 'location']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            
            if missing_fields:
                return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}', 'status_code':status.HTTP_400_BAD_REQUEST})
            
            # if Employee_Details.objects.filter(employee_id=data['employee_id']).exists():
            #     return JsonResponse({'error': 'Employee ID already exists', 'status_code':status.HTTP_400_BAD_REQUEST})
            
            Employee_Details.objects.create(**data)
            return JsonResponse({'message': 'Employee Details Successfully Registered', 'status_code':status.HTTP_201_CREATED})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format','status_code':status.HTTP_400_BAD_REQUEST})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'message': 'Please use POST method ', 'status_code':status.HTTP_400_BAD_REQUEST})
    
@csrf_exempt
def TaxDetails(request):
    if request.method == 'POST' :
        try:
            data = json.loads(request.body)
            required_fields = ['employee_id','fedral_income_tax','social_and_security','medicare_tax','state_taxes']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            
            if missing_fields:
                return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}', 'status_code':status.HTTP_400_BAD_REQUEST})
            
            Tax_details.objects.create(**data)
            return JsonResponse({'message': 'Tax Details Successfully Registered', 'status_code':status.HTTP_201_CREATED})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format','status_code':status.HTTP_400_BAD_REQUEST})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'message': 'Please use POST method ', 'status_code':status.HTTP_400_BAD_REQUEST})
    
    
#for Updating the Employer Profile data

class EmployerProfileEditView(RetrieveUpdateAPIView):
    queryset = Employer_Profile.objects.all()
    serializer_class = EmployerProfileSerializer
    lookup_field = 'employer_id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # Check for missing fields
        required_fields = ['employer_name', 'street_name', 'federal_employer_identification_number', 'city', 'state', 'country', 'zipcode', 'email', 'number_of_employer', 'department', 'location']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}', 'status_code':status.HTTP_400_BAD_REQUEST})

        # Validate length of federal_employer_identification_number
        if 'federal_employer_identification_number' in data and len(str(data['federal_employer_identification_number'])) != 9:
            return JsonResponse({'error': 'Federal Employer Identification Number must be exactly 9 characters long', 'status_code':status.HTTP_400_BAD_REQUEST})

        # Validate email if it's being updated
        if 'email' in data and Employer_Profile.objects.filter(email=data['email']).exclude(profile_id=instance.profile_id).exists():
            return JsonResponse({'error': 'Email already registered', 'status_code':status.HTTP_400_BAD_REQUEST})

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            'success': True,
            'message': 'Data Updated successfully',
            'Code': status.HTTP_200_OK
        }
        return JsonResponse(response_data)




#For updating the Registor details

class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'username'  
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
                'success': True,
                'message': 'Data Updated successfully',
                'Code': status.HTTP_200_OK}
        return JsonResponse(response_data)
    


# For Deleting the Employer Profile data

class UserDeleteAPIView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'username' 
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
                'success': True,
                'message': 'Data Deleted successfully',
                'Code': status.HTTP_204_NO_CONTENT}
        return JsonResponse(response_data)
    

#PDF upload view

@transaction.atomic
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            pdf_name = pdf_file.name
            pdf_data = pdf_file.read()
            
            # Store PDF file data in the database
            pdf_record = PDFFile(name=pdf_name, data=pdf_data)
            pdf_record.save()

            return HttpResponse("File uploaded successfully.")
    else:
        form = PDFUploadForm()

    return render(request, 'upload_pdf.html', {'form': form})



#Get Employer Details on the bases of Employer_ID

@api_view(['GET'])
def get_employee_by_employer_id(request, employer_id):
    employees=Employee_Details.objects.filter(employer_id=employer_id)
    if employees.exists():
        try:
            serializer = GetEmployeeDetailsSerializer(employees, many=True)
            response_data = {
                    'success': True,
                    'message': 'Data Get successfully',
                    'Code': status.HTTP_204_NO_CONTENT}
            response_data['data'] = serializer.data
            return JsonResponse(response_data)


        except Employee_Details.DoesNotExist:
            return JsonResponse({'message': 'Data not found', 'status_code':status.HTTP_404_NOT_FOUND})
    else:
        return JsonResponse({'message': 'Employer ID not found', 'status':status.HTTP_404_NOT_FOUND})



#Get Employer Details from employer ID

@api_view(['GET'])
def get_employer_details(request, employer_id):
    employees=Employer_Profile.objects.filter(employer_id=employer_id)
    if employees.exists():
        try:
            serializer = GetEmployerDetailsSerializer(employees, many=True)
            response_data = {
                    'success': True,
                    'message': 'Data Get successfully',
                    'Code': status.HTTP_204_NO_CONTENT}
            response_data['data'] = serializer.data
            return JsonResponse(response_data)


        except Employer_Profile.DoesNotExist:
            return JsonResponse({'message': 'Data not found', 'status_code':status.HTTP_404_NOT_FOUND})
    else:
        return JsonResponse({'message': 'Employer ID not found', 'status':status.HTTP_404_NOT_FOUND})