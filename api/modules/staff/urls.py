from django.urls import path

from api.modules.staff.views import StaffListAPIView, StaffDetailAPIView

urlpatterns = [
    path('', StaffListAPIView.as_view(), name='list-creat-staff'),
    path('<int:pk>/', StaffDetailAPIView.as_view(), name='detail-edit-staff'),
]
