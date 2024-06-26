# Generated by Django 5.0.3 on 2024-04-12 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0023_alter_doctor_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='doctor_profile_pics'),
        ),
        migrations.AlterField(
            model_name='ehr',
            name='lab_result_image',
            field=models.ImageField(upload_to='ehr/lab_result/'),
        ),
        migrations.AlterField(
            model_name='ehr',
            name='xray_image',
            field=models.ImageField(upload_to='ehr/xray/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='patient_profile_pics'),
        ),
    ]
