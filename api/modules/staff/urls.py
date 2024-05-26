from django.urls import path

from api.modules.staff.views import StaffListAPIView
urlpatterns = [
    path('', StaffListAPIView.as_view(), name='list-creat-staff'),
]
