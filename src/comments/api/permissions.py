from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Checks if object belongs to the user making the request
    Only the owner may perform actions on their own models
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
