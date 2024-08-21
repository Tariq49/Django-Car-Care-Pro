from django.contrib import admin
from .models.customer_service_request import Vehicle, ServiceRequest
from .models.customer import Customer

class VehicleInline(admin.TabularInline): 
    model = Vehicle
    extra = 1 

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name','address','contact_number')

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class ServiceRequestAdmin(admin.ModelAdmin):
    inlines = [VehicleInline] 
    
    list_display = ('customer', 'vehicle_details', 'service_name', 'problem_description','mechanic_assigned', 'status', 'date_of_request')

    def customer(self, obj):
        return obj.customer.user.username
    
    def mechanic_assigned(self, obj):
        if obj.mechanic:
            return f"{obj.mechanic.user.first_name} {obj.mechanic.user.last_name}"
        return "No mechanic assigned"
    
    def vehicle_details(self, obj):
        # Assuming one vehicle per service request. Adjust if multiple vehicles are allowed.
        vehicles = obj.vehicles.all()
        return ", ".join([f"{v.vehicle_name} {v.vehicle_model} ({v.vehicle_no})" for v in vehicles])

admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(Customer,CustomerAdmin)

