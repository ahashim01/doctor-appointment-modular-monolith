import unittest
import uuid
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from appointment_management.domain.appointment_management_service import DoctorAppointmentManagementService
from appointment_management.ports.outbound.appointment_repository_port import AppointmentRecord


class TestAppointmentManagementService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = DoctorAppointmentManagementService(appointment_repository=self.mock_repo)

    def test_get_upcoming_appointments(self):
        # Setup
        mock_records = [
            AppointmentRecord(
                id=uuid.uuid4(),
                slot_id=uuid.uuid4(),
                patient_id=uuid.uuid4(),
                patient_name="John",
                reserved_at=datetime.now() + timedelta(days=1),
            )
        ]
        self.mock_repo.find_upcoming.return_value = mock_records

        # Execute
        results = self.service.get_upcoming_appointments()

        # Verify
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].patient_name, "John")
        self.mock_repo.find_upcoming.assert_called_once()

    def test_mark_appointment_completed(self):
        appointment_id = uuid.uuid4()
        mock_record = AppointmentRecord(
            id=appointment_id,
            slot_id=uuid.uuid4(),
            patient_id=uuid.uuid4(),
            patient_name="John",
            reserved_at=datetime.now(),
        )
        self.mock_repo.find_by_id.return_value = mock_record

        success = self.service.mark_appointment_completed(appointment_id)
        self.assertTrue(success)
        self.assertTrue(mock_record.is_completed)

    def test_cancel_appointment_already_completed(self):
        appointment_id = uuid.uuid4()
        mock_record = AppointmentRecord(
            id=appointment_id,
            slot_id=uuid.uuid4(),
            patient_id=uuid.uuid4(),
            patient_name="John",
            reserved_at=datetime.now(),
            is_completed=True,
        )
        self.mock_repo.find_by_id.return_value = mock_record

        success = self.service.cancel_appointment(appointment_id)
        self.assertFalse(success)
