from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from django.db import transaction
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.auth.serializer import UserCreateSerializer, VerifyEmailSerializer
from api.models import CustomUser
from api.modules.token import services as token_services
from email_sender import services as email_sender_service


TokenObtainPairAPIView = extend_schema_view(
    post=extend_schema(tags=['Auth'])
)(TokenObtainPairView.as_view())

TokenRefreshAPIView = extend_schema_view(
    post=extend_schema(tags=['Auth'])
)(TokenRefreshView.as_view())

TokenVerifyAPIView = extend_schema_view(
    post=extend_schema(tags=['Auth'])
)(TokenVerifyView.as_view())


@extend_schema(
    tags=["Auth"],
    summary="Create a new user. Version 1",
    description="This endpoint allows you to create a new user. You need to provide the necessary user details.",
    request=UserCreateSerializer,
    responses={201: UserCreateSerializer, 400: "Bad Request"},
)
class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer


@extend_schema(
    tags=["Auth"],
    request=UserCreateSerializer,
    summary="Create a new user. Version 2",
    responses={201: UserCreateSerializer},
    description="Register a new user with a valid token",
    parameters=[
        OpenApiParameter(name='token', description='Verification token', required=True, type=str)
    ]
)
class UserRegisterAPIView(APIView):

    def post(self, request):
        try:
            with transaction.atomic():
                request = self.request
                token = request.query_params.get('token', None)
                email = token_services.get_email_and_validate_token(token)

                data = request.data
                data['email'] = email

                serializer = UserCreateSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                token_services.clear_token_related_with_email(email)
                return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response({'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Auth"],
    request=VerifyEmailSerializer,
    responses={200: OpenApiResponse(description='Email verified successfully')},
    description="Verify an email address and send a verification code.",
)
class VerifyEmailAPIView(APIView):

    def post(self, request):
        try:
            with transaction.atomic():
                request = self.request

                data = request.data
                serializer = VerifyEmailSerializer(data=data)
                serializer.is_valid(raise_exception=True)

                email = serializer.validated_data['email']
                code = token_services.create_code(email)

                email_sender_service.send_verification_email(email, code)
                return Response(data={'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Auth"],
    responses={200: OpenApiResponse(description='Token created successfully')},
    parameters=[
        OpenApiParameter(name='code', description='Verification code', required=True, type=str)
    ],
    description="Validate a code and create a token."
)
class VerifyCodeAPIView(APIView):

    def get(self, request):
        try:
            with transaction.atomic():
                request = self.request
                code = request.query_params.get('code', None)
                token_services.validate_code(code)

                token = token_services.create_token(code)
                return Response(data={'token': token}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception)}, status=status.HTTP_400_BAD_REQUEST)
