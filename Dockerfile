# Указываем базовый образ для Python
FROM python:3.11

# Устанавливаем переменную окружения для неинтерактивного режима
ENV PYTHONUNBUFFERED 1

# Создаем директорию внутри контейнера для приложения
WORKDIR /app

# Копируем все файлы из текущей директории в корень контейнера
COPY . .

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && pip install --no-cache-dir -r requirements.txt

# Определяем команду для запуска приложения
CMD ["bash", "-c", "python manage.py runserver & sleep 1 && celery -A welbex.celery worker -l info -P threads & sleep 1 && celery -A welbex beat -l info"]


