from django.db.models import Avg
from rest_framework import serializers

from app_basket.models import BasketProduct


class BasketProductSerializer(serializers.ModelSerializer):
    """
    Serializer for basket product model
    """

    id = serializers.SerializerMethodField(method_name='get_id')
    title = serializers.SerializerMethodField(method_name='get_title')
    price = serializers.SerializerMethodField(method_name='get_price')
    description = serializers.SerializerMethodField(method_name='get_description')
    fullDescription = serializers.SerializerMethodField(method_name='get_fullDescription')
    count = serializers.SerializerMethodField(method_name='get_count')
    category = serializers.SerializerMethodField(method_name='get_category')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    images = serializers.SerializerMethodField(method_name='get_images')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    freeDelivery = serializers.SerializerMethodField(method_name='get_freeDelivery')
    date = serializers.SerializerMethodField(method_name='get_date')
    class Meta:
        model = BasketProduct
        fields = ('id', 'title', 'price', 'description',
                  'fullDescription', 'category',
                  'count', 'freeDelivery', 'date', 'images',
                  'tags', 'reviews', 'rating')

    def get_date(self,  obj):
        return obj.product.date

    def get_freeDelivery(self, obj):
        return obj.product.freeDelivery

    def get_count(self, obj):
        return obj.amount

    def get_category(self, obj):
        return obj.product.category.id

    def get_fullDescription(self, obj):
        return obj.product.fullDescription

    def get_description(self, obj):
        return obj.product.description

    def get_price(self, obj):
        return obj.product.price

    def get_title(self, obj):
        return obj.product.title

    def get_id(self, obj):
        return obj.product.id

    def get_tags(self, obj):
        result = [
            {
            'id': obj.id,
            'name': obj.name,
            }
            for obj in obj.product.tags.all()]
        return result

    def get_reviews(self, obj):
        result = obj.product.reviews_all.count()
        return result

    def get_images(self, obj):
        result = []
        for image in obj.product.images.all():
            result.append({
                'src': image.image.url,
                'alt': 'Product image'
            })
        return result

    def get_rating(self, obj):
        return obj.product.reviews_all.all().aggregate(Avg('rating'))['rating__avg']