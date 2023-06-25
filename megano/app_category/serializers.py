from rest_framework import serializers

from app_category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for category model
    """

    subcategories = serializers.SerializerMethodField(method_name='get_subcategories')
    image = serializers.SerializerMethodField(method_name='get_image')
    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

    def get_subcategories(self, obj):
        """
        Getting subcategories for category
        """

        subcategories = [
            {
                'id': subcategory.id,
                'title': subcategory.title,
                'image': {
                    'src': subcategory.image.url,
                    'alt': 'Subcategory image'
                }
            }
            for subcategory in obj.subcategories.all()
        ]
        return subcategories

    def get_image(self, obj):
        """
        Need to match the expected response for frontend
        """

        return {'src': obj.image.url,
                'alt': 'Category image'}





