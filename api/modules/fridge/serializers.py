from rest_framework import serializers

from api.models import Fridge
from api.modules.fridgeproduct.serializers import FridgeProductCoverSerializer


class FridgeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = "__all__"


class FridgeAdminCoverSerializer(serializers.ModelSerializer):
    products = FridgeProductCoverSerializer(source='fridgeproduct_set', many=True)

    class Meta:
        model = Fridge
        fields = ['account', 'description', 'products']
