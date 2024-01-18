from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('doctors/', views.doctor, name='doctor'),
    path('patients/', views.patient, name='patient'),
    path('appointment/', views.appointment, name='appointment'),
]