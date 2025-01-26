import uuid
from typing import Optional

from appointment_booking.application.repositories.appointment_repository_interface import IAppointmentRepository
from appointment_booking.domain.entities import Appointment
from appointment_booking.infrastructure.models import AppointmentModel


class AppointmentRepository(IAppointmentRepository):
    """
    Concrete implementation of IAppointmentRepository using Django ORM.
    """

    def save(self, appointment: Appointment) -> Appointment:
        # Upsert logic: either create or update
        appointment_model, _ = AppointmentModel.objects.update_or_create(
            id=appointment.id,
            defaults={
                "slot_id": appointment.slot_id,
                "patient_id": appointment.patient_id,
                "patient_name": appointment.patient_name,
            },
        )

        # Synchronize domain entity with stored data
        appointment.id = appointment_model.id
        return appointment

    def find_by_slot_id(self, slot_id: uuid.UUID) -> Optional[Appointment]:
        try:
            app_model = AppointmentModel.objects.get(slot_id=slot_id)
            return Appointment(
                id=app_model.id,
                slot_id=app_model.slot_id,
                patient_id=app_model.patient_id,
                patient_name=app_model.patient_name,
                reserved_at=app_model.reserved_at,
            )
        except AppointmentModel.DoesNotExist:
            return None
