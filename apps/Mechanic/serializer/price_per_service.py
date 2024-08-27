from rest_framework import serializers
from apps.Mechanic.models import Mechanic
from apps.Mechanic.models import MechanicPricePerService

class MechanicPricePerServiceSerializer(serializers.ModelSerializer):
    mechanic_full_name = serializers.SerializerMethodField()
    mechanic_experience = serializers.SerializerMethodField()

    class Meta:
        model = MechanicPricePerService
        fields = [
            'id',
            'mechanic',
            'mechanic_full_name',
            'mechanic_experience',
            'service_name',
            'hourly_rate',
            'currency',
        ]

    def get_mechanic_full_name(self, obj):
        return f"{obj.mechanic.user.first_name} {obj.mechanic.user.last_name}"

    def get_mechanic_experience(self, obj):
        return obj.mechanic.years_of_experience
