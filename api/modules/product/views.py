from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models import Product
from api.permissions import *
from api.modules.product.serializers import (
    ProductSerializer,
    ProductCoverSerializer,
)


@extend_schema_view(
    list=extend_schema(
        tags=['Product Admin'],
        description="List all products",
        responses={200: ProductCoverSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['Product Admin'],
        description="Retrieve details of a specific product",
        responses={200: ProductSerializer}
    ),
    create=extend_schema(
        tags=['Product Admin'],
        description="Create a new product",
        responses={201: ProductSerializer}
    ),
    update=extend_schema(
        tags=['Product Admin'],
        description="Update an existing product",
        responses={200: ProductSerializer}
    ),
    partial_update=extend_schema(
        tags=['Product Admin'],
        description="Partially update an existing product",
        responses={200: ProductSerializer}
    ),
    destroy=extend_schema(
        tags=['Product Admin'],
        description="Delete a product",
        responses={204: None}
    )
)
class ProductAdminModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductCoverSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['list', 'retrieve']:
            permission_classes += [
                IsSuperAdmin |
                IsLocalAdminOfFridgeForProduct |
                IsStaffReadOnly
            ]
        elif self.action in ['destroy', 'create', 'update', 'partial_update']:
            permission_classes += [
                IsSuperAdmin |
                IsLocalAdminOfFridgeForProduct
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Product.objects.all()
        elif user.is_local_admin:
            permitted_product_ids = FridgeProduct.objects.filter(fridge__owner=user).values_list('product_id',
                                                                                                 flat=True)
            return Product.objects.filter(id__in=permitted_product_ids)
        elif user.is_staff:
            permitted_fridge_ids = CourierFridgePermission.objects.filter(user=user).values_list('fridge_id', flat=True)
            permitted_product_ids = FridgeProduct.objects.filter(fridge_id__in=permitted_fridge_ids).values_list(
                'product_id', flat=True)
            return Product.objects.filter(id__in=permitted_product_ids)

        return Product.objects.none()

