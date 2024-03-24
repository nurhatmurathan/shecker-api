from django.urls import path

from api.modules.transaction.views import PaymentHandlingAPIView

urlpatterns = [
    path('', PaymentHandlingAPIView.as_view(), name='payment-handling'),
]