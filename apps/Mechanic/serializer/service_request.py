from apps.Customer.models.customer_service_request import ServiceRequest
from rest_framework import serializers
from apps.Customer.models.customer_service_request import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_no', 'vehicle_name', 'vehicle_model', 'vehicle_brand']

class MechanicUpdateServiceRequestSerializer(serializers.ModelSerializer):
    
    vehicles = VehicleSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = ServiceRequest
        fields = ['mechanic_update', 'status', 'completed_date']
        read_only_fields = ['mechanic', 'customer', 'category', 'problem_description', 'date_of_request', 'service_name','due_date','vehicles']