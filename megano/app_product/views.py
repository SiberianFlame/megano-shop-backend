import random

from django.db.models import Max, Count, Avg, QuerySet
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app_product.models import Product, Sale, Tag, Review
from app_product.serializers import BannerSerializer, SaleSerializer, ProductSerializer, TagSerializer, ReviewSerializer
from app_product.utils import apply_filters_to_queryset, get_random_products, pagination_for_items


class BannersAPIView(ListAPIView):
    """
    Class view for getting random banners
    """

    serializer_class = BannerSerializer

    def get_queryset(self):
        queryset = get_random_products()
        return queryset

class CatalogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for products in catalog
    """

    serializer_class = BannerSerializer

    def get_queryset(self) -> QuerySet:
        """
        Applying filters to queryset with all products
        :return: Filtered queryset
        """

        queryset = Product.objects.all().prefetch_related('reviews_all')
        filter_params = self.request.query_params

        queryset = apply_filters_to_queryset(queryset, filter_params)

        return queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Getting list of products with pagination
        :param request: Request object from user
        :return: Response with products and pagination
        """

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        start, end, page, last_page = pagination_for_items(self.request.query_params, queryset.count())

        return Response({
            'items': serializer.data[start:end],
            'currentPage': page,
            'lastPage': last_page
        })

class PopularProductsAPIView(ListAPIView):
    """
    Class view for getting popular products
    """

    serializer_class = BannerSerializer

    def get_queryset(self):
        """
        Gets 4 most popular products
        :return: Queryset with popular products
        """

        queryset = Product.objects.order_by('-purchases_num').prefetch_related('images')[:4]
        return queryset

class LimitedProductsAPIView(ListAPIView):
    """
    Class view for getting limited products
    """

    serializer_class = BannerSerializer

    def get_queryset(self):
        """
        Gets 4 products with tag Limited
        :return: Queryset with limited products
        """

        queryset = Product.objects.filter(tags__name="Limited").prefetch_related('tags')[:4]
        return queryset

class SalesViewSet(viewsets.ModelViewSet):
    """
    Viewset for sales list
    """

    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.all().select_related('product')

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Gets list of all sales
        :param request: Request object from user
        :return: Response with sales and pagination
        """

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        start, end, page, last_page = pagination_for_items(self.request.query_params, queryset.count())

        return Response({
            'items': serializer.data[start:end],
            'currentPage': page,
            'lastPage': last_page
        })

class ProductAPIView(RetrieveAPIView):
    """
    Class view for getting detail information about product
    """

    serializer_class = ProductSerializer
    def get_object(self) -> Product:
        return Product.objects.get(id=self.kwargs['id'])

class TagsAPIView(ListAPIView):
    """
    Class view for getting tags
    """

    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.all().prefetch_related('products')
        return queryset

class ProductReviewsAPIView(ListAPIView, CreateAPIView):
    """
    Class view for getting and creating product reviews
    """

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['id']).select_related('product')

    def get(self, *args, **kwargs):
        return self.list(self.request, *args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        """
        Creating review for product
        :return: Response with serialized reviews or with serializer errors
        """

        product = Product.objects.get(id=self.kwargs['id'])
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():
            Review.objects.create(product=product, rating=serializer.validated_data['rate'],  text=serializer.validated_data['text'],
                                  author=serializer.validated_data['author'], email=serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
