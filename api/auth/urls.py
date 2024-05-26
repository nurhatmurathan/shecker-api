from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from api.auth.views import UserCreateAPIView

urlpatterns = [
    path('sign-up', UserCreateAPIView.as_view()),
    path('sign-in', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sign-in/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign-in/verify', TokenVerifyView.as_view(), name='token_verify')
]
