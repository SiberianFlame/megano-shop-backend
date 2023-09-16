from django.contrib import admin

from app_order.models import Order, DeliveryCost, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Class for displaying order information in admin panel
    """

    list_display = ('id', 'fullName', 'created_at', 'totalCost', 'email', 'phone')

@admin.register(DeliveryCost)
class DeliveryCostAdmin(admin.ModelAdmin):
    """
    Class for displaying and setting delivery cost in admin panel
    """

    list_display = ('regular_cost', 'express_cost', 'min_price')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    """
    Class for displaying product in order information in admin panel
    """

    list_display = ('id', 'order', 'product', 'amount')

