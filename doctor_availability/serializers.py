from rest_framework import serializers


class SlotSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    time = serializers.DateTimeField()
    doctor_id = serializers.UUIDField()
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)
    is_reserved = serializers.BooleanField(read_only=True)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_time(self, value):
        """
        Ensure the slot time is in the future.
        """
        from django.utils.timezone import now

        if value <= now():
            raise serializers.ValidationError("Slot time must be in the future.")
        return value

    def validate_cost(self, value):
        """
        Ensure the cost is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Cost must be a positive number.")
        return value
