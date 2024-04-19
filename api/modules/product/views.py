from rest_framework.viewsets import ModelViewSet

from api.models import Product
from api.permissions import IsStaffUser, IsSuperUser
from api.modules.product.serializers import (
    ProductSerializer,
    ProductCoverSerializer,
)


class ProductAdminModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsStaffUser, IsSuperUser]
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductCoverSerializer

        return super().get_serializer_class()

