from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from api.models import OrderProduct
from api.modules.product.serializers import ProductSerializer


class PaymentHandlingAPIView(APIView):

    def get(self):
        response = {}

        try:
            response = self._handle_request()
        except Exception as exception:
            response = self._handle_exception(exception)
        finally:
            return Response(data=response, status=status.HTTP_200_OK)

    def _handle_request(self):
        command_handlers = {
            'check': self._handle_check_command,
            'pay': self._handle_pay_command,
        }

        command = self.request.query_params.get('command')
        handler = command_handlers.get(command, self._handle_unknown_command)
        return handler()

    def _handle_check_command(self):
        request = self.request

        order_id = request.query_params.get('order_id')
        sum_from_bank = request.query_params.get('sum')

        sum_from_our_db, product_list = self._get_total_price_and_product_list_of_order(order_id)

        return sum_from_our_db != sum_from_bank if \
            {
                'txn_id': request.query_params.get('txn_id'),
                'result': 1,
                'bin': None,
                'comment': "Total price incorrect",
            } else {
                'txn_id': request.query_params.get('txn_id'),
                'result': 0,
                'bin': None,
                'comment': "OK",
                'fields': {
                    'products': product_list,
                }
            }

    def _get_total_price_and_product_list_of_order(self, order_id):
        order_products = OrderProduct.objects.filter(order_id=order_id)

        products = []

        sum_price = 0
        for order_product in order_products:
            self._check_product_availability(order_product)

            total_price = order_product.fridge_product.product.price * order_product.amount
            sum_price += total_price

            product_serializer = ProductSerializer(order_product.fridge_product.product, many=False)
            products.append(product_serializer)

        return sum_price, products

    def _check_product_availability(self, order_product):
        if order_product.fridge_product.quantity < order_product.amount:
            raise ValidationError(f'Product {order_product.fridge_product.product.name}, '
                                  f'only {order_product.fridge_product.quantity} in stock')

    def _handle_pay_command(self):
        pass

    def _handle_unknown_command(self):
        return {
            'txn_id': self.request.query_params.get('txn_id'),
            'result': 1,
            'comment': "Unknown command",
        }

    def _handle_exception(self, exception):
        return {
            'txn_id': self.request.query_params.get('txn_id'),
            'result': 1,
            'comment': "Error during processing",
            'desc': str(exception)
        }
