from datetime import timedelta
from django.utils import timezone

from api.models import Transaction, Order
from api.modules.transaction.handlers import CheckCommandHandler, PayCommandHandler
from config import settings

from api.modules.order import services as order_services


def get_or_create_instance(order_id):
    try:
        return Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return Transaction.objects.create(order_id=order_id)


def get_instance_by_order_id(order_id):
    try:
        return Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return None


def generate_exception_json(txn_id, result, comment):
    return {
        'txn_id': txn_id,
        'result': result,
        'BIN': settings.BIN,
        'comment': comment,
    }


def set_pay_txn_id_and_date(transaction: Transaction, pay_txn_id, txn_date):
    transaction.set_pay_txn_id_and_date(pay_txn_id, txn_date)


def set_check_txn_id(transaction: Transaction, check_txn_id):
    transaction.set_check_txn_id(check_txn_id)


def is_transaction_expired(transaction) -> bool:
    current_date = timezone.now()
    current_date_utc = current_date.replace(tzinfo=None)

    time_difference = current_date_utc - transaction.expiration_time.replace(tzinfo=None)

    return time_difference > timedelta(minutes=1)


def get_transaction_expired_exception_response():
    return {
        'result': 2,
        'comment': 'Time is up, transaction canceled.'
    }


class PaymentHandlingService:
    def __init__(self):
        self.command_handlers = {
            'check': CheckCommandHandler(),
            'pay': PayCommandHandler(),
        }

    def handle_request(self, request):
        command = request.query_params.get('command')
        handler = self.command_handlers.get(command)

        if handler is None:
            return self._handle_unknown_command(request)

        order_id = request.query_params.get('account')
        txn_id = request.query_params.get('txn_id')
        sum_from_bank = request.query_params.get('sum')

        order = order_services.get_instance(order_id)
        if order is None:
            response = order_services.get_order_not_found_exception_response()
            return self._generate_exception_json(response, txn_id)

        response = order_services.get_status_of_order_response(order, command)
        if response.get('result') != 0:
            order_services.set_order_status(order, Order.Status.FAILED)
            return self._generate_exception_json(response, txn_id)

        transaction = get_or_create_instance(order.id)
        handler.pre_process(request, transaction)

        if order_services.is_order_expired(order):
            order_services.set_order_status(order, Order.Status.FAILED)
            response = order_services.get_order_expired_exception_response()
            return self._generate_exception_json(response, txn_id)

        if is_transaction_expired(transaction):
            order_services.set_order_status(order, Order.Status.FAILED)
            response = get_transaction_expired_exception_response()
            return self._generate_exception_json(response, txn_id)

        if command == 'pay' and order_services.is_total_price_incorrect(order, sum_from_bank):
            order_services.set_order_status(order, Order.Status.FAILED)
            response = order_services.get_incorrect_total_price_exception_response(order)
            return self._generate_exception_json(response, txn_id)

        return handler.handle(request, order, transaction)

    @staticmethod
    def _handle_unknown_command(request):
        return {
            'txn_id': request.query_params.get('txn_id'),
            'result': 1,
            'comment': "Unknown command",
        }

    @staticmethod
    def _generate_exception_json(response, txn_id):
        return generate_exception_json(
            txn_id,
            response.get('result'),
            response.get('comment')
        )
