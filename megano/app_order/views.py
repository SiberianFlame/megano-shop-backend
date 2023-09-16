from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app_basket.utils import get_basket_by_id_or_session
from app_order.models import Order, OrderProduct
from app_order.serializers import FullOrderSerializer
from app_order.utils import adding_information_to_order


class OrdersAPIView(LoginRequiredMixin,APIView):
    """
    Class for creating and getting orders
    """

    def get(self, request: Request) -> Response:
        """
        Getting all user's orders
        :param request: Request object from user
        :return: Response object with all user's serialized orders
        """

        return Response(FullOrderSerializer(Order.objects.filter(
            user=request.user).prefetch_related('products').order_by('-created_at'), many=True).data)
    def post(self, request: Request) -> Response:
        """
        Creating new order without any information
        :param request: Request object from user
        :return: Response object with new order's id
        """

        basket = get_basket_by_id_or_session(request)
        order = Order.objects.create(user=request.user)

        for product in basket.products.all():
            OrderProduct.objects.create(order=order, product=product.product, amount=product.amount)
            product.delete()


        return Response({'orderId': order.id})

class OrderAPIView(LoginRequiredMixin,APIView):
    """
    Class for creating and getting order
    """

    def get(self, request: Request, id: int) -> Response:
        """
        Getting single order object by id
        :param request: Request object from user
        :param id: Primary key of order object
        :return: Response with serialized order
        """

        order = Order.objects.get(id=id)
        order.set_total_cost()

        if request.user.is_authenticated:
            serializer = FullOrderSerializer(order, context={
                'profile': request.user.profile
            })
        else:
            serializer = FullOrderSerializer(order)

        return Response(serializer.data)

    def post(self, request: Request, id: int) -> Response:
        """
        Adding information to order
        :param request: Request object from user
        :param id: Primary key of order object
        :return: Response with order id and status
        """

        order = Order.objects.get(id=id)
        adding_information_to_order(order, request.data)

        return Response(
            data={
                "orderId": order.pk,
            },
            status=status.HTTP_200_OK
        )

class OrderDetailAPIView(LoginRequiredMixin,APIView):
    """
    Class for getting detail information about order
    """

    def get(self, request: Request, id: int) -> Response:
        """
        Getting detail information about order by id
        :param request: Request object from user
        :param id: Primary key of order object
        :return: Response with serialized order
        """

        order = Order.objects.get(id=id)
        serializer = FullOrderSerializer(order)
        return Response(serializer.data)
