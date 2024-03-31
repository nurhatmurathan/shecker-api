#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# from api.models import Order
#
# from api.modules.order import services
#
#
# class TestAPIView(APIView):
#
#     def get(self, request):
#         try:
#             services.test_services()
#             return Response(data={'message': Order.Status.PENDING}, status=status.HTTP_200_OK)
#         except Exception as exception:
#             return Response(data={'message': exception.args[0]}, status=status.HTTP_400_BAD_REQUEST)
