from django.test import TestCase
from django.utils.timezone import now, timedelta

from doctor_availability.models import Doctor
from doctor_availability.services import SlotService


class SlotServiceTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Dr. Ahmed",
            specialization="Cardiology",
            email="ahmed@example.com",
            phone_number="1234567890",
        )

    def test_create_slot_service(self):
        """
        Test the SlotService's create_slot method.
        """
        slot = SlotService.create_slot(
            doctor_id=self.doctor.id,
            time=now() + timedelta(days=1),
            cost=150.00,
        )
        self.assertEqual(slot.doctor.name, "Dr. Ahmed")
        self.assertEqual(slot.cost, 150.00)
        self.assertFalse(slot.is_reserved)

    def test_list_available_slots(self):
        """
        Test listing available slots via SlotService.
        """
        SlotService.create_slot(
            doctor_id=self.doctor.id,
            time=now() + timedelta(days=1),
            cost=200.00,
        )
        available_slots = SlotService.list_available_slots()
        self.assertEqual(len(available_slots), 1)
