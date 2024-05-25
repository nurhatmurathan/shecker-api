from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import CustomUser


class StaffSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'company', 'is_active', 'is_staff', 'is_superuser',
                  'is_local_admin', 'date_joined']

    def get_first_name(self, obj):
        if obj.first_name is None:
            return "No last_name"

        return obj.first_name

    def get_last_name(self, obj):
        if obj.last_name is None:
            return "No last_name"

        return obj.last_name

    def get_company(self, obj):
        if obj.is_local_admin is False:
            return "No local admin user"

        if obj.company is None:
            return "No company name"

        return obj.company
