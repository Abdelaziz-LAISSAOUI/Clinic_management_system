from django.shortcuts import render

# Create your views here.
def hello(request):
    return render(request,"base.html")

def doctor(request):
    return render(request,"pages/doctors.html")

def patient(request):
    return render(request,"pages/patients.html")

def appointment(request):
    return render(request,"pages/appointments.html")
