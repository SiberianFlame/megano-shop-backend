from django.db import models

from category_app.models import Category
from megano_auth.models import Profile


def product_image_directory_path(instance, filename):
    return 'products/{0}/{1}'.format(instance.product.title, filename)

class Product(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.IntegerField()
    description = models.CharField(max_length=200)
    fullDescription = models.TextField()
    freeDelivery = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    purchases_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_directory_path)

    def __str__(self):
        return f'{self.product.title} image'

    class Meta:
        verbose_name = 'product image'
        verbose_name_plural = 'product images'

class Tag(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='tags')

    def __str__(self):
        return f'{self.name} tag'

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

class Specification(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')

    def __str__(self):
        return f'{self.name} specification for {self.product.title}'

    class Meta:
        verbose_name = 'specification'
        verbose_name_plural = 'specifications'

class Review(models.Model):
    author = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    rating = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews_all')

    def __str__(self):
        return f'{self.date} review for {self.product.title}'

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    salePrice = models.DecimalField(max_digits=8, decimal_places=2)
    dateFrom = models.DateField()
    dateTo = models.DateField()

    def __str__(self):
        return f'Sale for {self.product.title}'

    class Meta:
        verbose_name = 'sale'
        verbose_name_plural = 'sales'
