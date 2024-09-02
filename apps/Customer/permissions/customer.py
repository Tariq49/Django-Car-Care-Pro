
from rest_framework.permissions import BasePermission
from apps.Customer.models import Customer
    
class IsOwnCustomer(BasePermission):
    """
    Custom permission to ensure that a customer can only access their own data.
    """
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            # Ensure the user can only access their own customer details
            try:
                customer = Customer.objects.get(user=request.user)
                return customer is not None
            except Customer.DoesNotExist:
                return False
        return True
    
    
    def has_object_permission(self, request, view, obj):
        # Allow access only if the object belongs to the requesting user
        return obj.user == request.user   