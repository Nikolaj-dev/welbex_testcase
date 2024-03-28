# Используем базовый образ Python 3.8
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файлы проекта внутрь контейнера
COPY . .

# Устанавливаем зависимости Python из requirements.txt
RUN pip install -r requirements.txt

# Команда по умолчанию при запуске контейнера
CMD ["bash"]
