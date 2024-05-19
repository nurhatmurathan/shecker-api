from rest_framework import routers

from django.urls import path, include
from api.modules.fridge.views import (
    FridgeProductsListAPIView,
    FridgeAdminModelViewSet,
    FridgeReadOnlyModelViewSet
)


fridge_admin_router = routers.SimpleRouter()
fridge_admin_router.register(r'', FridgeAdminModelViewSet)

fridge_user_router = routers.SimpleRouter()
fridge_user_router.register(r'', FridgeReadOnlyModelViewSet)


urlpatterns = [
    path('<str:account>/products/', FridgeProductsListAPIView.as_view(), name='fridge-products-list'),
    path('admin/', include(fridge_admin_router.urls)),
    path('user/', include(fridge_user_router.urls))
]
