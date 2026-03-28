## 13. Документация

# Лабораторная работа №2: RESTful API для управления персонажами

## Описание проекта

RESTful API для управления игровыми персонажами (на примере Pathfinder 2e). Реализован полный CRUD с мягким удалением (soft delete) и пагинацией. Проект использует Django + Django REST Framework, PostgreSQL в Docker.

## Технологии

- Python 3.12
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL 16
- Docker & Docker Compose

## Запуск проекта

./check_git_config.sh

### Предварительные требования

- Установленный Docker и Docker Compose
- (Опционально) Git для клонирования репозитория

### Шаги для запуска

1. **Клонировать репозиторий**:
   ```bash
   git clone <url-репозитория>
   cd lab_2
   ```

2. **Создать файл `.env`** на основе `.env.example` (см. ниже).

3. **Запустить контейнеры**:
   ```bash
   docker-compose up --build
   ```
   - При первом запуске автоматически выполнятся миграции.
   - API будет доступно по адресу: `http://localhost:4200/api/characters/`

4. **Остановить контейнеры**:
   ```bash
   docker-compose down
   ```

## Переменные окружения

Создайте файл `.env` в корне проекта со следующим содержимым (скопируйте из `.env.example` и при необходимости измените):

```env
# PostgreSQL
DB_USER=student
DB_PASSWORD=student_secure_password
DB_NAME=wp_labs
DB_HOST=postgres
DB_PORT=5432

# Приложение
APP_PORT=4200
```

**Примечание:** файл `.env.example` должен быть в репозитории, а сам `.env` добавлен в `.gitignore`.

## API Endpoints

Базовый URL: `http://localhost:4200/api/characters/`

| Метод   | URI                      | Описание                             | Статус успеха |
|---------|--------------------------|--------------------------------------|---------------|
| GET     | `/`                      | Список персонажей (с пагинацией)     | 200 OK        |
| POST    | `/`                      | Создание нового персонажа            | 201 Created   |
| GET     | `/<uuid:id>/`            | Получение персонажа по ID            | 200 OK        |
| PUT     | `/<uuid:id>/`            | Полное обновление персонажа          | 200 OK        |
| PATCH   | `/<uuid:id>/`            | Частичное обновление персонажа       | 200 OK        |
| DELETE  | `/<uuid:id>/`            | Мягкое удаление персонажа            | 204 No Content|

### Пагинация

Параметры передаются в query string:
- `page` – номер страницы (по умолчанию 1)
- `limit` – количество записей на странице (по умолчанию 10, максимум 100)

**Пример запроса**:
```
GET /api/characters/?page=2&limit=20
```

**Ответ**:
```json
{
  "data": [
    { /* объект персонажа */ }
  ],
  "meta": {
    "total": 42,
    "page": 2,
    "limit": 20,
    "totalPages": 3
  }
}
```

## Миграции

Миграции запускаются автоматически при старте контейнера (команда `python manage.py migrate` в `CMD` Dockerfile). Если необходимо выполнить миграции вручную:

```bash
docker exec -it wp_labs_app python manage.py migrate
```

## Тестирование

Для запуска тестов (внутри контейнера или локально с PostgreSQL):

```bash
python manage.py test characters
```

Все тесты должны проходить успешно.

## Структура проекта

```
lab_2/
├── characters/               # приложение
│   ├── models.py            # модель Character
│   ├── views.py             # контроллеры
│   ├── serializers.py       # сериализаторы
│   ├── services.py          # бизнес-логика
│   ├── exceptions.py        # кастомный обработчик ошибок
│   └── tests.py             # тесты
├── myproject/               # настройки Django
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Ссылки

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker Compose](https://docs.docker.com/compose/)
