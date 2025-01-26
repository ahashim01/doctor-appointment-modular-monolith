import uuid
from datetime import datetime
from typing import List, Optional

from appointment_booking.infrastructure.models import AppointmentModel
from appointment_management.ports.outbound.appointment_repository_port import AppointmentRecord, IAppointmentRepository


class AppointmentRepositoryAdapter(IAppointmentRepository):
    """
    Concrete implementation of IAppointmentRepository using Django ORM
    to access the appointments.
    """

    def find_by_id(self, appointment_id: uuid.UUID) -> Optional[AppointmentRecord]:
        try:
            app_model = AppointmentModel.objects.get(id=appointment_id)
            return self._to_record(app_model)
        except AppointmentModel.DoesNotExist:
            return None

    def find_upcoming(self, current_time: datetime) -> List[AppointmentRecord]:
        qs = AppointmentModel.objects.filter(is_canceled=False, is_completed=False, reserved_at__gte=current_time)
        return [self._to_record(am) for am in qs]  # am is short for AppointmentModel

    def save(self, appointment: AppointmentRecord) -> AppointmentRecord:
        app_model, _ = AppointmentModel.objects.update_or_create(
            id=appointment.id,
            defaults={
                "slot_id": appointment.slot_id,
                "patient_id": appointment.patient_id,
                "patient_name": appointment.patient_name,
                "reserved_at": appointment.reserved_at,
                "is_completed": appointment.is_completed,
                "is_canceled": appointment.is_canceled,
            },
        )
        return self._to_record(app_model)

    def _to_record(self, app_model: AppointmentModel) -> AppointmentRecord:
        return AppointmentRecord(
            id=app_model.id,
            slot_id=app_model.slot_id,
            patient_id=app_model.patient_id,
            patient_name=app_model.patient_name,
            reserved_at=app_model.reserved_at,
            is_completed=getattr(app_model, "is_completed", False),
            is_canceled=getattr(app_model, "is_canceled", False),
        )
