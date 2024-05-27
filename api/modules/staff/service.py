from django.shortcuts import get_object_or_404

from rest_framework.exceptions import NotFound

from api.models import CustomUser, Fridge


def get_user(local_admin_id):
    user = get_object_or_404(CustomUser, id=local_admin_id)

    return user


def bind_local_admin_to_fridges(user: CustomUser, fridge_ids: []):
    for fridge_id in fridge_ids:
        try:
            fridge = Fridge.objects.get(account=fridge_id)
            fridge.owner = user

            fridge.save()
        except Fridge.DoesNotExist:
            raise NotFound(f"No fridge with given id: {fridge_id}.")


