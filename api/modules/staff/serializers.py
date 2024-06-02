from rest_framework import serializers

from api.models import CustomUser


class StaffSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'company', 'is_active',
                  'is_staff', 'is_local_admin', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']


class BindFridgeToLocalAdminRequestSerializer(serializers.Serializer):
    local_admin_id = serializers.IntegerField()
    fridges = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


