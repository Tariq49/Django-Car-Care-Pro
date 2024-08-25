from rest_framework import serializers
from apps.Customer.models import CustomerFeedback

class CustomerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        fields = ['id', 'service_id', 'rating', 'comments']
        extra_kwargs = {
            'service_id': {'required': False},
            'rating': {'required': True},
        }

    def validate_rating(self, value):
        """
        Ensure the rating is between 1 and 5.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def to_representation(self, instance):
        """
        Customize the representation of the CustomerFeedback instance.
        """
        representation = super().to_representation(instance)
        service_request = instance.service_id
        
        # Get customer name
        representation['customer_name'] = service_request.customer.user.get_full_name() if service_request.customer.user else "Unknown Customer"
        
        # Get service details
        representation['service_name'] = service_request.service_name
        representation['problem_description'] = service_request.problem_description
        
        # Access mechanic's name through MechanicPricePerService and Mechanic models
        mechanic_price_per_service = service_request.mechanic
        if mechanic_price_per_service and mechanic_price_per_service.mechanic.user:
            representation['mechanic_name'] = mechanic_price_per_service.mechanic.user.get_full_name()
        else:
            representation['mechanic_name'] = "Unknown Mechanic"

        return representation

