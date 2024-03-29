from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Order
from api.modules.order import services as order_services
from api.modules.transaction import services as transaction_services


class PaymentHandlingAPIView(APIView):

    def get(self, request):
        response = {}

        try:
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

        order = order_services.get_order(order_id)
        return handler(sum_from_bank, txn_id, txn_date, order)

    def _handle_check_command(self, sum_from_bank, check_txn_id, txn_date, order):
        print(sum_from_bank)
        print(check_txn_id)
        print(txn_date)
        print(order)

        if order is None:
            return self._order_not_found(check_txn_id)

        transaction = transaction_services.\
            get_or_create_transaction(order.id, check_txn_id)
        if transaction.pay_txn_id is not None:
            return self._order_already_paid(order, check_txn_id)

        if self._is_total_price_incorrect(order, sum_from_bank):
            return self._total_price_incorrect(order, check_txn_id)

        product_list = order_services.get_product_list_of_order(order)
        order_services.set_order_status(order, Order.Status.CHECKED)
        return {
            'txn_id': check_txn_id,
            'result': 0,
            'bin': None,
            'comment': "OK",
            'fields': {
                'products': product_list,
            }
        }

    def _handle_pay_command(self, sum_from_bank, pay_txn_id, txn_date, order):
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

    def _order_not_found(self, txn_id):
        return transaction_services.\
            generate_exception_json(txn_id, 'The order not found.')

    def _order_already_paid(self, order, txn_id):
        order_services.set_order_status(order, Order.Status.FAILED)
        return transaction_services.\
            generate_exception_json(txn_id, 'The order has already been paid.')

    def _total_price_incorrect(self, order, txn_id):
        order_services.set_order_status(order, Order.Status.FAILED)
        return transaction_services.generate_exception_json(txn_id, 'Total price incorrect.')

    def _is_total_price_incorrect(self, order, sum_from_bank):
        sum_from_our_db = order_services.get_total_price_of_order(order)
        return sum_from_our_db != int(sum_from_bank)
