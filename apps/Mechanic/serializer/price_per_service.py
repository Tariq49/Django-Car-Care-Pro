from rest_framework import serializers
from apps.Mechanic.models import Mechanic
from apps.Mechanic.models import MechanicPricePerService

class MechanicPricePerServiceSerializer(serializers.ModelSerializer):
    
    mechanic_name = serializers.SerializerMethodField()
   
    class Meta:
        model = MechanicPricePerService
        fields = [
            'id',
            'mechanic_name',
            'service_name',
            'hourly_rate',
            'currency',
        ]
       

    def get_mechanic_name(self, obj):
        # Ensure obj.mechanic is a valid Mechanic instance
        if obj.mechanic and obj.mechanic.user:
            return f"{obj.mechanic.user.first_name} {obj.mechanic.user.last_name}"
        return "Unknown Mechanic"
