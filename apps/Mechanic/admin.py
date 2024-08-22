from django.contrib import admin
from apps.Mechanic.models import Mechanic,Specialization
from apps.Mechanic.models import MechanicPricePerService

# Register your models here.


class MechanicDetails(admin.ModelAdmin):
    list_display = ('get_mechanic_name', 'years_of_experience','get_specializations','contact_number','preferred_job_types','formatted_work_days')

    def get_mechanic_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_mechanic_name.short_description = 'Mechanic Name'

    def get_specializations(self, obj):
        return ", ".join([specialization.name for specialization in obj.specializations.all()])

    get_specializations.short_description = 'Specializations'

    def formatted_work_days(self, obj):
        return ", ".join(obj.work_days) if obj.work_days else "Not specified"
    formatted_work_days.short_description = 'Work Days'

class MechanicService(admin.ModelAdmin):
    list_display = ('get_mechanic_name','service_name','formatted_hourly_rate')   

    def get_mechanic_name(self, obj):
        return f"{obj.mechanic.user.first_name} {obj.mechanic.user.last_name}" 
    get_mechanic_name.short_description = 'Mechanic Name'

    def formatted_hourly_rate(self, obj):
        return f"{obj.hourly_rate} {obj.currency}"
    formatted_hourly_rate.short_description = 'Hourly Rate'
   
admin.site.register(Specialization) 
admin.site.register(Mechanic,MechanicDetails)
admin.site.register(MechanicPricePerService,MechanicService)
