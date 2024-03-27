from api.models import OrderProduct, Order
from api.modules.product import services
from api.modules.order.serializers import OrderProductSerializer


def create_order():
    return Order.objects.create(status=Order.Status.PENDING)


def create_order_details(basket_products, order):
    for product in basket_products:
        product['order'] = order.id

        serializer = OrderProductSerializer(data=product, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()


def get_total_price_and_product_list_of_order(order_id):
    order_products = OrderProduct.objects.filter(order_id=order_id)

    sum_price = 0
    for order_product in order_products:
        services.check_product_availability(order_product)

        total_price = order_product.fridge_product.product.price * order_product.amount
        sum_price += total_price

    return sum_price, services.get_product_list_of_given_order(order_products)
