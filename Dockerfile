# Базовый Dockerfile для backend Skatinov LeadLab
# Используем официальный Python-образ как основу
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости (по минимуму, можно расширить позже)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей (Poetry/requirements) при необходимости
# Для упрощения Дня 5 сделаем установку через pip для FastAPI и Uvicorn
RUN pip install --no-cache-dir fastapi uvicorn

# Копируем весь проект внутрь контейнера
COPY . /app

# Открываем порт 8000 внутри контейнера
EXPOSE 8000

# Команда по умолчанию: запускаем uvicorn с приложением app.main:app
# Позже можно заменить на запуск через твою структуру (например, app.api.main:app)
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
