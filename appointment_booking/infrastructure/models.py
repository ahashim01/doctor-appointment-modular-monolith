import uuid

from django.db import models
from django.utils.timezone import now


class AppointmentModel(models.Model):
    """
    Infrastructure representation of an Appointment.
    This mirrors the domain's Appointment entity.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slot_id = models.UUIDField()
    patient_id = models.UUIDField()
    patient_name = models.CharField(max_length=255)
    reserved_at = models.DateTimeField(default=now)
    is_completed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment({self.patient_name}, {self.slot_id})"
