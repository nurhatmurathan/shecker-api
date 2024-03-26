from django.urls import path

from api.modules.transaction.views import *

urlpatterns = [
    path('payment', PaymentHandlingAPIView.as_view(), name='transaction-pay'),
]
