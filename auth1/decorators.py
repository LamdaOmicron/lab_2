# auth/decorators.py
from functools import wraps
from django.http import JsonResponse

def login_required(view_func):
    """
    Декоратор для защиты эндпоинтов: возвращает 401, если пользователь не аутентифицирован.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or request.user is None:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper