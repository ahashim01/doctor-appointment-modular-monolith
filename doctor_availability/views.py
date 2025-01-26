from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import SlotSerializer
from .services import SlotService


class SlotListCreateView(generics.GenericAPIView):
    """
    Handles listing and creating slots via the SlotService.
    """

    serializer_class = SlotSerializer

    def get(self, request, *args, **kwargs):
        """
        List all available slots.
        """
        slots = SlotService.list_available_slots()
        serializer = self.serializer_class(slots, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new slot for a doctor.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                slot = SlotService.create_slot(
                    doctor_id=serializer.validated_data["doctor_id"],
                    time=serializer.validated_data["time"],
                    cost=serializer.validated_data["cost"],
                )
                # Serialize and return the created slot
                serialized_slot = self.serializer_class(slot)
                return Response(serialized_slot.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
