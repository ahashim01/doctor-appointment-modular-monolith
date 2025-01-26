import uuid
from datetime import datetime, timezone
from typing import Optional

from appointment_booking.application.gateways.notification_gateway_interface import INotificationGateway
from appointment_booking.application.repositories.appointment_repository_interface import IAppointmentRepository
from appointment_booking.domain.entities import Appointment

# We'll need to reference the doctor_availability module for slot checks
# but let's keep the minimal coupling via a function interface or direct import:
from doctor_availability.services import SlotService


class BookAppointmentUseCase:
    """
    Handles the business logic for booking an appointment:
    - Checks if the slot is available.
    - Reserves the slot and creates an Appointment entity.
    """

    def __init__(self, appointment_repository: IAppointmentRepository, notification_gateway: INotificationGateway):
        self.appointment_repository = appointment_repository
        self.notification_gateway = notification_gateway

    def execute(self, slot_id: uuid.UUID, patient_id: uuid.UUID, patient_name: str) -> Optional[Appointment]:
        """
        Book an appointment for a given slot if it's free.
        """
        # 1. Check if an appointment already exists for this slot
        existing_appointment = self.appointment_repository.find_by_slot_id(slot_id)
        if existing_appointment:
            # Slot is already booked
            return None

        # 2. Check if slot is actually available (not reserved)
        slot = SlotService.get_slot_by_id(slot_id)
        if not slot or slot.is_reserved:
            # Slot not found or already reserved
            return None

        # 3. Mark slot as reserved
        SlotService.reserve_slot(slot_id)

        # 4. Create appointment entity
        new_appointment = Appointment(
            slot_id=slot_id,
            patient_id=patient_id,
            patient_name=patient_name,
            reserved_at=datetime.now(timezone.utc),
        )

        # 5. Persist appointment
        saved_appointment = self.appointment_repository.save(new_appointment)

        # 6. Send confirmation notification
        self.notification_gateway.send_appointment_confirmation(
            appointment_id=saved_appointment.id,
            patient_name=saved_appointment.patient_name,
            doctor_name=slot.doctor.name,  # from the slot
            appointment_time=slot.time,
        )

        return saved_appointment
