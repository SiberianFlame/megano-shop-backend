from django.contrib.auth.models import User
from django.db import models

from app_product.models import Product


class Order(models.Model):
    """
    Order model with ForeignKey to User model
    """

    created_at = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    deliveryType = models.CharField(max_length=20)
    paymentType = models.CharField(max_length=20)
    totalCost = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    status = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'Order on {self.created_at}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def set_total_cost(self) -> None:
        """
        Setting total cost to order object
        """

        delivery = DeliveryCost.objects.first()
        new_cost = 0
        for product in self.products.all():
            new_cost += product.product.price * product.amount

        if self.deliveryType == 'express':
            new_cost += delivery.express_cost
        elif new_cost < delivery.min_price:
            new_cost += delivery.regular_cost

        if new_cost != self.totalCost:
            self.totalCost = new_cost
            self.save()


class DeliveryCost(models.Model):
    """
    DeliveryCost singleton class. Necessary to set the delivery cost and minimum order amount for free delivery.
    """

    regular_cost = models.DecimalField(max_digits=15, decimal_places=2)
    express_cost = models.DecimalField(max_digits=15, decimal_places=2)
    min_price = models.DecimalField(max_digits=15, decimal_places=2, default=24.00)

    class Meta:
        verbose_name = 'Delivery Cost'
        verbose_name_plural = 'Delivery Costs'

    def __str__(self):
        return 'Delivery cost parameters'

    def save(self, *args, **kwargs):
        """
        Deleting previous object if it exists and saving new one.
        """

        self.__class__.objects.exclude(id=self.id).delete()
        super(DeliveryCost, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Loading object from the database
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class OrderProduct(models.Model):
    """
    Model for storing product in the order
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product} on {self.order}'

    class Meta:
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'
