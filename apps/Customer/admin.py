from django.contrib import admin
from .models.customer_service_request import Vehicle, ServiceRequest
from .models.customer import Customer
from .models.customer_feeback import CustomerFeedback

class VehicleInline(admin.TabularInline): 
    model = Vehicle
    extra = 1 

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name','username','address','contact_number','email','date_of_join')

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def email(self,obj):
        return obj.user.email
    
    def date_of_join(self, obj):
        return obj.user.date_joined
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

class ServiceRequestAdmin(admin.ModelAdmin):
    inlines = [VehicleInline] 
    
    list_display = ('customer', 'vehicle_details', 'service_name', 'problem_description','mechanic_assigned', 'status', 'date_of_request')

    def customer(self, obj):
        return obj.customer.user.username
    
    def mechanic_assigned(self, obj):
        if obj.mechanic:
            return f"{obj.mechanic.mechanic.user.first_name} {obj.mechanic.mechanic.user.last_name}"
        return "No mechanic assigned"
    
    def vehicle_details(self, obj):
        # Assuming one vehicle per service request. Adjust if multiple vehicles are allowed.
        vehicles = obj.vehicles.all()
        return ", ".join([f"{v.vehicle_name} {v.vehicle_model} ({v.vehicle_no})" for v in vehicles])

class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'get_customer_name', 
        'service_name', 
        'problem_description', 
        'rating', 
        'comments',
        'mechanic_name'
    )

    def get_customer_name(self, obj):
        return obj.service_id.customer.user.get_full_name() if obj.service_id.customer.user else "Unknown Customer"
    get_customer_name.short_description = 'Customer Name'

    def service_name(self, obj):
        return obj.service_id.service_name
    service_name.short_description = 'Service Name'

    def problem_description(self, obj):
        return obj.service_id.problem_description
    problem_description.short_description = 'Problem Description'

    def rating(self, obj):
        return obj.rating
    rating.short_description = 'Rating'

    def comments(self, obj):
        return obj.comments or "No comments provided"
    comments.short_description = 'Comments'

    def mechanic_name(self, obj):
        # Access the related ServiceRequest and then the MechanicPricePerService
        service_request = obj.service_id
        if service_request.mechanic:
            return service_request.mechanic.mechanic.user.get_full_name()
        return "No Mechanic Assigned"
    mechanic_name.short_description = 'Serviced By'

admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(CustomerFeedback,CustomerFeedbackAdmin)

