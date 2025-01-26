from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from appointment_management.adapters.outbound.appointment_repository_adapter import AppointmentRepositoryAdapter
from appointment_management.domain.appointment_management_service import DoctorAppointmentManagementService


class UpcomingAppointmentsController(APIView):
    """
    Handles requests to view upcoming appointments for the doctor.
    """

    def get(self, request):
        service = DoctorAppointmentManagementService(appointment_repository=AppointmentRepositoryAdapter())
        appointments = service.get_upcoming_appointments()

        response_data = []
        for appt in appointments:
            response_data.append(
                {
                    "id": str(appt.id),
                    "patient_name": appt.patient_name,
                    "reserved_at": appt.reserved_at.isoformat(),
                    "is_completed": appt.is_completed,
                    "is_canceled": appt.is_canceled,
                }
            )

        return Response(response_data, status=status.HTTP_200_OK)


class MarkAppointmentCompletedController(APIView):
    """
    Handles requests to mark an appointment as completed.
    """

    def post(self, request, appointment_id):
        service = DoctorAppointmentManagementService(appointment_repository=AppointmentRepositoryAdapter())

        success = service.mark_appointment_completed(appointment_id)
        if success:
            return Response({"detail": "Appointment marked as completed."}, status=status.HTTP_200_OK)
        return Response({"detail": "Unable to complete appointment."}, status=status.HTTP_400_BAD_REQUEST)


class CancelAppointmentController(APIView):
    """
    Handles requests to cancel an appointment.
    """

    def post(self, request, appointment_id):
        service = DoctorAppointmentManagementService(appointment_repository=AppointmentRepositoryAdapter())

        success = service.cancel_appointment(appointment_id)
        if success:
            return Response({"detail": "Appointment canceled."}, status=status.HTTP_200_OK)
        return Response({"detail": "Unable to cancel appointment."}, status=status.HTTP_400_BAD_REQUEST)
