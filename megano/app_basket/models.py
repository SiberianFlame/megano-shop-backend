from django.contrib.auth.models import User
from django.db import models

from app_product.models import Product


class Basket(models.Model):
    """
    Basket model. If user is anonymous, then session_id is used to identify basket.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket', null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)

class BasketProduct(models.Model):
    """
    Basket product model. It is connected with basket and product.
    """

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_products')
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product.title} in basket'

    class Meta:
        verbose_name = 'Basket product'
        verbose_name_plural = 'Basket products'
