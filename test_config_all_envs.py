"""
Тестовый скрипт для проверки всех трёх окружений.

Показывает, как конфигурация меняется в зависимости от окружения.
"""

from app.config import get_settings, Environment

print("\n" + "=" * 70)
print("TESTIROVANIE VSEKH OKRUZHENII (dev, test, prod)")
print("=" * 70)

# Тестируем dev окружение
print("\n[1] OKRUZHENIE: DEV")
print("-" * 70)
dev_settings = get_settings("dev")
print(f"Okruzhenie:        {dev_settings.environment.value}")
print(f"Imya:              {dev_settings.app_name}")
print(f"Debug:             {dev_settings.debug}")
print(f"BD:                {dev_settings.database_url}")
print(f"API nazvanie:      {dev_settings.api_title}")
print(f"Uroven logov:      {dev_settings.log_level}")

# Тестируем test окружение
print("\n[2] OKRUZHENIE: TEST")
print("-" * 70)
test_settings = get_settings("test")
print(f"Okruzhenie:        {test_settings.environment.value}")
print(f"Imya:              {test_settings.app_name}")
print(f"Debug:             {test_settings.debug}")
print(f"BD:                {test_settings.database_url}")
print(f"API nazvanie:      {test_settings.api_title}")
print(f"Uroven logov:      {test_settings.log_level}")

# Тестируем prod окружение
print("\n[3] OKRUZHENIE: PROD")
print("-" * 70)
prod_settings = get_settings("prod")
print(f"Okruzhenie:        {prod_settings.environment.value}")
print(f"Imya:              {prod_settings.app_name}")
print(f"Debug:             {prod_settings.debug}")
print(f"BD:                {prod_settings.database_url}")
print(f"API nazvanie:      {prod_settings.api_title}")
print(f"Uroven logov:      {prod_settings.log_level}")

print("\n" + "=" * 70)
print("[OK] Vse tri okruzheniia zagruzheny uspeshno!")
print("=" * 70 + "\n")
