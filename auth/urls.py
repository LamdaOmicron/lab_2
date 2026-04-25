# auth/urls.py
from django.urls import path
from .views import (
    RegisterView, LoginView, RefreshView, LogoutView, LogoutAllView,
    WhoAmIView, ForgotPasswordView, ResetPasswordView
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('refresh', RefreshView.as_view(), name='refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('logout-all', LogoutAllView.as_view(), name='logout-all'),
    path('whoami', WhoAmIView.as_view(), name='whoami'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
]