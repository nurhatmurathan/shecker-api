from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.db import transaction

from api.models import Order
from api.permissions import IsSuperAdmin
from api.paginations import OrderAdminPagination
from api.utils import get_data
from api.modules.order import services
from api.modules.order.serializers import OrderDetailSerializer, OrderSerializer, BasketSerializer, \
    OrderAdminCoverSerializer, OrderAdminListSerializer


class OrderAPIView(APIView):
    @extend_schema(
        request=BasketSerializer,
        responses=OrderSerializer,
    )
    def post(self, request):
        request = self.request

        try:
            with transaction.atomic():
                basket_products = get_data(request.data, 'basket_products', ['fridge_product', 'amount'])
                order = services.create_order_and_order_details(basket_products)

                order_serializer = services.get_serialized_instance(order)
                return Response(data=order_serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception.args[0])}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'pk'


class OrderAdminReadonlyModelViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsSuperAdmin]
    queryset = Order.objects.all().order_by('date')
    serializer_class = OrderAdminListSerializer
    pagination_class = OrderAdminPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderAdminCoverSerializer

        return super().get_serializer_class()

