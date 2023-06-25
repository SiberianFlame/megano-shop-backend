from django.urls import path
from app_auth import views

urlpatterns = [
    path('sign-in', views.SignInView.as_view()),
    path('sign-up', views.SignUpView.as_view()),
    path('sign-out', views.signOut),
    path('profile', views.ProfileAPIView.as_view()),
    path('profile/password', views.ChangePasswordAPIView.as_view()),
    path('profile/avatar', views.AvatarAPIView.as_view()),
]