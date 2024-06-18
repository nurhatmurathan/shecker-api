from datetime import datetime

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from api.models import Token


def are_token_is_exists(token: str):
    if not token:
        ValidationError({'validation-error': 'Token is required'})


def are_code_is_exists(code: str):
    if not code:
        ValidationError({'validation-error': 'Code is required'})


def are_instance_is_expired(instance: Token, field: str):
    print(instance.expiration_date)
    print(timezone.now())

    if instance.expiration_date < timezone.now():
        raise ValidationError({'validation-error': f'{field} is expired'})
