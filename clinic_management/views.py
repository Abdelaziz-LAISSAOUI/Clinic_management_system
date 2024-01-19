from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm, DoctorLoginForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .decorators import login_required

# instance = get_object_or_404(Object, name=name, job=job)
# redirect(reverse('test:output_page', args=instance))


# Create your views here.

@login_required
def hello(request):
    return render(request,"pages/home.html")

@login_required
def doctors(request):
    return render(request,"pages/doctors.html")

@login_required
def one_doctor(request, username):
    return render(request, "pages/doctor.html", {'username': username})

@login_required
def patient(request):
    return render(request,"pages/patients.html")

@login_required
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