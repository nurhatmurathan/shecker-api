from rest_framework import generics

from api.models import FridgeProduct
from api.modules.fridge.serializers import FridgeProductSerializer


class FridgeProductsListAPI(generics.ListAPIView):
    serializer_class = FridgeProductSerializer

    def get_queryset(self):
        fridge_account = self.kwargs.get('account')
        return FridgeProduct.objects.filter(fridge__account=fridge_account)
