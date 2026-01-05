# Базовый Dockerfile для backend Skatinov LeadLab
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаю минимальные системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Устанавливаю зависимости проекта напрямую через pip
# (без установки самого пакета по pyproject.toml)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    "pydantic-settings>=2.12.0,<3.0.0" \
    "python-dotenv>=1.2.1,<2.0.0" \
    "sqlalchemy>=2.0.45,<3.0.0" \
    "alembic>=1.17.2,<2.0.0" \
    "psycopg2-binary>=2.9.9,<3.0.0"

# Копирую весь проект внутрь контейнера
COPY . /app

# Открываю порт 8000 внутри контейнера
EXPOSE 8000

# Команда по умолчанию: запускаю uvicorn с приложением app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
