"""
Тестовый скрипт для проверки, что конфигурация работает правильно.

Этот скрипт читает настройки из .env.dev и выводит их в консоль.
"""

from app.config import settings, Environment

print("=" * 60)
print("PROVERKA KONFIGURATSII")
print("=" * 60)
print(f"Okruzhenie:        {settings.environment.value}")
print(f"Imya prilozheniya: {settings.app_name}")
print(f"Debug rezhim:      {settings.debug}")
print(f"Baza dannykh:      {settings.database_url}")
print(f"API nazvanie:      {settings.api_title}")
print(f"API versiya:       {settings.api_version}")
print(f"Uroven logov:      {settings.log_level}")
print("=" * 60)
print("[OK] Konfiguratsiya zagruzhena uspeshno!")
print("=" * 60)
