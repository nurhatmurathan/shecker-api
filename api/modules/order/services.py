from api.models import Order

from api.modules.order.serializers import (
    OrderProductSerializer,
    OrderProductCoverSerializer,
    OrderSerializer
)
from api.modules.product import services as product_services


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

        product_services.check_product_availability(instance)

    return order


def reduce_quantity_of_product(order: Order):
    order_products = order.orderproduct_set.all()

    for order_product in order_products:
        product_services.check_product_availability(order_product)
        product_services.reduce_quantity(order_product)


def get_product_list_of_order(order: Order):
    order_products = order.orderproduct_set.all()
    return OrderProductCoverSerializer(order_products, many=True).data


def get_total_price_of_order(order: Order):
    return order.calculate_total_sum()


def set_order_status(order: Order, status: Order.Status):
    order.set_status(status)


def handle_status_of_order(order: Order, command):
    if (command == "check" and order.status == Order.Status.PENDING) or \
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
        Order.Status.PAYED: {
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


#
# def test_services():
#     product_services.test_services()