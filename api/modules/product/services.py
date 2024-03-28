from rest_framework.exceptions import ValidationError

from api.models import OrderProduct
from api.modules.product.serializers import ProductCoverSerializer

from typing import Iterable


def get_product_list_of_given_order(order_products: Iterable[OrderProduct]):
    products = []

    for order_product in order_products:
        product_serializer = ProductCoverSerializer(
                order_product.fridge_product.product,
                many=False
        )
        products.append(product_serializer)

    return products


def check_product_availability(order_product: OrderProduct):
    if order_product.fridge_product.quantity < order_product.amount:
        raise ValidationError(f'Product {order_product.fridge_product.product.name}, '
                              f'only {order_product.fridge_product.quantity} in stock')
