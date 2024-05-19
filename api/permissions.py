from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsStaffUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return request.method in SAFE_METHODS
        return False


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
