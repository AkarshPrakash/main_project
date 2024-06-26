# Generated by Django 5.0.3 on 2024-03-28 17:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ehr', '0006_remove_patient_user_delete_doctor_delete_patient'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('specification', models.CharField(max_length=100)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='doctor_profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('location', models.CharField(max_length=100)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='patient_profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
