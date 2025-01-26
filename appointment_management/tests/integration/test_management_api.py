import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta
from rest_framework import status
from rest_framework.test import APIClient

from appointment_booking.infrastructure.models import AppointmentModel


class AppointmentManagementAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some sample appointments
        self.app1 = AppointmentModel.objects.create(
            slot_id=uuid.uuid4(),
            patient_id=uuid.uuid4(),
            patient_name="Alice",
            reserved_at=now() + timedelta(days=1),
        )
        self.app2 = AppointmentModel.objects.create(
            slot_id=uuid.uuid4(),
            patient_id=uuid.uuid4(),
            patient_name="Bob",
            reserved_at=now() - timedelta(days=1),  # Past appointment
        )

    def test_get_upcoming_appointments(self):
        url = reverse("upcoming-appointments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect only app1 is returned because app2 is in the past
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["patient_name"], "Alice")

    def test_mark_appointment_completed(self):
        url = reverse("mark-appointment-completed", args=[str(self.app1.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.app1.refresh_from_db()
        self.assertTrue(self.app1.is_completed)

    def test_cancel_appointment(self):
        url = reverse("cancel-appointment", args=[str(self.app1.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.app1.refresh_from_db()
        self.assertTrue(self.app1.is_canceled)
