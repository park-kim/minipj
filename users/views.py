from functools import partial

from django.contrib.auth import authenticate
from django.core import signing
from django.core.signing import SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsOwner
from users.serializer import (
    UserJoinSerializer,
    UserListSerializer,
    UserLoginSerializer,
)
from utils.email import send_email


class VerifyEmail(APIView):
    permission_classes = []

    def get(self, request):
        code = request.GET.get("code", "")
        signer = TimestampSigner()
        try:
            decoded_user_email = signing.loads(code)
            email = signer.unsign(decoded_user_email, max_age=60)
        except (TypeError, SignatureExpired) as e:
            return Response({"error": str(e)}, 400)

        user = get_object_or_404(User, email=email, is_active=False)
        user.is_active = True
        user.save()

        return Response({"msg": "Success verified"}, 200)


class UserRegister(APIView):
    def post(self, request):
        serializer = UserJoinSerializer(data=request.data)
        if serializer.is_valid():
            signer = TimestampSigner()
            signed_user_email = signer.sign(serializer.validated_data["email"])
            signer_dump = signing.dumps(signed_user_email)
            url = f"{request.scheme}://{request.get_host()}/verify/?code={signer_dump}"

            subject = "[parkim]이메일 인증을 완료해 주세요"
            message = f'다음 링크를 클릭해 주세요. <a href="{url}">url</a>'
            send_email(subject, message, serializer.validated_data["email"])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            # user = User.objects.get(email=email)
            print(password)
            user = authenticate(request, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                user.last_login = timezone.now()
                user.save()
                return Response(
                    {
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"msg": "Invalid Token"}, status=400)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Successfully Logout"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserManage(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        user = get_object_or_404(User, email=request.user.email)
        serializer = UserListSerializer(user)
        return Response(serializer.data, status=200)

    def put(self, request):
        user = get_object_or_404(User, email=request.user.email)
        serializer = UserListSerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)

    def patch(self, request):
        user = get_object_or_404(User, email=request.user.email)
        serializer = UserListSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)

    def delete(self, request):
        user = get_object_or_404(User, email=request.user.email)
        user.delete()
        return Response({"msg": "Successfully deleted"}, status=200)
