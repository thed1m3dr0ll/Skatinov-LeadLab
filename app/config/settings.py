"""
Модуль централизованной конфигурации приложения.

Здесь хранятся все настройки для разных окружений (dev, test, prod).
Настройки читаются из переменных окружения и .env файлов.
Это безопаснее, чем хранить пароли и ключи прямо в коде.
"""

import os
from enum import Enum
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Возможные окружения приложения."""
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class Settings(BaseSettings):
    """
    Главный класс конфигурации.
    
    Pydantic Settings автоматически читает переменные окружения и .env файлы.
    Переменные окружения имеют приоритет над значениями в .env.
    """
    
    # Основные настройки
    environment: Environment = Field(default=Environment.DEV, validation_alias="ENVIRONMENT")
    app_name: str = Field(default="Skatinov LeadLab", validation_alias="APP_NAME")
    debug: bool = Field(default=True, validation_alias="DEBUG")
    
    # База данных
    database_url: str = Field(
        default="sqlite:///./skatinov_dev.db",
        validation_alias="DATABASE_URL"
    )
    
    # API настройки
    api_title: str = Field(default="Skatinov LeadLab API", validation_alias="API_TITLE")
    api_version: str = Field(default="0.1.0", validation_alias="API_VERSION")
    
    # Логирование
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    
    # Безопасность (для prod окружения)
    secret_key: str = Field(
        default="dev-secret-key-not-for-prod",
        validation_alias="SECRET_KEY"
    )
    allowed_hosts: str = Field(
        default="localhost,127.0.0.1",
        validation_alias="ALLOWED_HOSTS"
    )
    
    class Config:
        # Файл .env будет читаться из корня проекта
        env_file = ".env.dev"
        case_sensitive = False
        # Если переменная окружения установлена, она имеет приоритет


def get_settings(env: str = None) -> Settings:
    """
    Получить настройки для конкретного окружения.
    
    Читает переменную окружения ENVIRONMENT или используется переданный параметр env.
    Затем читает соответствующий .env файл (.env.dev, .env.test или .env.prod).
    
    Пример:
        settings = get_settings()  # читает из ENVIRONMENT или .env.dev по умолчанию
        settings = get_settings("prod")  # читает из .env.prod
    """
    # Получаем окружение из переменной окружения или параметра
    environment = env or os.getenv("ENVIRONMENT", Environment.DEV.value)
    
    # Определяем путь к .env файлу в зависимости от окружения
    env_file = f".env.{environment}"
    
    # Проверяем, существует ли файл
    if not Path(env_file).exists():
        raise FileNotFoundError(
            f"Файл конфигурации {env_file} не найден. "
            f"Создай его на основе {env_file}.example"
        )
    
    # Создаём объект Settings с правильным .env файлом
    return Settings(_env_file=env_file)


# По умолчанию экспортируем настройки для текущего окружения
settings = get_settings()
