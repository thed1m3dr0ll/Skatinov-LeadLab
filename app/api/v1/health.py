# app/api/v1/health.py — базовый health‑чек приложения

from fastapi import APIRouter

router = APIRouter()


@router.get("", summary="Базовый health-check сервиса")
async def health_root():
    """
    Простейший health‑эндпоинт.

    На этом уровне я проверяю только то, что приложение запущено
    и обрабатывает HTTP‑запросы. Позже сюда добавлю проверки БД, брокера и т.п.
    """
    return {
        "status": "ok",
        "service": "skatinov-leadlab",
        "details": "base app is up",
    }
