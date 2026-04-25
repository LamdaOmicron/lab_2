# auth/middleware.py
import logging
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .utils.jwt_utils import decode_access_token
from users.models import User

logger = logging.getLogger(__name__)

class JWTAuthMiddleware(MiddlewareMixin):
    """
    Middleware для аутентификации через JWT access token в cookies.
    Устанавливает request.user, если токен валиден.
    """

    def process_request(self, request):
        # Извлекаем access token из cookies
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            request.user = None
            return

        # Декодируем и проверяем токен
        payload = decode_access_token(access_token)
        if not payload:
            logger.debug(f"Invalid access token for request: {request.path}")
            request.user = None
            return

        user_id = payload.get('user_id')
        if not user_id:
            request.user = None
            return

        try:
            # Ищем пользователя (активного, не удалённого)
            user = User.objects.get(id=user_id, deleted_at__isnull=True)
            request.user = user
        except User.DoesNotExist:
            logger.warning(f"User {user_id} not found or deleted, but token valid")
            request.user = None