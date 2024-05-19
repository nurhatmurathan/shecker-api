from django.urls import path

from api.modules.transaction.views import *

urlpatterns = [
    path('paymentg', PaymentHandlingAPIView.as_view(), name='payment-handling'),
]
