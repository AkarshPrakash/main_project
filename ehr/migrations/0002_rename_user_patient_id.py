# Generated by Django 5.0.3 on 2024-03-28 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='user',
            new_name='id',
        ),
    ]
