import os
from datetime import datetime


def image_upload_path(filename):
    current_datetime = datetime.now()
    date_time_string = current_datetime.strftime('%Y/%m/%d/%H_%M_%S')

    return f"media/photos/{date_time_string}/{filename}"
