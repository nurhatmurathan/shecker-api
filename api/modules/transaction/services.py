from api.models import Transaction


def get_or_create_transaction(order_id: int,  check_txn_id: int):
    try:
        return Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return Transaction.objects.create(
            order_id=order_id,
            check_txn_id=check_txn_id
        )


def generate_exception_json(txn_id: int, comment: str):
    return {
        'txn_id': txn_id,
        'result': 1,
        'BIN': None,
        'comment': comment,
    }