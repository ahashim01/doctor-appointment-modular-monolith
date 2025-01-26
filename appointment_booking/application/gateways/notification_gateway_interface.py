import uuid
from abc import ABC, abstractmethod
from datetime import datetime


class INotificationGateway(ABC):
    """
    Defines the contract for sending appointment notifications.
    """

    @abstractmethod
    def send_appointment_confirmation(
        self, appointment_id: uuid.UUID, patient_name: str, doctor_name: str, appointment_time: datetime
    ) -> None:
        """
        Send or log a confirmation notification for a booked appointment.
        """
        pass
