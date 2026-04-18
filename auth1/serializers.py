# auth/serializers.py
from rest_framework import serializers
from users.models import User
import re

# --- Вспомогательные функции валидации ---
def validate_email_format(email):
    """Базовая проверка формата email (можно расширить)."""
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        raise serializers.ValidationError("Некорректный формат email")
    return email

def validate_password_strength(password):
    """Проверка сложности пароля: минимум 8 символов, цифры, буквы разного регистра."""
    if len(password) < 8:
        raise serializers.ValidationError("Пароль должен содержать минимум 8 символов")
    if not re.search(r'[A-Z]', password):
        raise serializers.ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
    if not re.search(r'[a-z]', password):
        raise serializers.ValidationError("Пароль должен содержать хотя бы одну строчную букву")
    if not re.search(r'\d', password):
        raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру")
    return password

# --- Сериализаторы ---

class RegisterSerializer(serializers.Serializer):
    """DTO для регистрации нового пользователя."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password_strength])

    def validate_email(self, value):
        value = validate_email_format(value)
        # Проверка уникальности email
        if User.objects.filter(email=value, deleted_at__isnull=True).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

class LoginSerializer(serializers.Serializer):
    """DTO для входа."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class RefreshSerializer(serializers.Serializer):
    """DTO для обновления токенов (обычно пустой, так как токен берётся из cookies)."""
    pass  # refresh токен извлекается из cookies, не из тела запроса

class ForgotPasswordSerializer(serializers.Serializer):
    """DTO для запроса сброса пароля."""
    email = serializers.EmailField()

    def validate_email(self, value):
        # Проверяем, существует ли пользователь с таким email (но не раскрываем факт существования)
        if not User.objects.filter(email=value, deleted_at__isnull=True).exists():
            # По соображениям безопасности возвращаем ту же ошибку, что и при успехе
            pass
        return value

class ResetPasswordSerializer(serializers.Serializer):
    """DTO для установки нового пароля по токену сброса."""
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password_strength])

class UserProfileSerializer(serializers.ModelSerializer):
    """DTO для ответа с профилем пользователя (без чувствительных данных)."""
    class Meta:
        model = User
        fields = ['id', 'email', 'created_at']