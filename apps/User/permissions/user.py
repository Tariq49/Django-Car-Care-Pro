from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to view or manage users.
    """
    def has_permission(self, request, view):
        # Check if the user is an admin
        return request.user and request.user.is_staff
