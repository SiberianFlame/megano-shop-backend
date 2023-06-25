from django.shortcuts import render
from rest_framework.generics import ListAPIView

from app_category.models import Category
from app_category.serializers import CategorySerializer


class CategoryAPIView(ListAPIView):
    """
    Class for getting all categories
    """

    queryset = Category.objects.filter(parent=None).prefetch_related('subcategories')
    serializer_class = CategorySerializer
