# Generated by Django 5.0.3 on 2024-03-28 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0005_doctor_profile_picture_patient_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
