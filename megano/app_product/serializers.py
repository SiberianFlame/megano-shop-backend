from django.db.models import Avg
from rest_framework import serializers

from app_product.models import Sale, Product, Tag


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(method_name='get_tags')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    images = serializers.SerializerMethodField(method_name='get_images')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'description',
                  'fullDescription', 'category',
                  'count', 'freeDelivery', 'date', 'images',
                  'tags', 'specifications', 'reviews', 'rating')

    def get_tags(self, obj):
        result = [
            {
                'id': obj.id,
                'name': obj.name,
            }
            for obj in obj.tags.all()]
        return result


    def get_specifications(self, obj):
        result = []
        for specification in obj.specifications.all():
            result.append({
                'name': specification.name,
                'value': specification.value
            })
        return result

    def get_reviews(self, obj):
        result = []
        for review in obj.reviews_all.all():
            result.append({
                'author': review.author,
                'email': review.email,
                'text': review.text,
                'rate': review.rating,
                'date': review.date
            })
        return result

    def get_images(self, obj):
        result = []
        for image in obj.images.all():
            result.append({
                'src': image.image.url,
                'alt': 'Product image'
            })
        return result

    def get_rating(self, obj):
        return obj.reviews_all.all().aggregate(Avg('rating'))['rating__avg']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

class ReviewSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    text = serializers.CharField(max_length=1000)
    rate = serializers.IntegerField(min_value=1, max_value=5)

class BannerSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    images = serializers.SerializerMethodField(method_name='get_images')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'description',
                  'fullDescription', 'category',
                  'count', 'freeDelivery', 'date', 'images',
                  'tags', 'reviews', 'rating')

    def get_tags(self, obj):
        result = [
            {
            'id': obj.id,
            'name': obj.name,
            }
            for obj in obj.tags.all()]
        return result

    def get_reviews(self, obj):
        result = obj.reviews_all.count()
        return result

    def get_images(self, obj):
        result = []
        for image in obj.images.all():
            result.append({
                'src': image.image.url,
                'alt': 'Product image'
            })
        return result

    def get_rating(self, obj):
        return obj.reviews_all.all().aggregate(Avg('rating'))['rating__avg']

class SaleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    price = serializers.SerializerMethodField(method_name='get_price')
    title = serializers.SerializerMethodField(method_name='get_title')
    id = serializers.SerializerMethodField(method_name='get_id')
    class Meta:
        model = Sale
        fields = ('id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images')

    def get_id(self, obj):
        return obj.product.id

    def get_images(self, obj):
        result = []
        for image in obj.product.images.all():
            result.append({
                'src': image.image.url,
                'alt': 'Product image'
            })
        return result

    def get_price(self, obj):
        if obj.product.old_price:
            return obj.product.old_price
        else:
            return obj.product.price

    def get_title(self, obj):
        return obj.product.title