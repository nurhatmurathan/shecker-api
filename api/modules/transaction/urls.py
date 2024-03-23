from django.urls import path

from api.modules.fridge.views import FridgeProductsListAPI

urlpatterns = [
    path('payment', FridgeProductsListAPI.as_view(), name='fridge-products-list'),
]
