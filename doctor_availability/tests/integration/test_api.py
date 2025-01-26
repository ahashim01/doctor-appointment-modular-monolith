import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from doctor_availability.models import Doctor, Slot


class SlotAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create objects that are shared across all tests in this TestCase.
        Uses setUpTestData to improve performance (data is created once for all tests).
        """
        cls.doctor = Doctor.objects.create(
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
        cls.list_create_url = reverse("slot-list-create")

    def setUp(self):
        """
        Called once per test. Good place to initialize fresh state if needed.
        """
        self.client = APIClient()

    def test_list_empty_slots(self):
        """
        Test listing available slots when no slots exist yet.
        Should return an empty list.
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_slot_success(self):
        """
        Test creating a new slot via POST with valid data.
        """
        valid_data = {
            "time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "doctor_id": str(self.doctor.id),
            "cost": "200.00",
        }
        response = self.client.post(self.list_create_url, data=valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["doctor_id"], str(self.doctor.id))
        self.assertEqual(response.data["doctor_name"], "Dr. Ahmed")
        self.assertFalse(response.data["is_reserved"])
        self.assertEqual(response.data["cost"], "200.00")

        # Check data in the database
        slot_id = response.data["id"]
        created_slot = Slot.objects.get(id=slot_id)
        self.assertEqual(created_slot.doctor, self.doctor)
        self.assertEqual(created_slot.cost, 200.00)
        self.assertFalse(created_slot.is_reserved)

    def test_create_slot_with_invalid_doctor(self):
        """
        Test creating a new slot with a non-existent doctor UUID.
        Should return 400 with an error detail.
        """
        # Generate a random UUID that doesn't match any doctor
        invalid_doctor_id = str(uuid.uuid4())

        invalid_data = {
            "time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "doctor_id": invalid_doctor_id,
            "cost": "200.00",
        }
        response = self.client.post(self.list_create_url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Doctor with the provided ID does not exist.")

        # Ensure no new Slot was created
        self.assertEqual(Slot.objects.count(), 0)

    def test_create_slot_with_negative_cost(self):
        """
        Test creating a slot where cost <= 0.
        Should raise a validation error from the serializer.
        """
        invalid_data = {
            "time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "doctor_id": str(self.doctor.id),
            "cost": "-10.00",
        }
        response = self.client.post(self.list_create_url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure the cost field has the correct error message
        self.assertIn("cost", response.data)
        self.assertIn("Cost must be a positive number.", response.data["cost"])

        self.assertEqual(Slot.objects.count(), 0)

    def test_create_slot_with_past_time(self):
        """
        Test creating a slot with a time in the past.
        Should raise a validation error from the serializer.
        """
        invalid_data = {
            "time": (timezone.now() - timezone.timedelta(days=1)).isoformat(),
            "doctor_id": str(self.doctor.id),
            "cost": "200.00",
        }
        response = self.client.post(self.list_create_url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure the time field has the correct error message
        self.assertIn("time", response.data)
        self.assertIn("Slot time must be in the future.", response.data["time"])

        self.assertEqual(Slot.objects.count(), 0)

    def test_list_slots_after_creation(self):
        """
        Test listing available slots after creating multiple slots.
        Only not reserved slots should appear.
        """
        # Create several slots
        future_time = timezone.now() + timezone.timedelta(days=1)
        slot1 = Slot.objects.create(
            doctor=self.doctor,
            time=future_time,
            cost=100,
            is_reserved=False,
        )
        slot2 = Slot.objects.create(
            doctor=self.doctor2,
            time=future_time + timezone.timedelta(hours=2),
            cost=150,
            is_reserved=False,
        )
        slot3 = Slot.objects.create(
            doctor=self.doctor2,
            time=future_time + timezone.timedelta(hours=5),
            cost=250,
            is_reserved=True,  # This one is reserved
        )

        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We expect only the first two slots (unreserved) in the results
        returned_ids = [item["id"] for item in response.data]
        self.assertIn(str(slot1.id), returned_ids)
        self.assertIn(str(slot2.id), returned_ids)
        self.assertNotIn(str(slot3.id), returned_ids)

    def test_create_slot_for_second_doctor(self):
        """
        Test creating a slot for a different doctor.
        """
        valid_data = {
            "time": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            "doctor_id": str(self.doctor2.id),
            "cost": "300.00",
        }
        response = self.client.post(self.list_create_url, data=valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["doctor_name"], "Dr. Jane")

        # Confirm the slot belongs to Dr. Jane in the DB
        slot_id = response.data["id"]
        created_slot = Slot.objects.get(id=slot_id)
        self.assertEqual(created_slot.doctor, self.doctor2)
        self.assertEqual(created_slot.cost, 300.00)
        self.assertFalse(created_slot.is_reserved)
