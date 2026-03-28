import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError

logger = logging.getLogger(__name__)
class ConflictError(Exception):
    """Исключение для конфликта данных (например, попытка создать дубликат)."""
    pass


def custom_exception_handler(exc, context):
    # Сначала вызываем стандартный обработчик DRF
    response = exception_handler(exc, context)

    if response is not None:
        return response

    # Обрабатываем кастомные исключения
    if isinstance(exc, ConflictError):
        return Response(
            {"error": str(exc)},
            status=status.HTTP_409_CONFLICT
        )

    if isinstance(exc, DjangoValidationError):
        return Response(
            {"error": exc.messages[0] if exc.messages else "Ошибка валидации"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, IntegrityError):
        return Response(
            {"error": "Конфликт данных: запись уже существует"},
            status=status.HTTP_409_CONFLICT
        )

    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return Response(
        {"error": "Внутренняя ошибка сервера"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )