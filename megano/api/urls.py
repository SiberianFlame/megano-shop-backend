from django.urls import path
from api import views

urlpatterns = [
    path('banners', views.BannersAPIView.as_view()),
    path('categories', views.CategoryAPIView.as_view()),
    path('catalog', views.CatalogViewSet.as_view({'get': 'list'})),
    # path('catalog/<int:id>', views.ProductAPIView.as_view()),
    path('products/popular', views.PopularProductsAPIView.as_view()),
    path('products/limited', views.LimitedProductsAPIView.as_view()),
    path('sales', views.SalesViewSet.as_view({'get': 'list'})),
    path('basket', views.basket), #  todo add basket controller
    path('orders', views.orders), # todo add orders controller
    path('sign-in', views.signIn),
    path('sign-up', views.signUp),
    path('sign-out', views.signOut),
    path('product/<int:id>', views.ProductAPIView.as_view()),
    path('product/<int:id>/reviews', views.ProductReviewsAPIView.as_view()),
    path('tags', views.TagsAPIView.as_view()),
    path('profile', views.ProfileAPIView.as_view()),
    path('profile/password', views.ChangePasswordAPIView.as_view()),
    path('profile/avatar', views.AvatarAPIView.as_view()),
    path('order/<int:id>', views.order), # todo add order controller
    path('payment/<int:id>', views.payment), # todo add payment controller
]
