from django.contrib import admin

from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')
    # Add any additional customization here if needed

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
