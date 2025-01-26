import unittest
import uuid
from datetime import datetime

from appointment_booking.domain.entities import Appointment


class TestAppointmentEntity(unittest.TestCase):

    def test_create_appointment_entity(self):
        slot_id = uuid.uuid4()
        patient_id = uuid.uuid4()
        appointment = Appointment(
            slot_id=slot_id, patient_id=patient_id, patient_name="John Doe", reserved_at=datetime(2025, 1, 1, 10, 0, 0)
        )
        self.assertEqual(appointment.slot_id, slot_id)
        self.assertEqual(appointment.patient_name, "John Doe")
        self.assertEqual(appointment.reserved_at, datetime(2025, 1, 1, 10, 0, 0))
