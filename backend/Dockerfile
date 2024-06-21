# Используем базовый образ Python 3.9-alpine
FROM python:3.9-alpine

# Устанавливаем переменную окружения для работы внутри контейнера
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем requirements.txt и устанавливаем зависимости Python
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое текущей директории в контейнер
COPY . /code/

# Применяем миграции и создаем суперпользователя
RUN python manage.py migrate --noinput

# Команда для запуска сервера Django при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
