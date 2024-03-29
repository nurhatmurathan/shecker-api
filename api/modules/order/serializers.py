from rest_framework import serializers

from api.models import OrderProduct, Order


class OrderProductCoverKaspiSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = ['name', 'price', 'amount']

    def get_name(self, obj):
        return obj.fridge_product.product.name

    def get_price(self, obj):
        return obj.fridge_product.product.price


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
    account = serializers.SerializerMethodField()
    sum = serializers.SerializerMethodField()
    # order_products = OrderProductsCoverSerializer(source='orderproduct_set', many=True)

    class Meta:
        model = Order
        fields = ['account', 'sum', 'date']

    def get_account(self, obj):
        return obj.id

    def get_sum(self, obj):
        return obj.calculate_total_sum()
