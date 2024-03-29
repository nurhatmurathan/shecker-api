from rest_framework import serializers

from api.models import Product, FridgeProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', ]


class ProductCoverSerializer(serializers.ModelSerializer):
    class Meat:
        model = Product
        fields = ['id', 'name', 'price']
