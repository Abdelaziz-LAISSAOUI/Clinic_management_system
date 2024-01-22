from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
# from .forms import UserCreationForm, LoginForm, DoctorLoginForm
from .forms import LoginForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import *

# instance = get_object_or_404(Object, name=name, job=job)
# redirect(reverse('test:output_page', args=instance))

from django.http import HttpResponseRedirect


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect']=self['Location']
    status_code = 200
# Create your views here.

@login_required(login_url="/login")
def hello(request):
    return render(request,"pages/home.html")

@login_required(login_url="/login")
def doctors(request):
    return render(request,"pages/doctors.html")

@login_required(login_url="/login")
def one_doctor(request, username):
    return render(request, "pages/doctor.html", {'username': username})

@login_required(login_url="/login")
def patient(request):
    return render(request,"pages/patients.html")

@login_required(login_url="/login")
def appointment(request):
    return render(request,"pages/appointments.html")


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)   
                return render(request, 'pages/home.html')
            else: 
                # messages.error(request, )
                return render(request, 'login.html', {'error_message': 'Invalid username or password. Please try again.'})
    else:
        if request.user.is_authenticated:

            print('reeeaaaaaaaaaaallly ')
            response =  render(request, 'pages/home.html')
            response['HX-Location']= 'home/'
            print(response)
            return redirect('index')

        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')



def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            # Redirect to the appropriate URL after successful login
            return redirect(reverse('doctors', args=[request.user.username]))
    else:
        form = DoctorLoginForm(request)

    return render(request, 'doctor-login.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

@require_POST
@login_required(login_url="/login")
def add_patient(request):
    username = request.POST.get('username')
    patient_phone = request.POST.get('patient_phone')

    # Assuming you have proper validation before creating a patient
    user = User.objects.create(username=username)
    patient = Patient.objects.create(user=user, patient_phone=patient_phone)

    # return JsonResponse({'status': 'success', 'message': 'Patient added successfully'})
    patients = Patient.objects.all()
    print('poooost')
    return render(request,'partials/patientList.html', {'patients': patients})


@login_required(login_url="/login")
def patient_list(request):
    patients = Patient.objects.all()
    print('hhhhhhhhhhhhhhhhhhhhhh')
    return render(request,'pages/patients.html', {'patients': patients})

