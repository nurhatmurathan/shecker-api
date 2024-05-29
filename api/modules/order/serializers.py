from rest_framework import serializers

from api.models import OrderProduct, Order
from api.modules.product.serializers import ProductSerializer

class OrderProductCoverSerializer(serializers.ModelSerializer):
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


class OrderSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    sum = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['account', 'sum', 'date']

    def get_account(self, obj):
        return obj.id

    def get_sum(self, obj):
        return obj.calculate_total_sum()


class OrderDetailSerializer(serializers.ModelSerializer):
    fridge_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'status', 'fridge_id', 'date']

    def get_fridge_id(self, obj):
        order_products = obj.orderproduct_set.all()
        if order_products.exists():
            return order_products.first().fridge_product.fridge.account

        return None


class OrderProductAdminSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='fridge_product.product')

    class Meta:
        model = OrderProduct
        fields = ['amount', 'product']


class OrderAdminCoverSerializer(serializers.ModelSerializer):
    total_sum = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    order_products = OrderProductAdminSerializer(source='orderproduct_set')

    class Meta:
        model = Order
        fields = ['id', 'total_sum', 'total_quantity',
                  'status', 'date', 'order_products']

    def get_total_sum(self, obj):
        return obj.calculate_total_sum()

    def get_total_quantity(self, obj):
        return obj.calculate_product_quantity()


class OrderAdminListSerializer(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'sum', 'quantity', 'status', 'date']

    def get_sum(self, obj):
        return obj.calculate_total_sum()

    def get_quantity(self, obj):
        return obj.calculate_product_quantity()


class BasketProductSerializer(serializers.Serializer):
    fridge_product = serializers.IntegerField()
    amount = serializers.IntegerField()


class BasketSerializer(serializers.Serializer):
    basket_products = BasketProductSerializer(many=True)
