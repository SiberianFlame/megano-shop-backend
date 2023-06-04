import random

from django.db.models import Max, Count, Avg
from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import mixins, status, viewsets
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    CreateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ProductSerializer, TagSerializer, ReviewSerializer, BannerSerializer, SaleSerializer
from category_app.models import Category
from category_app.serializers import CategorySerializer, ProfileSerializer, PasswordSerializer, AvatarSerializer, \
    ChangePasswordSerializer
from megano_auth.models import Profile
from product.models import Product, Tag, Review, Sale

User = get_user_model()
def get_random_products():
    max_id = Product.objects.aggregate(max_id=Max("id"))['max_id']
    first_pk, second_pk = random.sample([num for num in range(1, max_id + 1)], 2)
    random_products = [Product.objects.get(pk=first_pk),
                       Product.objects.get(pk=second_pk)]
    return random_products

class BannersAPIView(ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        queryset = get_random_products()
        return queryset

class CategoryAPIView(ListAPIView):
    queryset = Category.objects.filter(parent=None).prefetch_related('subcategories')
    serializer_class = CategorySerializer

class CatalogViewSet(viewsets.ModelViewSet):
    serializer_class = BannerSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        filter_params = self.request.query_params

        if filter_params:
            if filter_params.get('filter[name]'):
                queryset = queryset.filter(title__icontains=filter_params.get('filter[name]'))

            if filter_params.get('filter[freeDelivery]') == 'true':
                queryset = queryset.filter(freeDelivery=True)

            if filter_params.get('filter[available]') == 'true':
                queryset = queryset.filter(count__gt=0)

            if filter_params.get('filter[minPrice]'):
                queryset = queryset.filter(price__gte=filter_params.get('filter[minPrice]'))

            if filter_params.get('filter[maxPrice]'):
                queryset = queryset.filter(price__lte=filter_params.get('filter[maxPrice]'))

        sort_by = self.request.query_params.get('sort', 'date')
        sort_type = self.request.query_params.get('sortType', 'dec')
        queryset = queryset.annotate(
            reviews=Count('reviews_all'),
            rating=Avg('reviews_all__rating')
            ).order_by(
            f'{"-" if sort_type == "dec" else ""}{sort_by}'
        )

        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)

        tags = self.request.query_params.getlist('tags[]', None)
        if tags:
            queryset = queryset.filter(tags__id__in=tags)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        limit = int(self.request.query_params.get('limit', 20))
        count = queryset.count()
        last_page = (count // limit) + (1 if count % limit > 0 else 0)

        page = int(request.query_params.get('currentPage', 1))
        start = (page - 1) * limit
        end = start + limit

        return Response({
            'items': serializer.data[start:end],
            'currentPage': page,
            'lastPage': last_page
        })

class PopularProductsAPIView(ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        queryset = Product.objects.order_by('-purchases_num')[:4]
        return queryset

class LimitedProductsAPIView(ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(tags__name="Limited").prefetch_related('tags')[:4]
        return queryset

class SalesViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        limit = int(self.request.query_params.get('limit', 5))
        count = queryset.count()
        last_page = (count // limit) + (1 if count % limit > 0 else 0)

        page = int(request.query_params.get('currentPage', 1))
        start = (page - 1) * limit
        end = start + limit

        return Response({
            'items': serializer.data[start:end],
            'currentPage': page,
            'lastPage': last_page
        })

def basket(request):
    if(request.method == "GET"):
        print('[GET] /api/basket/')
        data = [
            {
                "id": 123,
                "category": 55,
                "price": 500.67,
                "count": 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
                 "tags": [
                        {
                            "id": 0,
                            "name": "Hello world"
                        }
                 ],
                "reviews": 5,
                "rating": 4.6
            },
            {
                "id": 124,
                "category": 55,
                "price": 201.675,
                "count": 5,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
                 "tags": [
                        {
                            "id": 0,
                            "name": "Hello world"
                        }
                 ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "POST"):
        body = json.loads(request.body)
        id = body['id']
        count = body['count']
        print('[POST] /api/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))
        data = [
            {
                "id": id,
                "category": 55,
                "price": 500.67,
                "count": 13,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
                 "tags": [
                        {
                            "id": 0,
                            "name": "Hello world"
                        }
                 ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "DELETE"):
        body = json.loads(request.body)
        id = body['id']
        print('[DELETE] /api/basket/')
        data = [
            {
            "id": id,
            "category": 55,
            "price": 500.67,
            "count": 11,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
             ],
             "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
             ],
            "reviews": 5,
            "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

def orders(request):
    if (request.method == "POST"):
        data = [
            {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
             ],
             "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
             ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

def signIn(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)

def signUp(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        first_name = body['name']
        user = User.objects.create_user(username=username, password=password, first_name=first_name)
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        login(request, user)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)
def signOut(request):
    logout(request)
    return HttpResponse(status=200)

class ProductAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    def get_object(self):
        return Product.objects.get(id=self.kwargs['id'])

class TagsAPIView(ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        # queryset = Tag.objects.get(category=self.kwargs['category']).all()
        queryset = Tag.objects.all()
        return queryset

class ProductReviewsAPIView(ListAPIView, CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['id'])

    def get(self, *args, **kwargs):
        return self.list(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['id'])
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():
            Review.objects.create(product=product, rating=serializer.validated_data['rate'],  text=serializer.validated_data['text'],
                                  author=serializer.validated_data['author'], email=serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def get(self, *args, **kwargs):
        return self.retrieve(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)

class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def post(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("passwordCurrent")):
                return Response({"passwordCurrent": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            elif not serializer.data.get('password') == serializer.data.get('passwordReply'):
                return Response({'password': ['Passwords must match.']}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully!',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AvatarAPIView(APIView):
    serializer_class = AvatarSerializer

    def get_object(self):
        return self.request.user.profile

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        profile = self.get_object()
        if serializer.is_valid():
            avatar = serializer.validated_data['avatar']
            profile.avatar = avatar
            profile.save()
            return Response({'avatar': {'src': profile.avatar.url, 'alt': 'Your avatar'}}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def orders(request):
    if(request.method == 'GET'):
        data = [
            {
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orang",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      },
            {
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      }
        ]
        return JsonResponse(data, safe=False)

    elif(request.method == 'POST'):
        data = {
            "orderId": 123,
        }
        return JsonResponse(data)

    return HttpResponse(status=500)

def order(request, id):
    if(request.method == 'GET'):
        data = {
            "id": 123,
            "createdAt": "2023-05-05 12:12",
            "fullName": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "deliveryType": "free",
            "paymentType": "online",
            "totalCost": 567.8,
            "status": "accepted",
            "city": "Moscow",
            "address": "red square 1",
            "products": [
                {
                    "id": 123,
                    "category": 55,
                    "price": 500.67,
                    "count": 12,
                    "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                    "title": "video card",
                    "description": "description of the product",
                    "freeDelivery": True,
                    "images": [
                        {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "Image alt string"
                        }
                    ],
                    "tags": [
                        {
                        "id": 12,
                        "name": "Gaming"
                        }
                    ],
                    "reviews": 5,
                    "rating": 4.6
                },
            ]
        }
        return JsonResponse(data)

    elif(request.method == 'POST'):
        data = { "orderId": 123 }
        return JsonResponse(data)

    return HttpResponse(status=500)

def payment(request, id):
    print('qweqwewqeqwe', id)
    return HttpResponse(status=200)