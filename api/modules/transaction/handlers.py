from abc import ABC, abstractmethod

from django.utils import timezone


from api.modules.order import services as order_services
from api.models import Order
from config import settings


class CommandHandler(ABC):
    @abstractmethod
    def pre_process(self, request, transaction):
        pass

    @abstractmethod
    def handle(self, request, order, transaction):
        pass


class CheckCommandHandler(CommandHandler):
    def pre_process(self, request, transaction):
        txn_id = request.query_params.get('txn_id')
        transaction.set_check_txn_id(txn_id)

    def handle(self, request, order, transaction):
        product_list = order_services.get_product_list_of_order(order)
        total_price = order_services.get_total_price_of_order(order)

        order_services.set_order_date(order, timezone.now())
        order_services.set_order_status(order, Order.Status.CHECKED)
        return {
            'txn_id': transaction.check_txn_id,
            'sum': f"{total_price}.00",
            'result': 0,
            'bin': settings.BIN,
            'comment': "OK",
            'fields': {
                'products': product_list,
            }
        }


class PayCommandHandler(CommandHandler):
    def pre_process(self, request, transaction):
        txn_id = request.query_params.get('txn_id')
        txn_date = request.query_params.get('txn_date')
        transaction.set_pay_txn_id_and_date(txn_id, txn_date)

    def handle(self, request, order, transaction):
        sum_from_bank = request.query_params.get('sum')

        order_services.reduce_quantity_of_product(order)
        order_services.set_order_date(order, timezone.now())
        order_services.set_order_status(order, Order.Status.SUCCESS)
        return {
            'txn_id': transaction.pay_txn_id,
            'prv_txn_id': transaction.pk,
            'result': 0,
            'sum': float(sum_from_bank),
            'bin': settings.BIN,
            'comment': "Success",
        }
