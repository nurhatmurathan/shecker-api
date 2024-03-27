from rest_framework import serializers

from api.models import OrderProduct, Order


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

