from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.Customer.models.customer_service_request import Vehicle
from apps.Mechanic.models.price_per_service import MechanicPricePerService
from apps.Mechanic.models import Mechanic,Specialization
from apps.Customer.serializer import CustomerSerializer
from apps.Customer.models import ServiceRequest,Customer



class MechanicSerializer(serializers.ModelSerializer):

   

    class Meta:
        model = Mechanic
        fields = ['user']  
        read_only_fields = [ 'user'] 


class MechanicPricePerServiceSerializer(serializers.ModelSerializer):

    mechanic = MechanicSerializer(read_only=True)  
    
    class Meta:
        model = MechanicPricePerService
        fields = ['mechanic']
        read_only_fields = ['id'] 


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_no', 'vehicle_name', 'vehicle_model', 'vehicle_brand']
        read_only_fields = ['id']



class ServiceRequestSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    mechanic = serializers.PrimaryKeyRelatedField(queryset=MechanicPricePerService.objects.all(), required=False, allow_null=True)
    vehicles = VehicleSerializer(many=True, required=False)

    service_request_id = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        
    def validate_mechanic(self, value):
        if value and not MechanicPricePerService.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Invalid mechanic selected.")
        return value

    def get_service_request_id(self, obj):
        return obj.id

    def create(self, validated_data):

        vehicles_data = validated_data.pop('vehicles', [])
        mechanic = validated_data.pop('mechanic', None)
        customer = validated_data.get('customer')

         
        if customer is None:
            raise serializers.ValidationError({'customer': 'This field is required.'})
        
      #  service_request = ServiceRequest.objects.create(**validated_data)
         
        service_request = ServiceRequest.objects.create(
            customer=customer,
            mechanic=mechanic,
            category=validated_data.get('category'),
            problem_description=validated_data.get('problem_description'),
            service_name=validated_data.get('service_name'),
            status='Pending'
           
        )

        for vehicle_data in vehicles_data:
            vehicle_data.pop('id', None)
            Vehicle.objects.create(service_request=service_request, **vehicle_data)

        return service_request
  

    def update(self, instance, validated_data):
        vehicles_data = validated_data.pop('vehicles', None)

        instance.category = validated_data.get('category', instance.category)
        instance.problem_description = validated_data.get('problem_description', instance.problem_description)
        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.mechanic_update = validated_data.get('mechanic_update', instance.mechanic_update)
        instance.status = validated_data.get('status', instance.status)
        instance.completed_date = validated_data.get('completed_date', instance.completed_date)
        instance.save()

        if vehicles_data is not None:
            # Handle vehicle updates if needed
            for vehicle_data in vehicles_data:
                vehicle_id = vehicle_data.get('id')
                if vehicle_id:
                    try:
                        vehicle = Vehicle.objects.get(id=vehicle_id, service_request=instance)
                        for attr, value in vehicle_data.items():
                            setattr(vehicle, attr, value)
                        vehicle.save()
                    except Vehicle.DoesNotExist:
                        # Handle the case where the vehicle does not exist
                        pass
                else:
                    Vehicle.objects.create(service_request=instance, **vehicle_data)

        return instance