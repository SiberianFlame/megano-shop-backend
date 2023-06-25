from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

import app_basket
from app_basket.models import Basket, BasketProduct
from app_basket.serializers import BasketProductSerializer
from app_basket.utils import get_basket_by_id_or_session
from app_product.models import Product


class BasketAPIView(APIView):
    """
    View class for getting, changing and deleting basket and basket products
    """

    def get(self, request: Request) -> Response:
        """
        Getting basket and serializing it
        :param request: Request object from user
        :return: Response with serialized basket
        """

        basket = get_basket_by_id_or_session(request)
        serializer = BasketProductSerializer(basket.products.all(), many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Adding basket product to basket
        :param request: Request object from user
        :return: Response with serialized data or error status code
        """

        basket = get_basket_by_id_or_session(request)
        product = Product.objects.get(id=request.data.get('id'))
        count = request.data.get('count', 1)

        if count <= product.count:
            try:
                basket_product = BasketProduct.objects.get(basket=basket, product=product)
                basket_product.amount += count
                basket_product.save()
            except app_basket.models.BasketProduct.DoesNotExist:
                basket_product = BasketProduct.objects.create(basket=basket, product=product, amount=count)
                basket_product.save()

            serializer = BasketProductSerializer(basket.products.all(), many=True)
            return Response(serializer.data)
        else:
            return Response(status=400)

    def delete(self, request: Request) -> Response:
        """
        Deleting basket product from basket
        :param request: Request object from user
        :return: Response with serialized basket products
        """

        basket = get_basket_by_id_or_session(request)
        product = Product.objects.get(id=request.data.get('id'))
        basket_product = BasketProduct.objects.get(basket=basket, product=product)
        count = request.data.get('count', 1)

        if count < basket_product.amount:
            basket_product.amount -= count
            basket_product.save()
        elif count == basket_product.amount:
            basket_product.delete()
        else:
            return Response(status=400)

        serializer = BasketProductSerializer(basket.products.all(), many=True)
        return Response(serializer.data)
