# auth/services.py
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from users.models import User, RefreshToken
from .utils.jwt_utils import generate_access_token, generate_refresh_token, decode_refresh_token
from .utils.crypto_utils import hash_token
from .exceptions import AuthenticationError, ConflictError

logger = logging.getLogger(__name__)

class AuthService:
    
    @staticmethod
    def register(email: str, password: str):
        """Регистрация нового пользователя."""
        # Проверка уникальности email (дублируем для безопасности)
        if User.objects.filter(email=email, deleted_at__isnull=True).exists():
            raise ConflictError("Пользователь с таким email уже существует")
        
        user = User(email=email)
        user.set_password(password)
        user.save()
        
        # Генерация токенов
        access_token = generate_access_token(str(user.id))
        refresh_token = generate_refresh_token(str(user.id))
        
        # Сохранение refresh токена в БД (хешированного)
        token_hash = hash_token(refresh_token)
        RefreshToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=timezone.now() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION)
        )
        return user, access_token, refresh_token
    
    @staticmethod
    def login(email: str, password: str):
        """Аутентификация пользователя."""
        try:
            user = User.objects.get(email=email, deleted_at__isnull=True)
        except User.DoesNotExist:
            raise AuthenticationError("Неверный email или пароль")
        
        if not user.check_password(password):
            raise AuthenticationError("Неверный email или пароль")
        
        # Отзываем все предыдущие refresh токены пользователя (опционально: оставляем только текущий)
        RefreshToken.objects.filter(user=user, revoked=False).update(revoked=True)
        
        # Генерация новой пары токенов
        access_token = generate_access_token(str(user.id))
        refresh_token = generate_refresh_token(str(user.id))
        
        # Сохраняем новый refresh токен
        token_hash = hash_token(refresh_token)
        RefreshToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=timezone.now() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION)
        )
        return user, access_token, refresh_token
    
    @staticmethod
    def refresh(refresh_token_str: str):
        """Обновление пары токенов по refresh токену."""
        payload = decode_refresh_token(refresh_token_str)
        if not payload:
            raise AuthenticationError("Недействительный refresh токен")
        
        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationError("Недействительный refresh токен")
        
        # Проверяем наличие токена в БД (не отозван, не истёк)
        token_hash = hash_token(refresh_token_str)
        try:
            stored_token = RefreshToken.objects.get(
                token_hash=token_hash,
                user_id=user_id,
                revoked=False,
                expires_at__gt=timezone.now()
            )
        except RefreshToken.DoesNotExist:
            raise AuthenticationError("Refresh токен отозван или истёк")
        
        # Отзываем старый токен
        stored_token.revoke()
        
        # Генерируем новую пару
        new_access = generate_access_token(user_id)
        new_refresh = generate_refresh_token(user_id)
        
        # Сохраняем новый refresh
        new_hash = hash_token(new_refresh)
        RefreshToken.objects.create(
            user_id=user_id,
            token_hash=new_hash,
            expires_at=timezone.now() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION)
        )
        return new_access, new_refresh
    
    @staticmethod
    def logout(refresh_token_str: str):
        """Завершение текущей сессии (отзыв конкретного refresh токена)."""
        if not refresh_token_str:
            raise AuthenticationError("Refresh токен не предоставлен")
        
        token_hash = hash_token(refresh_token_str)
        try:
            stored_token = RefreshToken.objects.get(token_hash=token_hash, revoked=False)
            stored_token.revoke()
        except RefreshToken.DoesNotExist:
            # Если токена нет или он уже отозван – просто игнорируем
            pass
    
    @staticmethod
    def logout_all(user: User):
        """Завершение всех сессий пользователя."""
        RefreshToken.objects.filter(user=user, revoked=False).update(revoked=True)
    
    @staticmethod
    def get_user_by_id(user_id: str):
        """Получение пользователя по ID (для whoami)."""
        try:
            return User.objects.get(id=user_id, deleted_at__isnull=True)
        except User.DoesNotExist:
            return None