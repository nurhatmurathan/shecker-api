from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction as db_transaction

from api.models import Order
from api.modules.order import services as order_services
from api.modules.transaction import services as transaction_services
from config import settings


class PaymentHandlingAPIView(APIView):

    def get(self, request):
        response = {}

        try:
            with db_transaction.atomic():
                response = self._handle_request()
        except Exception as exception:
            response = self._handle_exception(exception.args[0])
        finally:
            return Response(data=response, status=status.HTTP_200_OK)

    def _handle_request(self):
        request = self.request

        command_handlers = {
            'check': self._handle_check_command,
            'pay': self._handle_pay_command,
        }

        command = self.request.query_params.get('command')
        handler = command_handlers.get(command, None)

        if handler is None:
            return self._handle_unknown_command()

        order_id = request.query_params.get('account')
        sum_from_bank = request.query_params.get('sum')
        txn_id = request.query_params.get('txn_id')
        txn_date = request.query_params.get('txn_date', None)

        order = order_services.get_instance(order_id)
        if order is None:
            return self._order_not_found(txn_id)

        msg = order_services.handle_status_of_order(order, command)
        if msg.get('result') != 0:
            order_services.set_order_status(order, Order.Status.FAILED)
            return transaction_services.generate_exception_json(
                txn_id,
                msg.get('result'),
                msg.get('comment')
            )

        return handler(sum_from_bank, txn_id, txn_date, order)

    def _handle_check_command(self, sum_from_bank, check_txn_id, txn_date, order):
        transaction = transaction_services.get_or_create_instance(order.id, check_txn_id)

        product_list = order_services.get_product_list_of_order(order)
        total_price = order_services.get_total_price_of_order(order)
        order_services.set_order_status(order, Order.Status.CHECKED)
        return {
            'txn_id': transaction.check_txn_id,
            'sum': str(total_price) + ".00",
            'result': 0,
            'bin': settings.BIN,
            'comment': "OK",
            'fields': {
                'products': product_list,
            }
        }

    def _handle_pay_command(self, sum_from_bank, pay_txn_id, txn_date, order):
        transaction_services.set_pay_txn_id_and_date(order.transaction, pay_txn_id, txn_date)

        if self._is_total_price_incorrect(order, sum_from_bank):
            return self._total_price_incorrect(order, pay_txn_id)

        order_services.reduce_quantity_of_product(order)
        order_services.set_order_status(order, Order.Status.PAYED)

        return {
            'txn_id': order.transaction.pay_txn_id,
            'prv_txn_id': order.transaction.pk,
            'result': 0,
            'sum': float(sum_from_bank),
            'bin': settings.BIN,
            'comment': "Success",
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
            'result': 6,
            'comment': "Error during processing",
            'desc': str(exception)
        }

    def _order_not_found(self, txn_id):
        return transaction_services. \
            generate_exception_json(txn_id, 1, 'The order not found.')

    def _total_price_incorrect(self, order, txn_id):
        order_services.set_order_status(order, Order.Status.FAILED)
        return transaction_services.generate_exception_json(txn_id, 5, 'Total price incorrect.')

    def _is_total_price_incorrect(self, order, sum_from_bank):
        sum_from_our_db = order_services.get_total_price_of_order(order)
        return sum_from_our_db != float(sum_from_bank)
