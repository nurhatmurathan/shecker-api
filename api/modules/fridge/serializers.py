from rest_framework import serializers

from api.models import FridgeProduct
from api.modules.product.serializers import ProductSerializer


class FridgeProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = FridgeProduct
        fields = ['id', 'quantity', 'product']
