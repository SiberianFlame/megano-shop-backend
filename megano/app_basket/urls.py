from django.urls import path
from app_basket import views

urlpatterns = [
    path('basket', views.BasketAPIView.as_view()),
]