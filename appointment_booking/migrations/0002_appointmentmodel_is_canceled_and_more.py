# Generated by Django 5.1.5 on 2025-01-26 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointment_booking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointmentmodel",
            name="is_canceled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="appointmentmodel",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
    ]
