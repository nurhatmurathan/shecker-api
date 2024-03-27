from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import OrderProduct, Order
from api.modules.order.serializers import OrderProductCoverKaspiSerializer


class PaymentHandlingAPIView(APIView):

    def get(self, request):
        response = {}

        try:
            response = self._handle_request()
        except Exception as exception:
            response = self._handle_exception(exception)

        return Response(data=response, status=status.HTTP_200_OK)

    def _handle_request(self):
        command_handlers = {
            'check': self._handle_check_command,
            'pay': self._handle_pay_command,
        }

        command = self.request.query_params.get('command')
        handler = command_handlers.get(command, 0)

        if not handler:
            return self._handle_unknown_command()


        request = self.request
        order_id = request.query_params.get('account')
        sum_from_bank = request.query_params.get('sum')
        kaspi_txn_id = request.query_params.get('txn_id')
        kaspi_txn_date = request.query_params.get('txn_date')
        order_instance = Order.objects.select_related('transaction').get(id=order_id)

        return handler(sum_from_bank, kaspi_txn_id, kaspi_txn_date, order_instance)

    def _handle_check_command(self, sum_from_bank, kaspi_txn_id, kaspi_txn_date, order_instance):

        sum_from_our_db, product_list_data = self._get_total_price_and_product_list_of_order(order_instance.id)

        if sum_from_our_db != float(sum_from_bank):
            return {
                'txn_id': kaspi_txn_id,
                'result': 1,
                'bin': None,
                'comment': "Total price incorrect",
            }

        order_instance.set_status("CHECKED")
        order_instance.transaction.set_check_txn_id(kaspi_txn_id)

        return {
            'txn_id': kaspi_txn_id,
            'result': 0,
            'bin': None,
            'comment': "OK",
            'fields': {
                'products': product_list_data,
            }
        }

    def _get_total_price_and_product_list_of_order(self, order_id):
        order_products = OrderProduct.objects.select_related('fridge_product__fridge',
                                                             'fridge_product__product').filter(order_id=order_id)
        sum_price = 0

        for order_product in order_products:
            total_price = order_product.fridge_product.product.price * order_product.amount
            sum_price += total_price

        return sum_price, OrderProductCoverKaspiSerializer(order_products, many=True).data

    def _handle_pay_command(self, sum_from_bank, kaspi_txn_id, kaspi_txn_date, order_instance):

        order_instance.set_status("PAYED")
        order_instance.transaction.set_pay_txn_id_and_date(kaspi_txn_id, kaspi_txn_date)

        return {
            'txn_id': kaspi_txn_id,
            'prv_txn_id': order_instance.transaction.pk,
            'result': 0,
            'sum': str(sum_from_bank)+".00",
            'bin': None,
            'comment': "Pay",
        }

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
