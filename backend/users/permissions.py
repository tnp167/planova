from rest_framework.permissions import BasePermission

class IsClerkAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_profile")
