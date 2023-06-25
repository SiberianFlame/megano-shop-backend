import json

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app_auth.models import Profile
from app_auth.serializers import AvatarSerializer, ChangePasswordSerializer, ProfileSerializer
from app_basket.utils import changing_basket_from_anonymous


class AvatarAPIView(LoginRequiredMixin,APIView):
    """
    Class for changing profile avatar
    """

    serializer_class = AvatarSerializer

    def get_object(self):
        return self.request.user.profile

    def post(self, request: Request) -> Response:
        """
        Changing avatar
        :param request: Request object from user
        :return: Response with avatar or with errors if something went wrong
        """

        serializer = self.serializer_class(data=request.data)
        profile = self.get_object()

        if serializer.is_valid():
            avatar = serializer.validated_data['avatar']
            profile.avatar = avatar
            profile.save()
            return Response({'avatar': {'src': profile.avatar.url, 'alt': 'Your avatar'}}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(LoginRequiredMixin,UpdateAPIView):
    """
    Class for changing user password
    """

    serializer_class = ChangePasswordSerializer

    def get_object(self) -> User:
        return self.request.user

    def post(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Checking if the entered passwords match and setting a new password
        :param request: Request object from user
        :return: Success response or response with error if something went wrong
        """

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

class ProfileAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    """
    Class for getting and updating user profile
    """

    serializer_class = ProfileSerializer

    def get_object(self) -> Profile:
        return self.request.user.profile

    def get(self, *args, **kwargs):
        return self.retrieve(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.get_object().full_name = self.request.data['fullName']
        return self.update(self.request, *args, **kwargs)

def signOut(request: Request) -> HttpResponse:
    logout(request)
    return HttpResponse(status=200)

class SignUpView(APIView):
    """
    Class for creating new user, new profile and basket
    """

    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        Creating user, profile, basket, and login new user
        :param request: Request object from user
        :return: HttpResponse with status 200 if everything is ok, 500 if something went wrong
        """

        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        first_name = body['name']

        user = User.objects.create_user(username=username, password=password, first_name=first_name)
        profile = Profile.objects.create(user=user)

        user = authenticate(username=username, password=password)
        basket = changing_basket_from_anonymous(request.session, user)

        if user:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)

class SignInView(APIView):
    def post(self, request: Request) -> HttpResponse:
        body = json.loads(request.body)
        username = body['username']
        password = body['password']

        user = authenticate(request, username=username, password=password)
        basket = changing_basket_from_anonymous(request.session, user)

        if user:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)
