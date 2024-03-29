from api.models import OrderProduct, Order

from api.modules.order.serializers import OrderProductSerializer, OrderSerializer
from api.modules.product import services


def create_order():
    return Order.objects.create(status=Order.Status.PENDING)


def get_serialized_order(order: Order):
    return OrderSerializer(order, many=False)


def create_order_and_order_details(basket_products: []):
    order: Order = create_order()

    for product in basket_products:
        product['order'] = order.id

        serializer = OrderProductSerializer(data=product, many=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        services.check_product_availability(instance)

    return order


def get_total_price_and_product_list_of_order(order_id: int):
    order_products = OrderProduct.objects.filter(order_id=order_id)

    price_sum: int = 0
    products: list = []

    for order_product in order_products:
        services.check_product_availability(order_product)

        price_sum += order_product.fridge_product.product.price * order_product.amount
        products.append(services.get_serialized_product(order_product))

    return price_sum, products
