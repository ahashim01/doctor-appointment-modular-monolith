from django.core.exceptions import ObjectDoesNotExist

from .models import Doctor, Slot


class SlotService:
    """
    Handles business logic related to slots.
    """

    @staticmethod
    def create_slot(doctor_id, time, cost):
        """
        Create a new slot for a doctor.
        """
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except ObjectDoesNotExist:
            raise ValueError("Doctor with the provided ID does not exist.")

        slot = Slot.objects.create(
            doctor=doctor,
            time=time,
            cost=cost,
            is_reserved=False,
        )
        return slot

    @staticmethod
    def list_available_slots():
        """
        Retrieve all available (not reserved) slots.
        """
        return Slot.objects.filter(is_reserved=False).select_related("doctor")
