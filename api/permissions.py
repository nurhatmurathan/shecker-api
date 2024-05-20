from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Fridge, CourierFridgePermission


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


class IsCourierWithFridgePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        elif request.user and not request.user.is_staff:
            return False

        fridge_id = view.kwargs.get('id')

        try:
            fridge = Fridge.objects.get(pk=fridge_id)
        except Fridge.DoesNotExist:
            return False

        return CourierFridgePermission.objects.filter(user=request.user, fridge=fridge).exists()
