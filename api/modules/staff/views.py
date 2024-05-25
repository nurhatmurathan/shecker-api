from django.contrib.auth.models import User
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.modules.staff.serializers import StaffSerializer
from api.permissions import *


class StaffListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = StaffSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='is_staff', description='Filter by staff users', required=False,
                             type=OpenApiTypes.BOOL,
                             default=True),
            OpenApiParameter(name='is_superuser', description='Filter by superadmin users', required=False,
                             type=OpenApiTypes.BOOL, default=True),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        is_staff = self.request.query_params.get('is_staff', None)
        is_superuser = self.request.query_params.get('is_superuser', None)

        if not is_staff and not is_superuser:
            return User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))

        query = Q(is_staff=(is_staff == 'true')) | Q(is_superuser=(is_superuser == 'true'))

        return User.objects.filter(query)
