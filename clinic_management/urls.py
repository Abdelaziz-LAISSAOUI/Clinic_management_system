from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='index'),
    path('doctors/<str:username>/', views.one_doctor, name='doctors'),  
    path('doctors/', views.doctors, name='doctors'),
    path('patients/', views.patient, name='patient'),
    path('appointment/', views.appointment, name='appointment'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('doctor-login/', views.doctor_login, name='doctor-login'),
]