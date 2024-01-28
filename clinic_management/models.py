from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.forms import ValidationError
from django.utils import timezone

# Create your models here.
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    doctor_phone = models.CharField(max_length=15, db_index=True)
    department_name = models.ForeignKey('Department', on_delete=models.SET_NULL, related_name='doctors', null=True)
    speciality  = models.CharField(max_length=200,default='')

    def __str__(self) -> str:
        return self.user.get_full_name()

class Department(models.Model):
    department_name = models.CharField(max_length=50, primary_key=True)
    head = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='department_head', null=True, blank=True)

    def __str__(self) -> str:
        return self.department_name

class TDate(models.Model):
    date = models.DateField(primary_key=True, db_index=True)

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    patient_phone = models.CharField(max_length=15, db_index=True)
    name = models.CharField(max_length=100, default="John")  
    surname = models.CharField(max_length=100, default="Doe") 
    birthDate = models.ForeignKey(TDate, on_delete=models.CASCADE, related_name='patient')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,default='Male')

    def validate_birthdate(value):
        today = timezone.now().date()
        if value > today:
            raise ValidationError("Birth date must be before today.")
        
    def save(self, *args, **kwargs):
        # Set default birthDate to today if not provided
        if not self.birthDate_id:
            self.birthDate_id = timezone.now().date()

        super().save(*args, **kwargs)

    birthDate.validators.append(validate_birthdate)
    birthDate.default = timezone.now().date()

    def __str__(self) -> str:
        return self.user.username
    
class MedicalRecord(models.Model):
    record_code = models.CharField(max_length=20, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records', db_index=True)

class MedicalTest(models.Model):
    test_name = models.CharField(max_length=50, primary_key=True)
    test_type = models.CharField(max_length=50)
    norm = models.CharField(max_length=50)

class TestMade(models.Model):
    record_code = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='tests_made', db_index=True)
    test_name = models.ForeignKey(MedicalTest, on_delete=models.CASCADE, related_name='tests_made')

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.ForeignKey(TDate, on_delete=models.CASCADE, related_name='appointments')
    confirmation = models.BooleanField(default=False)
    canelation = models.BooleanField(default=False)

class Examination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='examinations', db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='examinations')
    date = models.ForeignKey(TDate, on_delete=models.CASCADE, related_name='examinations')
    prescription = models.TextField()
    description = models.TextField()
