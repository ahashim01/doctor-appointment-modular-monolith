import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta
from rest_framework import status
from rest_framework.test import APIClient

from doctor_availability.models import Doctor, Slot


class BookAppointmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.doctor = Doctor.objects.create(name="Dr. Ahmed")
        self.slot = Slot.objects.create(
            doctor=self.doctor,
            time=now() + timedelta(days=1),
            cost=100.00,
            is_reserved=False,
        )
        self.url = reverse("book-appointment")
        self.payload = {
            "slot_id": str(self.slot.id),
            "patient_id": str(uuid.uuid4()),
            "patient_name": "Alice",
        }

    def test_book_appointment_success(self):
        response = self.client.post(self.url, data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("reserved_at", response.data)
        self.assertEqual(response.data["patient_name"], "Alice")

        # Verify slot is reserved
        self.slot.refresh_from_db()
        self.assertTrue(self.slot.is_reserved)

    def test_book_already_reserved_slot(self):
        """
        Reserve the slot, then try booking again.
        """
        self.slot.is_reserved = True
        self.slot.save()

        response = self.client.post(self.url, data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Slot is already booked or invalid.")
