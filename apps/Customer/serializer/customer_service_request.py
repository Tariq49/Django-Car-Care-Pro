from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.Customer.models.customer_service_request import Vehicle
from apps.Mechanic.models.price_per_service import MechanicPricePerService
from apps.Customer.models import ServiceRequest
from datetime import timedelta
from django.utils import timezone



class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_no', 'vehicle_name', 'vehicle_model', 'vehicle_brand']
        read_only_fields = ['id']



class ServiceRequestSerializer(serializers.ModelSerializer):
    
    mechanic = serializers.PrimaryKeyRelatedField(queryset=MechanicPricePerService.objects.all(), required=False)
    mechanic_details = serializers.SerializerMethodField()
    vehicles = VehicleSerializer(many=True)
    service_request_id = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField() 
    
    class Meta:
        model = ServiceRequest
        fields = [
            'service_request_id','customer','customer_name', 'mechanic','mechanic_details', 'vehicles', 'category',
            'problem_description', 'date_of_request', 'service_name',
            'status', 'due_date', 'completed_date', 'mechanic_update'
        ]
        
    def get_service_request_id(self, obj):
        return obj.id 
    
      
    def get_customer_name(self, obj):
        # Adjust based on how customer name can be accessed
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

    def create(self, validated_data):
        
       
        vehicles_data = validated_data.pop('vehicles', [])
        customer = validated_data.get('customer')
        mechanic = validated_data.get('mechanic')  
        
        
        
        if not customer:
            raise serializers.ValidationError("Customer does not exist.")
        
        mechanic_price_service = None
        
        if mechanic:
            mechanic_price_service = MechanicPricePerService.objects.filter(id=mechanic.id).first()
            if not mechanic_price_service:
                raise serializers.ValidationError("MechanicPricePerService with this ID does not exist.")

        # Handle due_date if not provided
      #  due_date = validated_data.get('due_date') or None
      #  if not due_date:
       #     due_date = timezone.now() + timedelta(days=7) 

        # Check for existing request
        existing_request = ServiceRequest.objects.filter(
            customer=customer,
            problem_description=validated_data.get('problem_description'),
            service_name=validated_data.get('service_name')
        ).first()

        if existing_request:
            raise serializers.ValidationError("A ServiceRequest with these details already exists.")

        # Create the ServiceRequest instance
        service_request = ServiceRequest.objects.create(
            customer=customer,
            mechanic=mechanic_price_service,  
            category=validated_data.get('category'),
            problem_description=validated_data.get('problem_description'),
            service_name=validated_data.get('service_name'),
            mechanic_update=validated_data.get('mechanic_update'),
            status=validated_data.get('status', 'Pending'),
            due_date=validated_data.get('due_date'),
            date_of_request=timezone.now(),  
            completed_date=validated_data.get('completed_date')
        )

        # Create related vehicles
        for vehicle_data in vehicles_data:
            Vehicle.objects.create(service_request=service_request, **vehicle_data)

        return service_request


    def update(self, instance, validated_data):
        
        vehicles_data = validated_data.pop('vehicles', [])
        instance.customer = validated_data.get('customer', instance.customer)
        instance.mechanic = validated_data.get('mechanic', instance.mechanic)
        instance.category = validated_data.get('category', instance.category)
        instance.problem_description = validated_data.get('problem_description', instance.problem_description)
        instance.date_of_request = validated_data.get('date_of_request', instance.date_of_request)
        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.status = validated_data.get('status', instance.status)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.completed_date = validated_data.get('completed_date', instance.completed_date)
        instance.mechanic_update = validated_data.get('mechanic_update',instance.mechanic_update)
        
        instance.save()

        
        # Handle vehicle updates
        current_vehicles = {v.id: v for v in instance.vehicles.all()}
        new_vehicles = []
        for vehicle_data in vehicles_data:
            vehicle_id = vehicle_data.get('id')
            if vehicle_id:
                try:
                    vehicle = current_vehicles.pop(vehicle_id)
                    for attr, value in vehicle_data.items():
                        setattr(vehicle, attr, value)
                    vehicle.save()
                except KeyError:
                    # Handle the case where the vehicle does not exist
                    Vehicle.objects.create(service_request=instance, **vehicle_data)
            else:
                new_vehicles.append(vehicle_data)
        
        # Add any new vehicles that were not previously assigned
        for vehicle_data in new_vehicles:
            Vehicle.objects.create(service_request=instance, **vehicle_data)

        # Delete any old vehicles that are no longer in the list
        for vehicle in current_vehicles.values():
            vehicle.delete()

        return instance