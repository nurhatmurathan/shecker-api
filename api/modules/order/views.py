from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
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
        tags=['Order'],
        request=BasketSerializer,
        responses=OrderSerializer,
        description="Create a new order with the provided basket products."
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


@extend_schema_view(
    retrieve=extend_schema(
        tags=['Order'],
        description="Retrieve detailed information about a specific order by its primary key.",
        responses={200: OrderDetailSerializer}
    )
)
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'pk'


@extend_schema_view(
    list=extend_schema(
        tags=['Order Admin'],
        parameters=[
            OpenApiParameter(name='fridge_id', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by Fridge ID'),
            OpenApiParameter(name='product_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by Product ID'),
            OpenApiParameter(name='status', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by Status'),
        ],
        description="Retrieve a list of orders with optional filters for fridge, product, and status",
        responses={200: OrderAdminListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['Order Admin'],
        description="Retrieve a specific order by ID",
        responses={200: OrderAdminCoverSerializer}
    )
)
class OrderAdminReadonlyModelViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsSuperAdmin]
    serializer_class = OrderAdminListSerializer
    pagination_class = OrderAdminPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderAdminCoverSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-date')

        filter_params = {
            'fridge_id': self.request.query_params.getlist('fridge_id', None),
            'product_id': self.request.query_params.getlist('product_id', None),
            'status': self.request.query_params.get('status', None)
        }

        filters = Q()
        if filter_params['status']:
            filters &= Q(status=str(filter_params['status']).upper())
        if filter_params['fridge_id']:
            filters &= Q(orderproduct__fridge_product__fridge__account__in=filter_params['fridge_id'])
        if filter_params['product_id']:
            filters &= Q(orderproduct__fridge_product__product__id__in=filter_params['product_id'])

        return queryset.filter(filters).distinct()

