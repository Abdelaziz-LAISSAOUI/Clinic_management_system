# Generated by Django 5.0 on 2024-01-30 16:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalTest',
            fields=[
                ('test_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('test_type', models.CharField(max_length=50)),
                ('norm', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TDate',
            fields=[
                ('date', models.DateField(db_index=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_phone', models.CharField(db_index=True, max_length=15)),
                ('department_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to='clinic_management.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_head', to='clinic_management.doctor'),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_phone', models.CharField(db_index=True, max_length=15, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('record_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='clinic_management.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription', models.TextField()),
                ('description', models.TextField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examinations', to='clinic_management.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examinations', to='clinic_management.patient')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examinations', to='clinic_management.tdate')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation', models.BooleanField(default=False)),
                ('cancelation', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinic_management.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinic_management.patient')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinic_management.tdate')),
            ],
        ),
        migrations.CreateModel(
            name='TestMade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_made', to='clinic_management.medicalrecord')),
                ('test_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_made', to='clinic_management.medicaltest')),
            ],
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(fields=('patient', 'doctor', 'date'), name='unique_patient_doctor_date_combination'),
        ),
    ]
