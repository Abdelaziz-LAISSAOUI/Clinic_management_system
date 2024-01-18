from django.db import models

# Create your models here.

class Doctor(models.Model):
    doctor_code = models.CharField(max_length=20, primary_key=True)
    doctor_first_name = models.CharField(max_length=50)
    doctor_last_name = models.CharField(max_length=50)
    doctor_phone = models.CharField(max_length=15, db_index=True)
    doctor_email = models.EmailField(db_index=True)
    department_name = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='doctors')

class Department(models.Model):
    department_name = models.CharField(max_length=50, primary_key=True)
    head = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='department_head')

class Patient(models.Model):
    patient_code = models.CharField(max_length=20, primary_key=True)
    patient_first_name = models.CharField(max_length=50)
    patient_last_name = models.CharField(max_length=50)
    patient_phone = models.CharField(max_length=15, db_index=True)
    patient_email = models.EmailField(db_index=True)

class MedicalRecord(models.Model):
    record_code = models.CharField(max_length=20, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records', db_index=True)

class MedicalTest(models.Model):
    test_name = models.CharField(max_length=50, primary_key=True)
    test_type = models.CharField(max_length=50)
    norm = models.CharField(max_length=50)

class TDate(models.Model):
    date = models.DateField(primary_key=True, db_index=True)

class TestMade(models.Model):
    record_code = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='tests_made', db_index=True)
    test_name = models.ForeignKey(MedicalTest, on_delete=models.CASCADE, related_name='tests_made')

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.ForeignKey(TDate, on_delete=models.CASCADE, related_name='appointments')
    confirmation = models.BooleanField(default=False)

class Examination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='examinations', db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='examinations')
    date = models.ForeignKey(TDate, on_delete=models.CASCADE, related_name='examinations')
    prescription = models.TextField()
    description = models.TextField()
