from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from django.core import validators

from api.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    company = serializers.CharField(validators=[
        validators.MinLengthValidator(limit_value=3, message="Company name should be at least 3 characters long."),
    ])
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'company', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            company=validated_data['company'],
            email=validated_data['email'],
            username=validated_data['email'],
            is_local_admin=True
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
