
from rest_framework.permissions import BasePermission

    
class IsOwnCustomer(BasePermission):
    """
    Custom permission to ensure that a customer can only access their own data.
    """

    def has_object_permission(self, request, view, obj):
        # Allow access only if the object belongs to the requesting user
        return obj.user == request.user   