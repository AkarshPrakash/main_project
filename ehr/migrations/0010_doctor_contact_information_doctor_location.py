# Generated by Django 5.0.3 on 2024-03-29 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0009_remove_doctor_user_remove_patient_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='contact_information',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
