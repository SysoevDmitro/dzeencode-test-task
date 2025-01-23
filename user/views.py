from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("/user/login/")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register_page(request):
    return render(request, "register.html")


class CustomTokenObtainPairView(TokenObtainPairView):

    def get(self, request):
        return redirect("/api/comments/")

    def post(self, request, *args, **kwargs):
        # Получаем стандартный ответ от TokenObtainPairView
        token_response = super().post(request, *args, **kwargs)

        # Создаём новый response для установки куки
        response = redirect("/api/comments/")

        # Удаляем существующие токены, если они есть
        if 'access_token' in request.COOKIES:
            response.delete_cookie('access_token')
        if 'refresh_token' in request.COOKIES:
            response.delete_cookie('refresh_token')

        # Получаем access и refresh токены из ответа
        access_token = token_response.data.get('access')
        refresh_token = token_response.data.get('refresh')

        if access_token and refresh_token:
            # Устанавливаем токены в куки
            response.set_cookie(
                'access_token', access_token, httponly=True, samesite='Strict'
            )
            response.set_cookie(
                'refresh_token', refresh_token, httponly=True, samesite='Strict'
            )

        return response


class LoginView(APIView):
    def get(self, request):
        return render(request, "login.html")


class LogoutView(APIView):
    """
    Эндпоинт для выхода из системы.
    Удаляет access и refresh токены из куков.
    """

    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logout successful"})

        # Удаление токенов из куков
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
