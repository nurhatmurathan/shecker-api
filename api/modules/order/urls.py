from django.urls import path

from api.modules.order.views import OrderAPIView

urlpatterns = [
    path('create', OrderAPIView.as_view(), name='create-order')
]
