from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from api.models import FridgeProduct, Fridge
from api.permissions import IsStaffUser
from api.modules.fridge.serializers import (
    FridgeProductCoverSerializer,
    FridgeAdminSerializer,
    FridgeAdminCoverSerializer
)


class FridgeProductsListAPIView(generics.ListAPIView):
    serializer_class = FridgeProductCoverSerializer

    def get_queryset(self):
        fridge_account = self.kwargs.get('account')
        return FridgeProduct.objects.filter(fridge__account=fridge_account)


class FridgeAdminModelViewSet(ModelViewSet):
    permission_classes = [IsStaffUser]
    queryset = Fridge.objects.all()
    serializer_class = FridgeAdminSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FridgeAdminCoverSerializer

        return super().get_serializer_class()

