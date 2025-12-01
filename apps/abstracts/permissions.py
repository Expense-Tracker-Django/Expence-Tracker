#Django REST Framework
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """Check if the requesting user is the owner of the object."""
        return obj.created_by == request.user