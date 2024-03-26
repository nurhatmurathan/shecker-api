from rest_framework import serializers

from api.models import OrderProduct


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
