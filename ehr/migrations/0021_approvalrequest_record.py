# Generated by Django 5.0.3 on 2024-04-01 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0020_alter_ehr_symptoms'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalrequest',
            name='record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ehr.ehr'),
        ),
    ]