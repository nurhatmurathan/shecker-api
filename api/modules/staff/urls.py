from django.urls import path

from api.modules.staff.views import (
    StaffListAPIView,
    StaffDetailAPIView,
    BindFridgeToLocalAdminAPIView
)

urlpatterns = [
    path('', StaffListAPIView.as_view(), name='list-creat-staff'),
    path('<int:pk>/', StaffDetailAPIView.as_view(), name='detail-edit-staff'),
    path('bind', BindFridgeToLocalAdminAPIView.as_view(), name='bind-fridges-with-user')
]
