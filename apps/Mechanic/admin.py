from django.contrib import admin
from apps.Mechanic.models import Mechanic,Specialization

# Register your models here.


class MechanicDetails(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'years_of_experience', 'get_specializations')

    def get_specializations(self, obj):
        # obj refers to the instance of Mechanic
        return ", ".join(s.name for s in obj.specializations.all())
    get_specializations.short_description = 'Specializations'  # This sets the column header

admin.site.register(Specialization) 
admin.site.register(Mechanic, MechanicDetails)
