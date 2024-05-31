from rest_framework import permissions


class IsUserOnly(permissions.BasePermission):
    """
    Permission class that only allows access to the user's objects.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has object permission.
        Args:
            request (HttpRequest): The HTTP request object.
            view (View): The view object.
            obj (Object): The object to check permission for.
        Returns:
            bool: True if the user has object permission, False otherwise.
        """
        if obj.user == request.user:
            return True
        return False
