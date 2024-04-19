from rest_framework import routers

from django.urls import path, include
from api.modules.fridge.views import (
    FridgeProductsListAPIView,
    FridgeAdminModelViewSet
)


fridge_admin_router = routers.SimpleRouter()
fridge_admin_router.register(r'admin', FridgeAdminModelViewSet)


urlpatterns = [
    path('<str:account>/products/', FridgeProductsListAPIView.as_view(), name='fridge-products-list'),
    path('', include(fridge_admin_router.urls))
]
