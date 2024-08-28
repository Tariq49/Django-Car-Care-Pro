from rest_framework import serializers
from apps.Mechanic.models import Mechanic
from apps.Mechanic.models import MechanicPricePerService

class MechanicPricePerServiceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = MechanicPricePerService
        fields = [
            'id',
            'mechanic',
            'service_name',
            'hourly_rate',
            'currency',
        ]

   
