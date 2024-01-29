from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
# from .forms import UserCreationForm, LoginForm, DoctorLoginForm
from .forms import LoginForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.db.models import Count
from datetime import datetime
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
    print(request.user.username)
    return render(request,"pages/home.html")

@login_required(login_url="/login")
def doctors(request):
    return render(request,"pages/doctors.html")

@login_required(login_url="/login")
def one_doctor(request, username):
    return render(request, "pages/doctor.html", {'username': username})






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
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password. Please try again.'})
    else:# GET
        if request.user.is_authenticated:
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


# ---------------------APPOINTMENTS---------------------
@login_required(login_url="/login")
def appointment(request):
    appointments= Appointment.objects.all()
    print(appointments)
    return render(request,"pages/appointments.html", {"appointments": appointments})

@login_required(login_url="/login")
def cancel_appointment(request):
    patient=User.objects.get(username=request.GET.get('patient'))
    doctor=User.objects.get(username=request.GET.get('doctor'))
    date=request.GET.get('date')
    date_obj = datetime.strptime(date, '%b. %d, %Y')

    print(
        patient,
        doctor,
        date
    )

    # Format the datetime object into the required format
    formatted_date = date_obj.strftime('%Y-%m-%d')
    Appointment.objects.filter(doctor=Doctor.objects.get(user=doctor), patient=Patient.objects.get(user=patient), date=TDate.objects.get(date=formatted_date)).update(cancelation=True)

    
    appointments= Appointment.objects.all()
    print(appointments)
    return render(request,"partials/appointmentsList.html", {"appointments": appointments, 'toast_success': True})

@login_required(login_url="/login")
def confirm_appointment(request):
    # patient_username = request.GET.get('patient')
    # doctor_username = request.GET.get('doctor')
    # date_str = request.GET.get('date')

    # # Get the User instances
    # patient = User.objects.get(username=patient_username)
    # doctor = User.objects.get(username=doctor_username)

    # # Parse the date string into a datetime object
    # date_obj = datetime.strptime(date_str, '%b. %d, %Y')

    # # Format the datetime object into the required format
    # formatted_date = date_obj.strftime('%Y-%m-%d')

    # # Get the Appointment instance using get_object_or_404
    # appointment = Appointment.objects.get(
    #     doctor=doctor,
    #     patient=patient,
    #     date=TDate.objects.get(date=formatted_date)
    # )

    # # Confirm the appointment
    # appointment.confirmation = True
    # appointment.save()

    patient=User.objects.get(username=request.GET.get('patient'))
    doctor=User.objects.get(username=request.GET.get('doctor'))
    date=request.GET.get('date')
    print(patient, doctor, date)
    # # Parse the date string into a datetime object
    date_obj = datetime.strptime(date, '%b. %d, %Y')

    # # Format the datetime object into the required format
    formatted_date = date_obj.strftime('%Y-%m-%d')
    Appointment.objects.filter(doctor=Doctor.objects.get(user=doctor), patient=Patient.objects.get(user=patient), date=TDate.objects.get(date=formatted_date)).update(confirmation=True)
    
    print("FIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIINE")

    appointments= Appointment.objects.all()
    # print(appointments)
    return render(request,"partials/appointmentsList.html", {"appointments": appointments, 'toast_success':True})

@login_required(login_url="/login")
def add_appointment(request):
    department= request.POST.get('department')
    booking_choice= request.POST.get('date-vs-doctor')

    print(department, booking_choice)
    if booking_choice == 'doctor':
        doctors = Doctor.objects.filter(department_name=department)
        available_dates= None
    else: 
        # Retrieve all doctors of the department "d"
        doctors= None
        doctors_of_department_d = Doctor.objects.filter(department_name=department)

        # Filter dates where at least one doctor of the department "d" is available
        available_dates = TDate.objects.filter(
            appointments__doctor__in=doctors_of_department_d,
            appointments__cancelation=False
        ).annotate(num_doctors=Count('appointments__doctor')).filter(
            num_doctors__gt=0
        ).values('date') 


    return render(request,"partials/add_appointment.html", {'dates':available_dates, 'doctors': doctors})

@login_required(login_url="/login")
def book_apppointment(request):
    doctor = request.POST.get('doctor')
    print(doctor)
    user = User.objects.get(username=doctor)
    doctor = Doctor.objects.get(user=user)  
    
    # Assuming the doctor is available if the number of appointments on a date is less than 20
    available_dates = TDate.objects.filter(
        appointments__doctor=doctor,
        appointments__cancelation=False
    ).annotate(num_appointments=Count('appointments')).filter(
        num_appointments__lt=20
    ).values_list('date', flat=True)
    
    # Now 'available_date' contains the date on which the doctor "d" is available


    return render(request,"partials/choiceResult.html", {"result": available_dates, "dates":True})

@require_POST
@login_required(login_url="/login")
def create_appointment(request):
    print(request.POST.get('patient'))
    print(request.POST.get('doctor'))

   
    date = request.POST.get('date')
    patient_user = User.objects.get(username=request.POST.get('patient'))
    patient= Patient.objects.get(user=patient_user)

    try:
        tdate_obj, created = TDate.objects.get_or_create(date=date)
        doctor = User.objects.get(username=request.POST.get('doctor'))
        app = Appointment.objects.create(patient=patient, doctor=Doctor.objects.get(user=doctor), date=tdate_obj)    
    except Exception as e:
        print(str(e))
        patient = Patient.objects.get(user=User.objects.get(username=request.POST.get('patient')))
        appointments = Appointment.objects.filter(patient=patient)
        return render(request,'partials/appointmentsList.html', {'appointments': appointments, 'toast_failed': True })

    appointments = Appointment.objects.filter(patient=patient)
    

    return render(request,'partials/appointmentsList.html', {'appointments': appointments, 'toast_success': True })

@login_required(login_url="/login")
def appointment_list(request):
    return 


# ---------------------PATIENT---------------------

@login_required(login_url="/login")
def patient(request):
    return render(request,"pages/patients.html")

@require_POST
@login_required(login_url="/login")
def add_patient(request):
    username = request.POST.get('username').strip()
    patient_phone = request.POST.get('patient_phone').strip()

    # Assuming you have proper validation before creating a patient
    try:
        # user = User.objects.create(username=username)
        user = User(username=username)
        user.save()
        patient = Patient.objects.create(user=user, patient_phone=patient_phone)
        print(patient)
    except IntegrityError as e:
        if 'UNIQUE constraint failed: clinic_management_patient.patient_phone' in str(e):
            user.delete()
            patients = Patient.objects.all()
            return render(request,'partials/patientList.html', {'patients': patients, 'toast_error': True })
    except Exception as e:
        print(str(e))
        patients = Patient.objects.all()
        return render(request,'partials/patientList.html', {'patients': patients, 'toast_error': True })

    # return JsonResponse({'status': 'success', 'message': 'Patient added successfully'})
    patients = Patient.objects.all()
    return render(request,'partials/patientList.html', {'patients': patients, 'toast_success': True })

@login_required(login_url="/login")
def patient_list(request):
    patients = Patient.objects.all()
    return render(request,'pages/patients.html', {'patients': patients, 'newPatient': False})


@login_required(login_url="/login")
def one_patient(request, username):
    if request.method =="GET":
        try : 
            patient = Patient.objects.get(user__username=username)
            # Get all appointments for the patient
            appointments = Appointment.objects.filter(patient=patient)
        except: 
            return render(request, "pages/patientDetails.html", {'username': username, 'error_404': True})
        departements = Department.objects.all()
        return render(request, "pages/patientDetails.html", {'patient': patient, 'appointments':appointments, 'departements': departements, 'error_404':False}) 


@login_required(login_url="/login")
def update_patient(request):
    if request.method =="POST":
        username = request.POST.get('username')
        new_patient_phone = request.POST.get('patient_phone')
        try:
            user = User.objects.get(username=username)
            patient = Patient.objects.get(user=user)
            patient.patient_phone = new_patient_phone
            patient.save()
            return render(request, "partials/toast.html", {'toast_success': True})
        except :
            return render(request, "partials/toast.html", {'toast_failed': True})

@login_required(login_url="/login")
def delete_patient(request, username):
    if request.method == 'DELETE':
        user_to_delete = User.objects.get(username=username)

        # Retrieve the patient instance associated with the user
        patient_to_delete = Patient.objects.get(user=user_to_delete)

        # Delete the patient
        patient_to_delete.delete()

        # Optionally, delete the associated user if needed
        user_to_delete.delete()
        patients = Patient.objects.all()
        return render(request,'partials/patientList.html', {'patients': patients, 'toast_success ': True })