from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import mixins, status
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from category_app.models import Category
from category_app.serializers import CategorySerializer, ProfileSerializer, PasswordSerializer, AvatarSerializer, \
    ChangePasswordSerializer
from megano_auth.models import Profile

User = get_user_model()

def banners(request):
    data = [
        {
            "id": "123",
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
                    "alt": "any alt text",
                }
            ],
            "tags": [
                "string"
            ],
            "reviews": 5,
            "rating": 4.6
        },
    ]
    return JsonResponse(data, safe=False)

class CategoryAPIView(ListAPIView):
    queryset = Category.objects.filter(parent=None).prefetch_related('subcategories')
    serializer_class = CategorySerializer

def catalog(request):
    data = {
         "items": [
                 {
                     "id": 123,
                     "category": 123,
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
         ],
         "currentPage": randrange(1, 4),
         "lastPage": 3
     }
    return JsonResponse(data)

def productsPopular(request):
    data = [
        {
            "id": "123",
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

def productsLimited(request):
    data = [
        {
            "id": "123",
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

def sales(request):
    data = {
        'items': [
            {
                "id": 123,
                "price": 500.67,
                "salePrice": 200.67,
                "dateFrom": "2023-05-08",
                "dateTo": "2023-05-20",
                "title": "video card",
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
            }
        ],
        'currentPage': randrange(1, 4),
        'lastPage': 3,
    }
    return JsonResponse(data)

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

def product(request, id):
    data = {
        "id": 123,
        "category": 55,
        "price": 500.67,
        "count": 12,
        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
        "title": "video card",
        "description": "description of the product",
        "fullDescription": "full description of the product",
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
        "reviews": [
            {
                "author": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "text": "rewrewrwerewrwerwerewrwerwer",
                "rate": 4,
                "date": "2023-05-05 12:12"
            }
        ],
        "specifications": [
            {
                "name": "Size",
                "value": "XL"
            }
        ],
        "rating": 4.6
    }
    return JsonResponse(data)

def tags(request):
    data = [
        { "id": 0, "name": 'tag0' },
        { "id": 1, "name": 'tag1' },
        { "id": 2, "name": 'tag2' },
    ]
    return JsonResponse(data, safe=False)

def productReviews(request, id):
    data = [
    {
      "author": "Annoying Orange",
      "email": "no-reply@mail.ru",
      "text": "rewrewrwerewrwerwerewrwerwer",
      "rate": 4,
      "date": "2023-05-05 12:12"
    },
    {
      "author": "2Annoying Orange",
      "email": "no-reply@mail.ru",
      "text": "rewrewrwerewrwerwerewrwerwer",
      "rate": 5,
      "date": "2023-05-05 12:12"
    },
    ]
    return JsonResponse(data, safe=False)

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