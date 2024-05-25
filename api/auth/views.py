from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView

from api.auth.serializer import UserCreateSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer