from django.contrib import admin

from app_basket.models import Basket, BasketProduct


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Class for displaying Basket model in admin panel
    """

    list_display = ('id', 'user')

@admin.register(BasketProduct)
class BasketProductAdmin(admin.ModelAdmin):
    """
    Class for displaying products in basket in admin panel
    """

    list_display = ('id', 'basket', 'product')
