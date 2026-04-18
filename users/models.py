# users/models.py
import uuid
import bcrypt
from django.db import models
from django.utils import timezone

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=200, unique=True, db_index=True)
    password = models.CharField(max_length=128, blank=True, null=True)  # хеш bcrypt, может быть пустым для OAuth-пользователей
    
    # OAuth идентификаторы
    yandex_id = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    vk_id = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Флаг активности (можно вычислить по deleted_at)
    @property
    def is_active(self):
        return self.deleted_at is None
    
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        self.deleted_at = None
        self.save()
    
    # --- Работа с паролем ---
    def set_password(self, raw_password: str):
        """Хеширует пароль с помощью bcrypt (соль генерируется автоматически)"""
        if not raw_password:
            self.password = None
            return
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, raw_password: str) -> bool:
        """Проверяет пароль, сравнивая с хранимым хешем"""
        if not self.password:
            return False
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    # --- Для удобства администрирования ---
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['deleted_at']),
            models.Index(fields=['email']),
        ]
        
class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token_hash = models.CharField(max_length=128)   # SHA-256 хеш токена
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def revoke(self):
        self.revoked = True
        self.save()
    
    class Meta:
        db_table = 'refresh_tokens'
        indexes = [
            models.Index(fields=['token_hash']),
            models.Index(fields=['user', 'revoked']),
        ]