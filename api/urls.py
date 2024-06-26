from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('fridge/', include('api.modules.fridge.urls')),
    path('product/', include('api.modules.product.urls')),
    path('order/', include('api.modules.order.urls')),
    path('transaction/', include('api.modules.transaction.urls')),
    path('fridgeproduct/', include('api.modules.fridgeproduct.urls')),
    path('staff/', include('api.modules.staff.urls')),
    path('services/', include('api.services.urls')),
]
