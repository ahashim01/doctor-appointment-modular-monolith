import unittest
from datetime import datetime
from unittest.mock import patch

from appointment_confirmation.confirmation_service import send_appointment_confirmation


class TestConfirmationService(unittest.TestCase):

    @patch("appointment_confirmation.confirmation_service.logger")
    def test_send_appointment_confirmation(self, mock_logger):
        appointment_id = "1234"
        patient_name = "John Doe"
        doctor_name = "Dr. Smith"
        appointment_time = datetime(2025, 1, 1, 10, 0, 0)

        send_appointment_confirmation(
            appointment_id=appointment_id,
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_time=appointment_time,
        )

        # Verify that logging was called once with the expected log message
        self.assertTrue(mock_logger.info.called)
        log_args, _ = mock_logger.info.call_args
        self.assertIn("Appointment Confirmation:", log_args[0])
        self.assertIn("John Doe", log_args[0])
        self.assertIn("Dr. Smith", log_args[0])
        self.assertIn("2025-01-01T10:00:00", log_args[0])
