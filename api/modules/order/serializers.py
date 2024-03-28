from rest_framework import serializers

from api.models import OrderProduct, Order


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderProductsCoverSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='fridge_product.product.name')
    product_price = serializers.IntegerField(source='fridge_product.product.price')

    class Meta:
        model = OrderProduct
        fields = ['product_name', 'product_price']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductsCoverSerializer(source='orderproduct_set', many=True)

    class Meta:
        model = Order
        fields = ['id', 'date', 'order_products']

