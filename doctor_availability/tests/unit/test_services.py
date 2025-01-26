import uuid

from django.test import TestCase
from django.utils import timezone

from doctor_availability.models import Doctor, Slot
from doctor_availability.services import SlotService


class TestSlotService(TestCase):
    """
    Unit tests for the SlotService class.
    """

    @classmethod
    def setUpTestData(cls):
        # Create some doctor objects for use in our tests.
        cls.doctor1 = Doctor.objects.create(
            name="Dr. Ahmed",
            specialization="Cardiology",
            email="ahmed@example.com",
            phone_number="1234567890",
        )
        cls.doctor2 = Doctor.objects.create(
            name="Dr. Jane",
            specialization="Dermatology",
            email="jane@example.com",
            phone_number="9876543210",
        )

    def test_create_slot_success(self):
        """
        Test successfully creating a slot for an existing doctor.
        """
        time_in_future = timezone.now() + timezone.timedelta(days=1)
        cost = 100.0

        slot = SlotService.create_slot(
            doctor_id=self.doctor1.id,
            time=time_in_future,
            cost=cost,
        )

        # Verify the slot was created correctly
        self.assertIsInstance(slot, Slot)
        self.assertEqual(slot.doctor, self.doctor1)
        self.assertEqual(slot.time, time_in_future)
        self.assertEqual(slot.cost, cost)
        self.assertFalse(slot.is_reserved)

    def test_create_slot_nonexistent_doctor(self):
        """
        Test attempting to create a slot with a doctor_id that doesn't exist.
        Should raise a ValueError.
        """
        random_uuid = uuid.uuid4()
        time_in_future = timezone.now() + timezone.timedelta(days=1)
        cost = 100.0

        with self.assertRaises(ValueError) as context:
            SlotService.create_slot(
                doctor_id=random_uuid,
                time=time_in_future,
                cost=cost,
            )
        self.assertIn("Doctor with the provided ID does not exist.", str(context.exception))

        # Ensure that no slot was created
        self.assertEqual(Slot.objects.count(), 0)

    def test_list_available_slots_empty(self):
        """
        Test that listing available slots returns an empty QuerySet if none exist.
        """
        slots = SlotService.list_available_slots()
        self.assertEqual(slots.count(), 0)

    def test_list_available_slots(self):
        """
        Test that list_available_slots only returns unreserved slots.
        """
        # Create some slots
        future_time = timezone.now() + timezone.timedelta(days=1)

        # Unreserved slot
        slot1 = Slot.objects.create(doctor=self.doctor1, time=future_time, cost=200, is_reserved=False)
        # Reserved slot
        slot2 = Slot.objects.create(
            doctor=self.doctor2, time=future_time + timezone.timedelta(hours=2), cost=300, is_reserved=True
        )
        # Another unreserved slot
        slot3 = Slot.objects.create(
            doctor=self.doctor1, time=future_time + timezone.timedelta(hours=3), cost=400, is_reserved=False
        )

        available_slots = SlotService.list_available_slots()
        self.assertIn(slot1, available_slots)
        self.assertIn(slot3, available_slots)
        self.assertNotIn(slot2, available_slots)
        self.assertEqual(available_slots.count(), 2)
