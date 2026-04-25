import hashlib

def hash_token(token: str) -> str:
    """Возвращает SHA-256 хеш строки токена (для хранения в БД)."""
    return hashlib.sha256(token.encode()).hexdigest()