import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_access_token(user_id: str) -> str:
    """Генерирует JWT access token с коротким сроком жизни."""
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRATION),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    return jwt.encode(payload, settings.JWT_ACCESS_SECRET, algorithm='HS256')

def generate_refresh_token(user_id: str) -> str:
    """Генерирует JWT refresh token с длительным сроком жизни."""
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    return jwt.encode(payload, settings.JWT_REFRESH_SECRET, algorithm='HS256')

def decode_access_token(token: str):
    """Декодирует и проверяет access token."""
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET, algorithms=['HS256'])
        if payload.get('type') != 'access':
            return None
        return payload
    except jwt.InvalidTokenError:
        return None

def decode_refresh_token(token: str):
    """Декодирует и проверяет refresh token."""
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_SECRET, algorithms=['HS256'])
        if payload.get('type') != 'refresh':
            return None
        return payload
    except jwt.InvalidTokenError:
        return None