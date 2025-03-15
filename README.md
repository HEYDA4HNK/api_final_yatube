# api_final
# Описание
api сервис, который предоставляет пользователям возможность подписываться на других пользователей, искать/создавать посты, Распределять эти самые посты в группы, и оставлять комментарии под постами
# Установка
1. Запстите виртуальное окружение и активируйте его "python -m venv venv", "source venv/Scripts/activate"
2. В терминале пропешите "pip install -r requirements.txt" для установки библиотек
3. Выполните миграции в базу данных "python {путь к manage.py} migrate"
4. Запустите сервер "python {путь к manage.py} runserver"
# Примеры запросов
1. /api/v1/posts/?limit={int}&offset={int}
2. /api/v1/posts/{id}/
3. /api/v1/posts/{post_id}/comments/
4. /api/v1/posts/{post_id}/comments/{id}/
5. /api/v1/groups/
6. /api/v1/groups/{id}/
7. /api/v1/follow/?search={username}
8. /api/v1/jwt/create/
9. /api/v1/jwt/refresh/
10. /api/v1/jwt/verify/
# Финал
