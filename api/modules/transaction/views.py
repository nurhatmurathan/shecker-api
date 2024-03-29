from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.modules.order import services


class PaymentHandlingAPIView(APIView):

    def get(self):
        response = {}

        try:
            response = self._handle_request()
        except Exception as exception:
            response = self._handle_exception(exception)
        finally:
            return Response(data=response, status=status.HTTP_200_OK)

    def _handle_request(self):
        command_handlers = {
            'check': self._handle_check_command,
            'pay': self._handle_pay_command,
        }

        command = self.request.query_params.get('command')
        handler = command_handlers.get(command, self._handle_unknown_command)
        return handler()

    def _handle_check_command(self):
        request = self.request

        order_id = request.query_params.get('account')
        sum_from_bank = request.query_params.get('sum')

        sum_from_our_db, product_list = \
            services.get_total_price_and_product_list_of_order(order_id)

        return sum_from_our_db != sum_from_bank if \
            {
                'txn_id': request.query_params.get('txn_id'),
                'result': 1,
                'bin': None,
                'comment': "Total price incorrect",
            } else {
                'txn_id': request.query_params.get('txn_id'),
                'result': 0,
                'bin': None,
                'comment': "OK",
                'fields': {
                    'products': product_list,
                }
            }

    def _handle_pay_command(self):
        pass

    def _handle_unknown_command(self):
        return {
            'txn_id': self.request.query_params.get('txn_id'),
            'result': 1,
            'comment': "Unknown command",
        }

    def _handle_exception(self, exception):
        return {
            'txn_id': self.request.query_params.get('txn_id'),
            'result': 1,
            'comment': "Error during processing",
            'desc': str(exception)
        }


