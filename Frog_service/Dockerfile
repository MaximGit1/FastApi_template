FROM python:3.12.6-alpine

RUN pip install poetry

WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY alembic.ini .