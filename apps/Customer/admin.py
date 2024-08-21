from django.contrib import admin
from . import models


class ServiceRequests(admin.ModelAdmin):
    
    list_display = ('customer_username','vehicle_no','service_name')

    def customer_username(self, obj):
        return obj.customer.user.username

admin.site.register(models.Customer)
admin.site.register(models.ServiceRequest,ServiceRequests)



