from rest_framework import routers

from django.urls import path, include
from api.modules.fridgeproduct.views import (
    FridgeProductAdminModelViewSet
)

fridge_product_admin_router = routers.SimpleRouter()
fridge_product_admin_router.register(r'admin', FridgeProductAdminModelViewSet, basename='fridgeproduct')


urlpatterns = [
    path('', include(fridge_product_admin_router.urls)),
]
