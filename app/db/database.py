"""
Модуль для подключения к базе данных и базового класса моделей.

Здесь настраивается SQLAlchemy engine, фабрика сессий и Base,
от которого будут наследоваться все модели БД.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings  # берём DATABASE_URL из настроек


# URL базы данных берётся из конфигурации (dev/test/prod)
DATABASE_URL = settings.database_url


# Создаём движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # можно включить True, чтобы видеть SQL-запросы в консоли
)


# Фабрика сессий для работы с базой (через зависимости в FastAPI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Базовый класс для всех моделей
Base = declarative_base()
