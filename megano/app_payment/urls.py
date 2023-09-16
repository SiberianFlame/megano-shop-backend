from django.urls import path
from app_payment import views

urlpatterns = [
    path('payment/<int:id>', views.PaymentAPIView.as_view()),
]