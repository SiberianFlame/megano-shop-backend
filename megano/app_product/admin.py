from django.contrib import admin

from app_product.models import Product, Tag, Specification, ProductImage, Sale


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Class for displaying, creating and changing tag in admin panel
    """

    list_display = ['id', 'name', 'category']

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """
    Class for displaying, creating and changing specification in admin panel
    """

    list_display = ['id', 'product', 'name']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Class for displaying, creating and changing product image in admin panel
    """

    list_display = ['id', 'product']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Class for displaying, creating and changing sale in admin panel
    """

    list_display = ['id', 'product', 'dateFrom', 'dateTo']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Class for displaying, creating and changing product in admin panel
    """

    list_display = ['id', 'title', 'price', 'count', 'freeDelivery']

