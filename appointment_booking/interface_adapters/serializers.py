from rest_framework import serializers


class BookAppointmentSerializer(serializers.Serializer):
    slot_id = serializers.UUIDField()
    patient_id = serializers.UUIDField()
    patient_name = serializers.CharField(max_length=255)
