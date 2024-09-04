from rest_framework.permissions import BasePermission

class IsMechanicOrOwner(BasePermission):
    """
    Custom permission to allow only mechanics to view their own details.
    Other mechanics' data is not accessible.
    """
    
    def has_permission(self, request, view):
        # Ensure the user is authenticated and is a mechanic
        return request.user and request.user.is_authenticated and hasattr(request.user, 'mechanic')

    def has_object_permission(self, request, view, obj):
        # Only allow mechanics to access their own details
        return obj == request.user.mechanic
