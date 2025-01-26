import uuid
from datetime import datetime

from appointment_booking.application.gateways.notification_gateway_interface import INotificationGateway
from appointment_confirmation.confirmation_service import send_appointment_confirmation


class NotificationGateway(INotificationGateway):
    """
    Concrete implementation of INotificationGateway using the
    appointment_confirmation module's simplest function.
    """

    def send_appointment_confirmation(
        self, appointment_id: uuid.UUID, patient_name: str, doctor_name: str, appointment_time: datetime
    ) -> None:
        send_appointment_confirmation(
            appointment_id=str(appointment_id),
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_time=appointment_time,
        )
