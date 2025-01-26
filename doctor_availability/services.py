import uuid
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from .models import Doctor, Slot


class SlotService:
    """
    Handles business logic related to slots.
    """

    @staticmethod
    def create_slot(doctor_id: uuid.UUID, time, cost) -> Slot:
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

    @staticmethod
    def get_slot_by_id(slot_id: uuid.UUID) -> Optional[Slot]:
        """
        Retrieve a specific slot by its UUID.
        Return None if it does not exist.
        """
        try:
            return Slot.objects.get(id=slot_id)
        except Slot.DoesNotExist:
            return None

    @staticmethod
    def reserve_slot(slot_id: uuid.UUID) -> bool:
        """
        Mark a slot as reserved, returning True if successful.
        Return False if the slot does not exist or is already reserved.
        """
        slot = SlotService.get_slot_by_id(slot_id)
        if slot is None or slot.is_reserved:
            return False

        slot.is_reserved = True
        slot.save()
        return True
