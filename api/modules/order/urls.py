from django.urls import path

from api.modules.order.views import OrderAPIView, OrderDetailView

urlpatterns = [
    path('create/', OrderAPIView.as_view(), name='create-order'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
