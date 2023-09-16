from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import django_rq

from app_order.models import Order
from . import tasks
from .utils import is_card_number_valid

from rq import Queue
from redis import Redis

redis_conn = Redis()
queue = Queue(connection=redis_conn)

class PaymentAPIView(LoginRequiredMixin,APIView):
    """
    View class for payment processing
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Imitation of payment
        :param request: Request object from user
        :return: Response with serialized payment info or with error status code
        """

        order = Order.objects.get(pk=kwargs['id'])

        if not is_card_number_valid(request.data['number']):
            order.status = 'Unpaid'
            return Response(status=400)

        if order.status == 'Paid':
            return Response(status=400)

        django_rq.enqueue(tasks.func_for_payment, kwargs['id'])

        data_dict = {
            "number": request.data['number'],
            "name": request.data['name'],
            "month": request.data['month'],
            "year": request.data['year'],
            "code": request.data['code'],
        }

        return Response(data=data_dict, status=status.HTTP_200_OK)
