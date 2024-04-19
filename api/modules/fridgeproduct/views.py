from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from django.db.models import Q

from api.models import FridgeProduct
from api.permissions import IsStaffUser, IsSuperUser
from api.modules.fridgeproduct.serializers import (
    FridgeProductSerializer,
    FridgeProductCoverSerializer,
    FridgeProductListSerializer
)


class FridgeProductAdminModelViewSet(ModelViewSet):
    serializer_class = FridgeProductSerializer
    permission_classes = [IsStaffUser, IsSuperUser]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['quantity', 'product__price']
    search_fields = ['product__name', 'product__description']

    def get_queryset(self):
        filter_params = {
            'min_price': self.request.query_params.get("min_price"),
            'max_price': self.request.query_params.get("max_price"),
        }

        queryset = FridgeProduct.objects.select_related('product')
        filters = Q()

        if filter_params['min_price']:
            filters &= Q(price__gte=int(filter_params['min_price']))
        if filter_params['max_price']:
            filters &= Q(price__lte=int(filter_params['max_price']))

        return queryset.filter(filters)

    def get_serializer_class(self):
        if self.action == 'list':
            return FridgeProductListSerializer
        elif self.action == 'retrieve':
            return FridgeProductCoverSerializer

        return super().get_serializer_class()

