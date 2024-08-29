from apps.Customer.models.customer_service_request import ServiceRequest
from rest_framework import serializers


class MechanicUpdateServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['mechanic_update', 'status', 'completed_date']
        read_only_fields = ['mechanic', 'customer', 'category', 'problem_description', 'date_of_request', 'service_name']