import random

from django.contrib.auth.models import User
from rest_framework.request import Request

import app_basket
from app_basket.models import Basket, BasketProduct



def get_basket_by_id_or_session(request: Request) -> Basket:
    """
    Get basket by id (if user is authenticated) or by session (if user is anonymous)
    :param request: Request object from user
    :return: basket
    """

    if request.user.is_anonymous:
        if 'unique_anonymous_id' not in request.session:
            request.session['unique_anonymous_id'] = f'{request.META["REMOTE_ADDR"]}{request.META["HTTP_USER_AGENT"]}{random.randrange(100, 1000)}'
            basket = Basket.objects.create(session_id=request.session['unique_anonymous_id'], user=None)
            return basket

        else:
            basket = Basket.objects.get(session_id=request.session['unique_anonymous_id'], user=None)
            return basket

    else:
        return Basket.objects.get(user=request.user, session_id=None)

def changing_basket_from_anonymous(session_data, user: User) -> Basket:
    """
    If user is anonymous, we create or get his basket. If user is authenticated, we get his basket by id.
    If user has logged, we delete his anonymous basket and move all products to new basket.
    :param session_data: Data of the user's session
    :param user: User from request object
    :return: basket
    """

    if 'unique_anonymous_id' in session_data:
        old_basket = Basket.objects.get(session_id=session_data['unique_anonymous_id'], user=None)
        new_basket = Basket.objects.get_or_create(user=user, session_id=None)[0]

        for product in old_basket.products.all():

            try:
                basket_product = BasketProduct.objects.get(basket=new_basket, product=product.product)
                basket_product.amount += product.amount
                basket_product.save()
            except app_basket.models.BasketProduct.DoesNotExist:
                basket_product = BasketProduct.objects.create(basket=new_basket, product=product.product, amount=product.amount)

            product.delete()

        old_basket.delete()
        session_data.delete()
        return new_basket

    else:
        basket = Basket.objects.get_or_create(user=user, session_id=None)[0]
        return basket