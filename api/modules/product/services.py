from api.models import OrderProduct
from api.modules.product.serializers import ProductCoverSerializer


def get_serialized_instance(order_product: OrderProduct):
    return ProductCoverSerializer(
        order_product.fridge_product.product,
        many=False
    )