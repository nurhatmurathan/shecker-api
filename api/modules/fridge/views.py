from rest_framework import generics
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.models import FridgeProduct, Fridge, CourierFridgePermission
from api.permissions import *
from api.modules.fridge.serializers import (
    FridgeSerializer,
    FridgeListSerializer,
    FridgeProductCoverSerializer,
    FridgeAdminSerializer,
    FridgeAdminCoverSerializer
)


class FridgeProductsListAPIView(generics.ListAPIView):
    serializer_class = FridgeProductCoverSerializer

    def get_queryset(self):
        fridge_account = self.kwargs.get('account')
        return FridgeProduct.objects.filter(fridge__account=fridge_account)


class FridgeReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Fridge.objects.all()
    serializer_class = FridgeListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FridgeSerializer

        return super().get_serializer_class()


class FridgeAdminModelViewSet(ModelViewSet):
    queryset = Fridge.objects.all()
    serializer_class = FridgeAdminSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FridgeAdminCoverSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['list', 'retrieve']:
            permission_classes += [
                IsSuperAdmin |
                IsLocalAdminOfFridge |
                IsStaffReadOnly
            ]
        elif self.action in ['update', 'partial_update']:
            permission_classes += [IsSuperAdmin | IsLocalAdminOfFridge]
        elif self.action in ['create', 'destroy']:
            permission_classes += [IsSuperAdmin]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Fridge.objects.all()
        elif user.is_local_admin:
            return Fridge.objects.filter(owner=user)
        elif user.is_staff:
            permitted_fridge_ids = CourierFridgePermission.objects.filter(user=user).values_list('fridge_id', flat=True)
            return Fridge.objects.filter(id__in=permitted_fridge_ids)

        return Fridge.objects.none()
