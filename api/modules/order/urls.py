from rest_framework.routers import SimpleRouter

from django.urls import path, include

from api.modules.order.views import OrderAPIView, OrderDetailView, OrderAdminReadonlyModelViewSet

order_readonly_admin_router = SimpleRouter()
order_readonly_admin_router.register(r'', OrderAdminReadonlyModelViewSet)

urlpatterns = [
    path('admin/', include(order_readonly_admin_router.urls)),
    path('create/', OrderAPIView.as_view(), name='create-order'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
