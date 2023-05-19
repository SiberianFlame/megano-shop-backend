from django.contrib.auth.models import User
from rest_framework import serializers

from category_app.models import Category
from megano_auth.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(method_name='get_subcategories')
    image = serializers.SerializerMethodField(method_name='get_image')
    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

    def get_subcategories(self, obj):
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
        return {'src': obj.image.url,
                'alt': 'Category image'}

class ProfileSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField(method_name='get_full_name')
    avatar = serializers.SerializerMethodField(method_name='get_avatar')
    class Meta:
        model = Profile
        fields = ('id', 'fullName', 'email', 'phone', 'avatar')

    def get_full_name(self, obj):
        return obj.full_name

    def get_avatar(self, obj):
        return {'src': obj.avatar.url,
                'alt': 'Your avatar'}

class PasswordSerializer(serializers.ModelSerializer):
    passwordCurrent = serializers.SerializerMethodField(method_name='get_password')
    class Meta:
        model = User
        fields = ('passwordCurrent', )

    def get_password(self, obj):
        return obj.password

    # def update(self, instance, validated_data):
    #     instance.set_password(validated_data['passwordReply'])
    #     instance.save()
    #     return instance

class ChangePasswordSerializer(serializers.Serializer):

    passwordCurrent = serializers.CharField(required=True)
    # passwordCurrent =  serializers.SerializerMethodField(method_name='get_password')
    password = serializers.CharField(required=True)
    passwordReply = serializers.CharField(required=True)

    # def get_password(self, obj):
    #     return obj.password

class AvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=True)