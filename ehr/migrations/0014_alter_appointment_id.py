# Generated by Django 5.0.3 on 2024-03-29 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0013_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
