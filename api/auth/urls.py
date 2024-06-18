from django.urls import path
from api.auth.views import (
    UserCreateAPIView,
    VerifyEmailAPIView,
    VerifyCodeAPIView,
    UserRegisterAPIView,
    TokenObtainPairAPIView,
    TokenRefreshAPIView,
    TokenVerifyAPIView
)

urlpatterns = [
    path('sign-up', UserCreateAPIView.as_view()),
    path('sign-in', TokenObtainPairAPIView, name='token_obtain_pair'),
    path('sign-in/refresh', TokenRefreshAPIView, name='token_refresh'),
    path('sign-in/verify', TokenVerifyAPIView, name='token_verify'),

    path('sign-up/verify-email', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('sign-up/verify-code', VerifyCodeAPIView.as_view(), name='token_code'),
    path('sign-up/v2', UserRegisterAPIView.as_view())
]
