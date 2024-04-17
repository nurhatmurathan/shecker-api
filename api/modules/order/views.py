from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from api.models import Order
from api.modules.order import services
from api.modules.order.serializers import OrderDetailSerializer


class OrderAPIView(APIView):
    def post(self, request):
        request = self.request

        try:
            with transaction.atomic():

                basket_products = self._get_basket_details(request.data)
                order = services.create_order_and_order_details(basket_products)

                order_serializer = services.get_serialized_instance(order)
                return Response(data=order_serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception.args[0])}, status=status.HTTP_400_BAD_REQUEST)

    def _get_basket_details(self, data):
        if 'basket_products' not in data:
            raise NotFound("Request is must contains basket information.")

        product_list = data.get('basket_products', [])
        all_required_fields_present = all(
            all(field in item for field in ['fridge_product', 'amount'])
            for item in product_list
        )

        if not all_required_fields_present:
            raise NotFound("Not all fields contains in form. Form must contains ['fridge_product', 'amount'] "
                           "fields.")

        return product_list


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'pk'
