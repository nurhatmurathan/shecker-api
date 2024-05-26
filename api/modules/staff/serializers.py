from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import CustomUser


class StaffSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'company', 'is_active', 'is_staff', 'is_superuser',
                  'is_local_admin', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'date_joined']

    def get_company(self, obj):
        if obj.is_local_admin is False:
            return "No local admin user"

        if obj.company is None:
            return "No company name"

        return obj.company
