from django.contrib import admin
from apps.Mechanic.models import Mechanic,Specialization

# Register your models here.


class MechanicDetails(admin.ModelAdmin):
    list_display = ('get_mechanic_name', 'years_of_experience','get_specializations')

    def get_mechanic_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_mechanic_name.short_description = 'Mechanic Name'

    def get_specializations(self, obj):
        return ", ".join([specialization.name for specialization in obj.specializations.all()])

    get_specializations.short_description = 'Specializations'
   
admin.site.register(Specialization) 
admin.site.register(Mechanic,MechanicDetails)
