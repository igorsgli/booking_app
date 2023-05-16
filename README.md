## Проект "Бронирование"

### Описание

Проект "Бронирование" - сервис управления бронированием отелей.
Пользователи могут искать, бронировать и отменять бронирования номеров в гостиницах.

### Шаблон наполнения env-файла

```
DB_HOST=localhost # адрес БД
DB_PORT=5432 # порт для подключения к БД
DB_USER=postgres # логин для подключения к базе данных
DB_PASS=postgres # пароль для подключения к БД (установите свой)
DB_NAME=postgres # имя базы данных

SMTP_HOST=smtp_host # адрес почтового сервера
SMTP_PORT=465 # порт для подключения к почтовому серверу
SMTP_USER=username # email адрес
SMTP_PASS=password # пароль для подключения к почтовому серверу

REDIS_HOST=localhost # адрес Redis
REDIS_PORT=6379 # порт для подключения к Redis

SECRET_KEY=secret_key # секретный ключ
ALGORITHM=HS256 # алгоритм
```

### Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/igorsgli/booking_app.git
```

```
cd booking_app
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
alembic upgrade head
```

Запустить проект:

```
uvicorn app.main:app --reload
```

Запустить параллельно celery:

```
celery -A app.tasks.celery:celery worker --loglevel=INFO
```
