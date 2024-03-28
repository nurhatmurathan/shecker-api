from django.urls import path

from api.services.views import upload_image

urlpatterns = [
    path('upload-image', upload_image, name='upload_image')
]