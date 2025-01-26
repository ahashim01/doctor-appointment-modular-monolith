from .models import Doctor, Slot


class SlotService:
    """
    Handles business logic related to doctor's availability slots.
    """

    @staticmethod
    def create_slot(doctor_id, time, cost):
        """
        Create a new slot for a given doctor.
        """
        doctor = Doctor.objects.get(id=doctor_id)
        slot = Slot.objects.create(doctor=doctor, time=time, cost=cost, is_reserved=False)
        return slot

    @staticmethod
    def list_available_slots():
        """
        List all available (not reserved) slots.
        """
        return Slot.objects.filter(is_reserved=False).select_related("doctor")
