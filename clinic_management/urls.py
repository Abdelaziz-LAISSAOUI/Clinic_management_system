from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='index'),
    path('doctors/<str:username>/', views.one_doctor, name='doctors'),  
    path('doctors/', views.doctors, name='doctors'),
    # path('patients/', views.patient, name='patient'),
    path('appointment/', views.appointment, name='appointment'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('doctor-login/', views.doctor_login, name='doctor-login'),
    path('patients/', views.patient_list, name='patient_list'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('update_patient/',views.update_patient,name="update_patient"),
    path('appointementDlist/', views.appointementDlist, name="appointementDlist"),
    path('cancellation/', views.cancellation, name='cancellation'),
    path('create_examination/<int:patient_id>/', views.create_examination, name='create_examination'),
]