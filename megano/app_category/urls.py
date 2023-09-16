from django.urls import path

from app_category import views

urlpatterns = [
    path('categories', views.CategoryAPIView.as_view()),
]