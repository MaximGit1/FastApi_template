FROM python:3.12.6-alpine

# Устанавливаем зависимости для сборки и работы psycopg
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libpq \
    postgresql-dev \
    python3-dev

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файл pyproject.toml для установки зависимостей
COPY ./pyproject.toml /app/pyproject.toml

# Устанавливаем зависимости через poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . /app
