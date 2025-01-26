import uuid
from abc import ABC, abstractmethod
from typing import Optional

from appointment_booking.domain.entities import Appointment


class IAppointmentRepository(ABC):
    """
    Defines the contract for storing and retrieving appointments.
    """

    @abstractmethod
    def save(self, appointment: Appointment) -> Appointment:
        """
        Persist an appointment.
        """
        pass

    @abstractmethod
    def find_by_slot_id(self, slot_id: uuid.UUID) -> Optional[Appointment]:
        """
        Find an appointment by its slot_id if it exists.
        """
        pass
