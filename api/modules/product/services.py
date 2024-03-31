from rest_framework.exceptions import ValidationError

from api.models import OrderProduct
from api.modules.product.serializers import ProductCoverSerializer


def get_serialized_instance(order_product: OrderProduct):
    return ProductCoverSerializer(
        order_product.fridge_product.product,
        many=False
    )


def check_product_availability(order_product: OrderProduct):
    if order_product.fridge_product.quantity < order_product.amount:
        raise ValidationError(f'Product {order_product.fridge_product.product.name}, '
                              f'only {order_product.fridge_product.quantity} in stock')


def reduce_quantity(order_product: OrderProduct):
    order_product.fridge_product.quantity -= order_product.amount
    order_product.fridge_product.save()


# def test_services():
#     raise ValidationError("Okay")