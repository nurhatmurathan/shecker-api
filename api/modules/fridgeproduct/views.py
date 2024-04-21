from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from django.db.models import Q
from django.db import transaction

from api.utils import get_data
from api.models import FridgeProduct
from api.permissions import IsStaffUser, IsSuperUser
from api.modules.fridgeproduct.services import create_or_update_instances
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

    @action(methods=['post'], detail=False, url_path='create-update')
    def create_update(self, request):
        request = self.request

        try:
            with transaction.atomic():
                fridge_products = get_data(request.data, 'fridge_products', ['quantity', 'product', 'fridge'])
                fridge_products_serialized_data = create_or_update_instances(fridge_products)

                return Response(data=fridge_products_serialized_data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception)}, status=status.HTTP_400_BAD_REQUEST)