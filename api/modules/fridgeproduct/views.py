from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from django.db.models import Q
from django.db import transaction

from api.utils import get_data
from api.models import FridgeProduct, CourierFridgePermission
from api.permissions import *
from api.modules.fridgeproduct.services import create_or_update_instances
from api.modules.fridgeproduct.serializers import (
    FridgeProductSerializer,
    FridgeProductCoverSerializer,
    FridgeProductListSerializer
)


class FridgeProductAdminModelViewSet(ModelViewSet):
    serializer_class = FridgeProductSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['quantity', 'product__price']
    search_fields = ['product__name', 'product__description']

    def get_serializer_class(self):
        if self.action == 'list':
            return FridgeProductListSerializer
        elif self.action == 'retrieve':
            return FridgeProductCoverSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update']:
            permission_classes += [
                IsSuperAdmin |
                IsLocalAdminOfFridgeOwnerForFridgeProduct |
                IsStaffUserFridgeCourierForFridgeProduct
            ]
        elif self.action == 'destroy':
            permission_classes += [
                IsSuperAdmin |
                IsLocalAdminOfFridgeOwnerForFridgeProduct
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        filter_params = {
            'min_price': self.request.query_params.get("min_price"),
            'max_price': self.request.query_params.get("max_price"),
            'fridge': self.request.query_params.get("fridge"),
        }

        queryset = FridgeProduct.objects.select_related('product').all()
        if not user.is_superuser and user.is_local_admin:
            queryset = queryset.filter(fridge__owner=user)
        elif not user.is_superuser and user.is_staff:
            permitted_fridge_ids = CourierFridgePermission.objects.filter(user=user).values_list('fridge_id', flat=True)
            queryset = queryset.filter(fridge_id__in=permitted_fridge_ids)

        filters = Q()
        if filter_params['min_price']:
            filters &= Q(price__gte=int(filter_params['min_price']))
        if filter_params['max_price']:
            filters &= Q(price__lte=int(filter_params['max_price']))
        if filter_params['fridge']:
            filters &= Q(fridge_id=int(filter_params['fridge']))

        return queryset.filter(filters)

    @action(methods=['post'], detail=False,
            url_path='create-update',
            permission_classes=[
                                IsSuperAdmin,
                                IsStaffUserFridgeCourierForFridgeProduct,
                                IsLocalAdminOfFridgeOwnerForFridgeProduct
                            ]
            )
    def create_update(self, request):
        request = self.request

        try:
            with transaction.atomic():
                fridge_products = get_data(request.data, 'fridge_products', ['quantity', 'product', 'fridge'])
                fridge_products_serialized_data = create_or_update_instances(fridge_products)

                return Response(data=fridge_products_serialized_data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=FridgeProductListSerializer,
        parameters=[
            OpenApiParameter(name='min_price', description='filter min price', required=True, type=int),
            OpenApiParameter(name='max_price', description='filter max price', required=True, type=int),
            OpenApiParameter(name='fridge', description='fridge id', required=True, type=int)
        ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=FridgeProductCoverSerializer
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
