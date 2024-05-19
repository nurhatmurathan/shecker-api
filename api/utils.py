import os
from datetime import datetime

from rest_framework.exceptions import NotFound


def image_upload_path(filename):
    current_datetime = datetime.now()
    date_time_string = current_datetime.strftime('%Y/%m/%d/%H_%M_%S')

    return f"media/photos/{date_time_string}/{filename}"


def get_data(data, key, fields):
    if key not in data:
        raise NotFound(f"Request is must contains {key} information.")

    data_list = data.get(key, [])
    all_required_fields_present = all(
        all(field in item for field in fields)
        for item in data_list
    )

    if not all_required_fields_present:
        raise NotFound(f"Not all fields contains in form. Form must contains {fields} "
                       "fields.")
    return data_list
