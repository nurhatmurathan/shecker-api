from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import CourierFridgePermission, FridgeProduct


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsLocalAdminOfFridgeForProduct(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_local_admin

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.is_local_admin:
            permitted_product_ids = FridgeProduct.objects.filter(fridge__owner=request.user).values_list('product_id',
                                                                                                         flat=True)
            return obj.id in permitted_product_ids

        return False


class IsLocalAdminOfFridge(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_local_admin

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_local_admin and obj.owner == request.user


class IsLocalAdminOfFridgeOwnerForFridgeProduct(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_local_admin

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_local_admin and obj.fridge.owner == request.user


class IsStaffReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff and request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_staff and request.method in SAFE_METHODS


class IsStaffUserFridgeCourierForFridgeProduct(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_staff:
            return CourierFridgePermission.objects.filter(user=request.user, fridge=obj.fridge).exists()
        return False
