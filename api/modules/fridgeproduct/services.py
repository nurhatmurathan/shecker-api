from rest_framework.exceptions import ValidationError

from django.shortcuts import get_object_or_404

from api.modules.fridgeproduct.serializers import FridgeProductSerializer
from api.models import OrderProduct, FridgeProduct


def check_product_availability(order_product: OrderProduct):
    if order_product.fridge_product.quantity < order_product.amount:
        raise ValidationError(f'Product {order_product.fridge_product.product.name}, '
                              f'only {order_product.fridge_product.quantity} in stock')


def create_or_update_instances(fridge_products):
    serialized_instances = []

    for product in fridge_products:
        if 'id' in product:
            instance = get_object_or_404(FridgeProduct, id=product.get('id'))
            serializer = FridgeProductSerializer(instance=instance, data=product)
        else:
            serializer = FridgeProductSerializer(data=product)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        serialized_instances.append(serializer.data)

    return serialized_instances
