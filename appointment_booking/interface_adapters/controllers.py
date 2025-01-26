from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from appointment_booking.application.use_cases.book_appointment_use_case import BookAppointmentUseCase
from appointment_booking.infrastructure.gateways.notification_gateway import NotificationGateway
from appointment_booking.infrastructure.repositories.appointment_repository import AppointmentRepository

from .serializers import BookAppointmentSerializer


class BookAppointmentController(APIView):
    """
    API Controller to book an appointment.
    """

    def post(self, request):
        serializer = BookAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            slot_id = serializer.validated_data["slot_id"]
            patient_id = serializer.validated_data["patient_id"]
            patient_name = serializer.validated_data["patient_name"]

            # Instantiate dependencies
            appointment_repo = AppointmentRepository()
            notification_gateway = NotificationGateway()

            use_case = BookAppointmentUseCase(
                appointment_repository=appointment_repo, notification_gateway=notification_gateway
            )
            appointment = use_case.execute(slot_id=slot_id, patient_id=patient_id, patient_name=patient_name)

            if not appointment:
                return Response({"detail": "Slot is already booked or invalid."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {
                    "id": str(appointment.id),
                    "slot_id": str(appointment.slot_id),
                    "patient_id": str(appointment.patient_id),
                    "patient_name": appointment.patient_name,
                    "reserved_at": appointment.reserved_at.isoformat(),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
