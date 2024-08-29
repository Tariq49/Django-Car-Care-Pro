from rest_framework.permissions import BasePermission

class IsMechanicOrCustomer(BasePermission):
    """
    Custom permission to only allow customers to view all mechanics and
    restrict mechanics to access only their own data.
    """
    
    def has_permission(self, request, view):
        # Allow access if the request method is safe (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow all customers to view all mechanics
        if request.user.is_customer:
            return True
        
        # Mechanics can only view or edit their own data
        if request.user.is_mechanic:
            return obj.id == request.user.mechanic.id
        
        return False
