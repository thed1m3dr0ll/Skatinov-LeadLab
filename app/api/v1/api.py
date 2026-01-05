# app/api/v1/api.py — корневой роутер API v1

from fastapi import APIRouter

from .health import router as health_router

api_router = APIRouter()

# Подключаю модуль health под /health
api_router.include_router(health_router, prefix="/health", tags=["health"])
