# Generated by Django 5.0 on 2024-01-19 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_management', '0002_alter_department_head'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_head', to='clinic_management.doctor'),
        ),
    ]
