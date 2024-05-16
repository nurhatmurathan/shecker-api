from datetime import timedelta
from django.utils import timezone

from api.models import Transaction
from config import settings


def get_or_create_instance(order_id,  check_txn_id):
    try:
        return Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return Transaction.objects.create(
            order_id=order_id,
            check_txn_id=check_txn_id
        )


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


def is_transaction_expired(transaction) -> bool:
    current_date = timezone.now()
    current_date_utc = current_date.replace(tzinfo=None)

    time_difference = current_date_utc - transaction.expiration_time.replace(tzinfo=None)

    return time_difference > timedelta(seconds=15)


def handle_transaction_expired_exception():
    return {
        'result': 2,
        'comment': 'Time is up, transaction canceled.'
    }
