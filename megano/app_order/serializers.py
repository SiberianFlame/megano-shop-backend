from rest_framework import serializers

from app_basket.serializers import BasketProductSerializer
from app_order.models import Order


class FullOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for order objects
    """

    createdAt = serializers.SerializerMethodField(method_name='get_createdAt')
    products = serializers.SerializerMethodField(method_name='get_products')
    fullName = serializers.SerializerMethodField(method_name='get_fullName')
    email = serializers.SerializerMethodField(method_name='get_email')
    phone = serializers.SerializerMethodField(method_name='get_phone')
    class Meta:
        model = Order
        fields = ('id', 'status', 'fullName',
                  'email', 'phone', 'deliveryType',
                  'paymentType', 'totalCost', 'city',
                  'address', 'createdAt','products')

    def get_createdAt(self, obj):
        return obj.created_at.strftime('%A %d-%m-%Y, %H:%M:%S')

    def get_products(self, obj):
        """
        Getting and serializing products in order
        :return: Serialized products
        """

        result = BasketProductSerializer(obj.products.all(), many=True).data
        return result

    def get_email(self, obj):
        profile = self.context.get('profile')
        if profile:
            return profile.email
        else:
            return obj.email

    def get_phone(self, obj):
        profile = self.context.get('profile')
        if profile:
            return profile.phone
        else:
            return obj.phone

    def get_fullName(self, obj):
        profile = self.context.get('profile')
        if profile:
            return profile.full_name
        else:
            return obj.fullName