from django.contrib import admin
from apps.Customer.models import Customer



# Register your models here.

class CustomerDetailAdmin(admin.ModelAdmin):


    list_display = ('username', 'first_name', 'last_name', 'address','email','gender','contact_number','date_of_join')
  
admin.site.register(Customer,CustomerDetailAdmin)