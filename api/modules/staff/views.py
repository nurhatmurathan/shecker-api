from rest_framework import generics

from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from api.modules.staff.serializers import StaffSerializer
from api.models import CustomUser
from api.permissions import IsSuperAdmin


class StaffListAPIView(ListModelMixin, GenericAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = StaffSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='is_staff', description='Filter by staff users', required=False,
                             type=OpenApiTypes.BOOL,
                             default=True),
            OpenApiParameter(name='is_local_admin', description='Filter by local admin users', required=False,
                             type=OpenApiTypes.BOOL, default=True),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        is_staff = self.request.query_params.get('is_staff', None)
        is_local_admin = self.request.query_params.get('is_local_admin', None)

        queryset = CustomUser.objects.filter(Q(is_staff=True) | Q(is_local_admin=True))

        if is_staff is None or is_local_admin is None:
            is_staff = False \
                if is_staff is None \
                else is_staff.lower() in ['true', '1', 't', 'yes', 'y']
            is_local_admin = False \
                if is_local_admin is None \
                else is_local_admin.lower() in ['true', '1', 't', 'yes', 'y']
            queryset = queryset.filter(Q(is_staff=is_staff) | Q(is_local_admin=is_local_admin))

        return queryset
