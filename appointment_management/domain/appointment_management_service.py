import uuid
from datetime import datetime
from typing import List

from appointment_management.ports.outbound.appointment_repository_port import IAppointmentRepository


class DoctorAppointmentManagementService:
    """
    Core domain service for managing the doctor's appointments.
    """

    def __init__(self, appointment_repository: IAppointmentRepository):
        self.appointment_repository = appointment_repository

    def get_upcoming_appointments(self) -> List:
        """
        Retrieve all upcoming appointments (not canceled, not completed, and time is in the future).
        """
        now = datetime.now(datetime.timezone.utc)
        return self.appointment_repository.find_upcoming(now)

    def mark_appointment_completed(self, appointment_id: uuid.UUID) -> bool:
        """
        Mark an appointment as completed if it's valid and not already canceled or completed.
        Returns True if successful, False otherwise.
        """
        appointment = self.appointment_repository.find_by_id(appointment_id)
        if not appointment or appointment.is_canceled or appointment.is_completed:
            return False

        appointment.is_completed = True
        self.appointment_repository.save(appointment)
        return True

    def cancel_appointment(self, appointment_id: uuid.UUID) -> bool:
        """
        Cancel an appointment if it's valid and not already canceled or completed.
        Returns True if successful, False otherwise.
        """
        appointment = self.appointment_repository.find_by_id(appointment_id)
        if not appointment or appointment.is_canceled or appointment.is_completed:
            return False

        appointment.is_canceled = True
        self.appointment_repository.save(appointment)
        return True
