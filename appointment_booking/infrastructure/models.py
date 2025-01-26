import uuid

from django.db import models


class AppointmentModel(models.Model):
    """
    Infrastructure representation of an Appointment.
    This mirrors the domain's Appointment entity.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slot_id = models.UUIDField()
    patient_id = models.UUIDField()
    patient_name = models.CharField(max_length=255)
    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment({self.patient_name}, {self.slot_id})"
