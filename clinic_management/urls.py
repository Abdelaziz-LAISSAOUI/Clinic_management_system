from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('doctor-login/', views.doctor_login, name='doctor-login'),
    
    path('doctors/<str:username>/', views.one_doctor, name='doctors'),  
    path('doctors/', views.doctors, name='doctors'),
    
    path('appointment/', views.appointment, name='appointment'),
    path('confirm-appointment/', views.confirm_appointment, name='confirm_appointment'),
    path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('book_apppointment/', views.book_apppointment, name='book_apppointment'), 


    path('patients/<str:username>/', views.one_patient, name='doctors'),  
    path('patients/', views.patient_list, name='patient_list'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('update_patient/', views.update_patient, name='update_patient'),
    path('delete_patient/<str:username>/', views.delete_patient, name='delete_patient'),
]