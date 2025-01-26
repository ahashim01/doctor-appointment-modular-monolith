import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def send_appointment_confirmation(
    appointment_id: str, patient_name: str, doctor_name: str, appointment_time: datetime, **kwargs
) -> None:
    """
    Sends a confirmation notification (logs a message) to both the patient and the doctor.
    This is a minimalistic approach, as required by the 'simplest architecture possible'.
    """
    # For the sake of this assessment, we'll just log a message.
    # In a real-world system, you'd integrate with an email service, SMS gateway, etc.

    notification_message = (
        f"Appointment Confirmation:\n"
        f"Appointment ID: {appointment_id}\n"
        f"Patient Name: {patient_name}\n"
        f"Doctor Name: {doctor_name}\n"
        f"Appointment Time: {appointment_time.isoformat()}\n"
    )

    # Log the confirmation message
    logger.info(notification_message)

    # If desired, also "notify" the console or do more advanced steps here.
    # For real emailing, integrate with an email API or Celery tasks, etc.
