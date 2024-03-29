from api.models import OrderProduct, Order

from api.modules.order.serializers import \
    OrderProductSerializer, \
    OrderProductCoverSerializer
from api.modules.product import services


def create_order():
    return Order.objects.create(status=Order.Status.PENDING)


def get_order(order_id: int):
    try:
        return Order.objects.select_related('transaction')\
            .get(id=order_id)
    except Order.DoesNotExist:
        return None


def create_order_and_order_details(basket_products: []):
    order: Order = create_order()

    for product in basket_products:
        product['order'] = order.id

        serializer = OrderProductSerializer(data=product, many=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        services.check_product_availability(instance)

    return order


def get_product_list_of_order(order: Order):
    order_products = order.orderproduct_set.all()
    return OrderProductCoverSerializer(order_products, many=True).data


def get_total_price_of_order(order: Order):
    return order.calculate_total_sum()


def set_order_status(order: Order, status: Order.Status):
    order.set_status(status)
