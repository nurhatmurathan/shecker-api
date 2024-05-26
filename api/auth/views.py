from rest_framework.generics import CreateAPIView

from api.auth.serializer import UserCreateSerializer
from api.models import CustomUser


class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
