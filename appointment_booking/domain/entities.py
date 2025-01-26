import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Appointment:
    """
    The Appointment entity holds the core business data for a booked appointment.
    It is a pure Python class with no Django dependencies.
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    slot_id: uuid.UUID = field(default_factory=uuid.uuid4)
    patient_id: uuid.UUID = field(default_factory=uuid.uuid4)
    patient_name: str = ""
    reserved_at: datetime = field(default_factory=datetime.utcnow)
