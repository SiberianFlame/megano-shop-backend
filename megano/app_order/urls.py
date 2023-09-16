from django.urls import path
from app_order import views

urlpatterns = [
    path('orders', views.OrdersAPIView.as_view()),
    path('order/<int:id>', views.OrderAPIView.as_view()),
    path('order-detail/<int:id>', views.OrderDetailAPIView.as_view(), name='order-detail'),
]