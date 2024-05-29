from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
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


@extend_schema_view(
    list=extend_schema(
        tags=['Fridge'],
        parameters=[
            OpenApiParameter(name='account', type=OpenApiTypes.STR, location=OpenApiParameter.PATH, description='Fridge account'),
        ],
        description="List all products in a specific fridge",
        responses={200: FridgeProductCoverSerializer(many=True)}
    )
)
class FridgeProductsListAPIView(generics.ListAPIView):
    serializer_class = FridgeProductCoverSerializer

    def get_queryset(self):
        fridge_account = self.kwargs.get('account')
        return FridgeProduct.objects.filter(fridge__account=fridge_account)


@extend_schema_view(
    list=extend_schema(
        tags=['Fridge'],
        description="List all fridges",
        responses={200: FridgeListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['Fridge'],
        description="Retrieve details of a specific fridge",
        responses={200: FridgeSerializer}
    )
)
class FridgeReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Fridge.objects.all()
    serializer_class = FridgeListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FridgeSerializer

        return super().get_serializer_class()


@extend_schema_view(
    list=extend_schema(
        tags=['Fridge Admin'],
        description="List all fridges with admin access",
        responses={200: FridgeAdminSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['Fridge Admin'],
        description="Retrieve details of a specific fridge with admin access",
        responses={200: FridgeAdminCoverSerializer}
    ),
    create=extend_schema(
        tags=['Fridge Admin'],
        description="Create a new fridge",
        responses={201: FridgeAdminSerializer}
    ),
    update=extend_schema(
        tags=['Fridge Admin'],
        description="Update an existing fridge",
        responses={200: FridgeAdminSerializer}
    ),
    partial_update=extend_schema(
        tags=['Fridge Admin'],
        description="Partially update an existing fridge",
        responses={200: FridgeAdminSerializer}
    ),
    destroy=extend_schema(
        tags=['Fridge Admin'],
        description="Delete a fridge",
        responses={204: None}
    )
)
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
