from rest_framework import routers

from django.urls import path, include
from api.modules.product.views import (
    ProductAdminModelViewSet,
)

product_admin_router = routers.SimpleRouter()
product_admin_router.register(r'admin', ProductAdminModelViewSet)

urlpatterns = [
    path('', include(product_admin_router.urls))
]
