from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializer import UserJoinSerializer, UserListSerializer


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
