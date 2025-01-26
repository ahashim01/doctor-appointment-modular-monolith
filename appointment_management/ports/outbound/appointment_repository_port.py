import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class AppointmentRecord:
    """
    A simple data structure representing an appointment record
    within the appointment_management context.
    """

    def __init__(
        self,
        id: uuid.UUID,
        slot_id: uuid.UUID,
        patient_id: uuid.UUID,
        patient_name: str,
        reserved_at: datetime,
        is_completed: bool = False,
        is_canceled: bool = False,
    ):
        self.id = id
        self.slot_id = slot_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.reserved_at = reserved_at
        self.is_completed = is_completed
        self.is_canceled = is_canceled


class IAppointmentRepository(ABC):
    """
    Outbound port for interacting with appointment records.
    """

    @abstractmethod
    def find_by_id(self, appointment_id: uuid.UUID) -> Optional[AppointmentRecord]:
        pass

    @abstractmethod
    def find_upcoming(self, current_time: datetime) -> List[AppointmentRecord]:
        """
        Retrieve all appointments that:
        - are not canceled
        - are not completed
        - have a reserved_at time >= current_time
        """
        pass

    @abstractmethod
    def save(self, appointment: AppointmentRecord) -> AppointmentRecord:
        """
        Create or update the appointment record.
        """
        pass
