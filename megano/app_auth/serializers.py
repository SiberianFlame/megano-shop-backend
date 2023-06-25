from django.contrib.auth.models import User
from rest_framework import serializers

from app_auth.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model with full name, email, phone and avatar fields
    """

    fullName = serializers.SerializerMethodField(method_name='get_full_name')
    avatar = serializers.SerializerMethodField(method_name='get_avatar')
    class Meta:
        model = Profile
        fields = ('id', 'fullName', 'email', 'phone', 'avatar')

    def get_full_name(self, obj):
        return obj.full_name

    def get_avatar(self, obj):
        """
        Need to match the expected response for frontend
        """

        return {'src': obj.avatar.url,
                'alt': 'Your avatar'}


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for getting password from frontend and changing it
    """

    passwordCurrent = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    passwordReply = serializers.CharField(required=True)

class AvatarSerializer(serializers.Serializer):
    """
    Serializer for getting avatar from frontend and changing it
    """

    avatar = serializers.ImageField(required=True)