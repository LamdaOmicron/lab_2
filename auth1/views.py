import json
from django.conf import settings
from rest_framework import status
from .services import AuthService
from django.shortcuts import render
from .decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect
from .exceptions import AuthenticationError, ConflictError
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from .serializers import (
    RegisterSerializer, LoginSerializer, RefreshSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer, UserProfileSerializer
)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user, access_token, refresh_token = AuthService.register(email, password)
        except ConflictError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        
        response = Response(UserProfileSerializer(user).data, status=status.HTTP_201_CREATED)
        self._set_auth_cookies(response, access_token, refresh_token)
        return response
    
    def _set_auth_cookies(self, response, access_token, refresh_token):
        response.set_cookie(
            'access_token', access_token,
            httponly=True, secure=False,  # в продакшене secure=True
            samesite='Lax',
            max_age=settings.JWT_ACCESS_EXPIRATION * 60
        )
        response.set_cookie(
            'refresh_token', refresh_token,
            httponly=True, secure=False,
            samesite='Lax',
            max_age=settings.JWT_REFRESH_EXPIRATION * 60
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user, access_token, refresh_token = AuthService.login(email, password)
        except AuthenticationError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        self._set_auth_cookies(response, access_token, refresh_token)
        return response
    
    def _set_auth_cookies(self, response, access_token, refresh_token):
        response.set_cookie(
            'access_token', access_token,
            httponly=True, secure=False,
            samesite='Lax',
            max_age=settings.JWT_ACCESS_EXPIRATION * 60
        )
        response.set_cookie(
            'refresh_token', refresh_token,
            httponly=True, secure=False,
            samesite='Lax',
            max_age=settings.JWT_REFRESH_EXPIRATION * 60
        )


class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token missing'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            new_access, new_refresh = AuthService.refresh(refresh_token)
        except AuthenticationError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response({'message': 'Token refreshed'}, status=status.HTTP_200_OK)
        response.set_cookie(
            'access_token', new_access,
            httponly=True, secure=False,
            samesite='Lax',
            max_age=settings.JWT_ACCESS_EXPIRATION * 60
        )
        response.set_cookie(
            'refresh_token', new_refresh,
            httponly=True, secure=False,
            samesite='Lax',
            max_age=settings.JWT_REFRESH_EXPIRATION * 60
        )
        return response


class LogoutView(APIView):
    @login_required
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            AuthService.logout(refresh_token)
        
        response = Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class LogoutAllView(APIView):
    @login_required
    def post(self, request):
        AuthService.logout_all(request.user)
        response = Response({'message': 'All sessions terminated'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class WhoAmIView(APIView):
    @login_required
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        # Здесь должна быть логика отправки email с токеном сброса
        # Для упрощения возвращаем успех всегда
        return Response({'message': 'If the email exists, a reset link has been sent'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        # Реализуйте проверку токена сброса (например, JWT с коротким сроком)
        # и обновление пароля пользователя
        # Здесь заглушка
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)