from django.urls import path
from api import views

urlpatterns = [
    path('banners', views.banners),
    path('categories', views.CategoryAPIView.as_view()),
    path('catalog', views.catalog),
    path('products/popular', views.productsPopular),
    path('products/limited', views.productsLimited),
    path('sales', views.sales),
    path('basket', views.basket),
    path('orders', views.orders),
    path('sign-in', views.signIn),
    path('sign-up', views.signUp),
    path('sign-out', views.signOut),
    path('product/<int:id>', views.product),
    path('product/<int:id>/reviews', views.productReviews),
    path('tags', views.tags),
    path('profile', views.ProfileAPIView.as_view()),
    path('profile/password', views.ChangePasswordAPIView.as_view()),
    path('profile/avatar', views.AvatarAPIView.as_view()),
    path('order/<int:id>', views.order),
    path('payment/<int:id>', views.payment),
]
