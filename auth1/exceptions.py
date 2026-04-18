# auth/exceptions.py
class AuthenticationError(Exception):
    """Ошибка аутентификации (401)."""
    pass

class ConflictError(Exception):
    """Конфликт данных (409)."""
    pass