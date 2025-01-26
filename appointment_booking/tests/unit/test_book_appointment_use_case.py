import unittest
import uuid
from unittest.mock import MagicMock

from appointment_booking.application.use_cases.book_appointment_use_case import BookAppointmentUseCase
from appointment_booking.domain.entities import Appointment


class TestBookAppointmentUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.use_case = BookAppointmentUseCase(appointment_repository=self.mock_repo)

    def test_slot_already_booked(self):
        # Setup
        slot_id = uuid.uuid4()
        self.mock_repo.find_by_slot_id.return_value = Appointment(
            slot_id=slot_id,
            patient_id=uuid.uuid4(),
            patient_name="Existing Patient",
        )

        # Act
        result = self.use_case.execute(slot_id, uuid.uuid4(), "New Patient")

        # Assert
        self.assertIsNone(result)

    def test_slot_is_available(self):
        slot_id = uuid.uuid4()
        self.mock_repo.find_by_slot_id.return_value = None
        # Mock SlotService as well
        from doctor_availability.services import SlotService

        SlotService.get_slot_by_id = MagicMock(return_value=MagicMock(is_reserved=False))
        SlotService.reserve_slot = MagicMock()

        self.mock_repo.save.side_effect = lambda app: app  # Return the same appointment object

        result = self.use_case.execute(slot_id, uuid.uuid4(), "John Doe")
        self.assertIsNotNone(result)
        self.assertEqual(result.patient_name, "John Doe")
        SlotService.reserve_slot.assert_called_once_with(slot_id)
