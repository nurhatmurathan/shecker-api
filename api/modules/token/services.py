import random
from datetime import timedelta

from rest_framework.exceptions import NotFound
from django.utils import timezone

from api.models import Token
from api.modules.token import validations


def get_instance_by_code(code: str):
    instance = Token.objects.get(code=code)
    return instance


def clear_token_related_with_email(email: str):
    instances = Token.objects.filter(email=email)
    if instances.exists():
        instances.delete()


def create_code(email: str):
    clear_token_related_with_email(email)

    code = generate_code()
    expiration_date = timezone.now() + timedelta(minutes=30)
    print(timezone.now())
    print(expiration_date)

    instance = Token.objects.create(email=email, code=code, expiration_date=expiration_date)

    return instance.code


def generate_code() -> str:
    code = f"{random.randint(0, 999999):06d}"

    while Token.objects.filter(code=code).exists():
        code = f"{random.randint(0, 999999):06d}"

    return code


def generate_token() -> str:
    token = f"{random.getrandbits(128):032x}"
    while Token.objects.filter(token=token).exists():
        token = f"{random.getrandbits(128):032x}"
    return token


def create_token(code: str) -> str:
    instance = get_instance_by_code(code)

    token = generate_token()
    instance.token = token

    instance.save()
    return instance.token


def get_email_and_validate_token(token: str):
    validations.are_token_is_exists(token)

    try:
        instance = Token.objects.get(token=token)
    except Token.DoesNotExist:
        raise NotFound({"not-found": "token is not found or invalid"})

    validations.are_instance_is_expired(instance, "Token")
    return instance.email


def validate_code(code: str):
    validations.are_code_is_exists(code)

    try:
        instance = Token.objects.get(code=code)
    except Token.DoesNotExist:
        raise NotFound({"not-found": "code is not found or invalid"})

    validations.are_instance_is_expired(instance, "Code")
    return code
