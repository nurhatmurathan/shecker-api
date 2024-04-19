from rest_framework import serializers

from api.models import FridgeProduct
from api.modules.product.serializers import ProductSerializer


class FridgeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = "__all__"


class FridgeProductListSerializer(serializers.ModelSerializer):
    account = serializers.CharField(source='fridge.account')
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.IntegerField(source='product.price')

    class Meta:
        model = FridgeProduct
        fields = ['id', 'account', 'product_name', 'product_price', 'quantity']


class FridgeProductCoverSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = FridgeProduct
        fields = ['id', 'quantity', 'product']
