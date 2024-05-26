from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Fridge, CourierFridgePermission


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser


class IsLocalAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_local_admin


class IsLocalAdminFridgeOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_local_admin

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_local_admin and obj.owner == request.user


class IsLocalAdminFridgeOwnerForFridgeProduct(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_local_admin

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_local_admin and obj.fridge.owner == request.user


class IsStaffReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.method in SAFE_METHODS


class IsStaffUserFridgeProductCourier(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return CourierFridgePermission.objects.filter(user=request.user, fridge=obj.fridge).exists()
        return False
