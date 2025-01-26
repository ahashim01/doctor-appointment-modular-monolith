# Generated by Django 5.1.5 on 2025-01-26 03:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AppointmentModel",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("slot_id", models.UUIDField()),
                ("patient_id", models.UUIDField()),
                ("patient_name", models.CharField(max_length=255)),
                ("reserved_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
