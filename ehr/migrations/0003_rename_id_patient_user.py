# Generated by Django 5.0.3 on 2024-03-28 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0002_rename_user_patient_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='id',
            new_name='user',
        ),
    ]