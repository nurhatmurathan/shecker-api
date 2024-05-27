from django.db import transaction
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin

from api.modules.staff.serializers import StaffSerializer
from api.models import CustomUser
from api.permissions import IsSuperAdmin
from api.utils import get_data_without_fields
from api.modules.staff import service


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


class StaffDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = StaffSerializer
    queryset = CustomUser.objects.all()


class BindFridgeToLocalAdminAPIView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        request = self.request

        try:
            with transaction.atomic():
                local_admin_id = get_data_without_fields(request.data, 'local_admin_id')
                fridge_ids = get_data_without_fields(request.data, 'fridges')

                user = service.get_user(local_admin_id)
                service.bind_local_admin_to_fridges(user, fridge_ids)

                return Response(data={'message': 'Fridges successfully bound to the user.'}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'message': str(exception)}, status=status.HTTP_400_BAD_REQUEST)
