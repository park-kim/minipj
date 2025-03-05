from django.utils import timezone

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from config.settings.base import SIMPLE_JWT
from users.models import User
from users.serializer import UserJoinSerializer, UserListSerializer, \
    UserLoginSerializer

class CustomAccessToken(AccessToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "user_id" in self.payload:
            # UUID를 str로 변환
            self.payload["user_id"] = str(self.payload["user_id"])
SIMPLE_JWT["AUTH_TOKEN_CLASSES"] = ("path.to.CustomAccessToken",)
class UserRegister(APIView):

    def get(self, request):
        users = User.objects.all()
        print(users)
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = UserJoinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email= serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.get(email=email)
            # user = authenticate( request, email=email, password=password)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                user.last_login = timezone.now()
                user.save()
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)

            return Response({"message": "Invalid credentials"},
                                status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        pass
