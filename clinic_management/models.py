from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    doctor_phone = models.CharField(max_length=15, db_index=True)
    department_name = models.ForeignKey('Department', on_delete=models.SET_NULL, related_name='doctors', null=True)

    def __str__(self) -> str:
        return self.user.username

class Department(models.Model):
    department_name = models.CharField(max_length=50, primary_key=True)
    head = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='department_head', null=True, blank=True)

    def __str__(self) -> str:
        return self.department_name

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    patient_phone = models.CharField(max_length=15, db_index=True, unique=True)

    def __str__(self) -> str:
        return self.user.username
    
class MedicalRecord(models.Model):
    record_code = models.CharField(max_length=20, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records', db_index=True)

class MedicalTest(models.Model):
    test_name = models.CharField(max_length=50, primary_key=True)
    test_type = models.CharField(max_length=50)
    norm = models.CharField(max_length=50)

class TDate(models.Model):
    date = models.DateField(primary_key=True, db_index=True)

    def __str__(self)->str:
        return str(self.date)

class TestMade(models.Model):
    record_code = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='tests_made', db_index=True)
    test_name = models.ForeignKey(MedicalTest, on_delete=models.CASCADE, related_name='tests_made')

class Appointment(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True, related_name='appointments')
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.OneToOneField(TDate, on_delete=models.CASCADE, related_name='appointments')
    confirmation = models.BooleanField(default=False)
    cancelation = models.BooleanField(default=False)

class Examination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='examinations', db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='examinations')
    date = models.ForeignKey(TDate, on_delete=models.CASCADE, related_name='examinations')
    prescription = models.TextField()
    description = models.TextField()
