from django.contrib import admin

from product.models import Product, Tag, Specification, ProductImage, Sale

# admin.site.register(Product)
# admin.site.register(Tag)
# admin.site.register(Specification)
# admin.site.register(ProductImage)
# admin.site.register(Sale)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'dateFrom', 'dateTo']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'count', 'freeDelivery']

