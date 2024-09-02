from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to view or manage users.
    """
   
     
    message = "You don't have permission to perform this action."
    
    def has_permission(self, request, view):
        
        if request.method == 'POST':
            # Allow anyone to POST (create) a user
            return True
        
        if request.method in ['GET', 'PUT', 'DELETE', 'PATCH']:
            # Allow only admin users to GET (list), PUT (update), DELETE, or PATCH users
            return request.user and request.user.is_authenticated and request.user.is_staff
            

        return False

    