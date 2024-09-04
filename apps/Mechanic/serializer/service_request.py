from apps.Customer.models.customer_service_request import ServiceRequest
from rest_framework import serializers
from apps.Customer.serializer.customer_service_request import VehicleSerializer



class MechanicUpdateServiceRequestSerializer(serializers.ModelSerializer):
    
    mechanic_details = serializers.SerializerMethodField()
    vehicles = VehicleSerializer(many=True, read_only=True)  # Vehicles should be read-only for mechanics
    service_request_id = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            'service_request_id', 
            'customer', 
            'customer_name', 
            'mechanic', 
            'mechanic_details', 
            'vehicles', 
            'category', 
            'problem_description', 
            'date_of_request', 
            'service_name', 
            'status', 
            'due_date', 
            'completed_date', 
            'mechanic_update'
        ]
        read_only_fields = [
            'service_request_id', 
            'customer', 
            'customer_name', 
            'mechanic', 
            'mechanic_details', 
            'vehicles', 
            'category', 
            'problem_description', 
            'date_of_request', 
            'service_name', 
            'due_date'
        ]

    def get_service_request_id(self, obj):
        return obj.id

    def get_customer_name(self, obj):
        if obj.customer and obj.customer.user:
            return f"{obj.customer.user.first_name} {obj.customer.user.last_name}".strip()
        return None

    def get_mechanic_details(self, obj):
        if obj.mechanic:
            mechanic = obj.mechanic
            return {
                'mechanic_name': f"{mechanic.mechanic.user.first_name} {mechanic.mechanic.user.last_name}",
                'years_of_experience': mechanic.mechanic.years_of_experience,
                'service_name': mechanic.service_name,
                'price_per_service': f"{mechanic.hourly_rate} {mechanic.currency}"
            }
        return None