# Generated by Django 5.0.3 on 2024-04-01 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0021_approvalrequest_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='ehr',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ehr.doctor'),
        ),
    ]
