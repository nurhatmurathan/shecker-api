from rest_framework.exceptions import ValidationError
from api.models import OrderProduct


def check_product_availability(order_product: OrderProduct):
    if order_product.fridge_product.quantity < order_product.amount:
        raise ValidationError(f'Product {order_product.fridge_product.product.name}, '
                              f'only {order_product.fridge_product.quantity} in stock')


