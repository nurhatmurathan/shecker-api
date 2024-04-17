from api.models import Transaction
from config import settings


def get_or_create_instance(order_id,  check_txn_id):

    try:

        transaction = Transaction.objects.get(order_id=order_id)

        if transaction:
            return transaction

        return Transaction.objects.create(
            order_id=order_id,
            check_txn_id=check_txn_id
        )
    except:
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
