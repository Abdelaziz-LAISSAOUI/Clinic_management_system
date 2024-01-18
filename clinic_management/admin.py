from django.contrib import admin
from .models import Doctor, Patient, Department, MedicalRecord, MedicalTest, TDate, TestMade, Appointment, Examination
# Register your models here.


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(MedicalRecord)
admin.site.register(MedicalTest)
admin.site.register(TDate)
admin.site.register(TestMade)
admin.site.register(Appointment)
admin.site.register(Examination)

