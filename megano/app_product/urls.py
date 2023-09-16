from django.urls import path
from app_product import views

urlpatterns = [
    path('banners', views.BannersAPIView.as_view()),
    path('catalog', views.CatalogViewSet.as_view({'get': 'list'})),
    path('products/popular', views.PopularProductsAPIView.as_view()),
    path('products/limited', views.LimitedProductsAPIView.as_view()),
    path('sales', views.SalesViewSet.as_view({'get': 'list'})),
    path('product/<int:id>', views.ProductAPIView.as_view()),
    path('product/<int:id>/reviews', views.ProductReviewsAPIView.as_view()),
    path('tags', views.TagsAPIView.as_view()),
]