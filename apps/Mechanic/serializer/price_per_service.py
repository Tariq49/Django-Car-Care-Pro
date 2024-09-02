from rest_framework import serializers
from apps.Mechanic.models import Mechanic
from apps.Mechanic.models import MechanicPricePerService
from decimal import Decimal 

class MechanicPricePerServiceSerializer(serializers.ModelSerializer):
    
    mechanic_name = serializers.SerializerMethodField()
    years_of_experience = serializers.SerializerMethodField()  
      
    hourly_rate = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=Decimal('0.01')  
    )
   
    class Meta:
        model = MechanicPricePerService
        fields = [
            'id',
            'mechanic_name',
            'years_of_experience',
            'service_name',
            'hourly_rate',
            'currency',
        ]
       

    def get_mechanic_name(self, obj):
        # Ensure obj.mechanic is a valid Mechanic instance
        if obj.mechanic and obj.mechanic.user:
            return f"{obj.mechanic.user.first_name} {obj.mechanic.user.last_name}"
        return "Unknown Mechanic"

    def get_years_of_experience(self, obj):
        # Ensure obj.mechanic is a valid Mechanic instance
        if obj.mechanic and obj.mechanic.years_of_experience is not None:
            return obj.mechanic.years_of_experience
        return "Unknown"  #