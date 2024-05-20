from django.urls import path

from api.modules.staff.views import StaffListCreateAPIView

urlpatterns = [
    path('', StaffListCreateAPIView.as_view(), name='list-creat-staff'),
]
