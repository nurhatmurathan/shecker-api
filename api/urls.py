from django.urls import path, include

urlpatterns = [
    path('fridge/', include('api.modules.fridge.urls')),
    path('product/', include('api.modules.product.urls')),
    path('order/', include('api.modules.order.urls')),
    path('payment/', include('api.modules.transaction.urls')),
    path('services/', include('api.services.urls'))
]