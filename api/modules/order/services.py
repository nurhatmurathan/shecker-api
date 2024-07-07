from datetime import timedelta
from django.utils import timezone

from api.models import Order
from api.modules.order.serializers import (
    OrderProductSerializer,
    OrderProductCoverSerializer,
    OrderSerializer
)
from api.modules.fridgeproduct import services as fridgeproduct_services


def create_instance():
    return Order.objects.create(status=Order.Status.PENDING)


def get_serialized_instance(order: Order):
    return OrderSerializer(order, many=False)


def get_instance(order_id: int):
    try:
        return Order.objects.select_related('transaction') \
            .get(id=order_id)
    except Order.DoesNotExist:
        return None


def create_order_and_order_details(basket_products: []):
    order: Order = create_instance()

    for product in basket_products:
        product['order'] = order.id

        serializer = OrderProductSerializer(data=product, many=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        fridgeproduct_services.check_product_availability(instance)

    return order


def reduce_quantity_of_product(order: Order):
    order_products = order.orderproduct_set.all()

    for order_product in order_products:
        fridgeproduct_services.check_product_availability(order_product)
        order_product.fridge_product.reduce_quantity(order_product.amount)


def get_product_list_of_order(order: Order):
    order_products = order.orderproduct_set.all()
    return OrderProductCoverSerializer(order_products, many=True).data


def get_total_price_of_order(order: Order):
    return order.calculate_total_sum()


def set_order_status(order: Order, status: Order.Status):
    order.set_status(status)


def set_order_date(order, date):
    order.set_date(date)


def get_status_of_order_response(order: Order, command):
    if (command == "check" and order.status in (Order.Status.PENDING, Order.Status.CHECKED)) or \
            (command == "pay" and order.status == Order.Status.CHECKED):
        return {
            'result': 0,
            'comment': 'Ok'
        }

    order_status_error_msg = {
        Order.Status.PENDING: {
            'result': 1,
            'comment': 'Order not checked'
        },
        Order.Status.CHECKED: {
            'result': 4,
            'comment': 'Payment in processing'
        },
        Order.Status.SUCCESS: {
            'result': 3,
            'comment': 'Order already paid'
        },
        Order.Status.FAILED: {
            'result': 2,
            'comment': 'Order canceled'
        }
    }

    other_error = {
        'result': 5,
        'comment': 'Other provider error'
    }

    return order_status_error_msg.get(order.status, other_error)


def get_order_not_found_exception_response():
    return {
        'result': 2,
        'comment': 'The order not found.'
    }


def get_incorrect_total_price_exception_response(order):
    return {
        'result': 5,
        'comment': 'Total price incorrect.'
    }


def is_total_price_incorrect(order, sum_from_bank) -> bool:
    sum_from_our_db = get_total_price_of_order(order)
    return sum_from_our_db != float(sum_from_bank)


def is_order_expired(order) -> bool:
    current_date = timezone.now()
    current_date_utc = current_date.replace(tzinfo=None)

    time_difference = current_date_utc - order.date.replace(tzinfo=None)

    return time_difference > timedelta(minutes=1)


def get_order_expired_exception_response():
    return {
        'result': 2,
        'comment': 'Time is up, order canceled.'
    }
