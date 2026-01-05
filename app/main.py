# app/main.py — точка входа FastAPI-приложения

import time
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router as api_v1_router
from app.config.settings import settings  # глобальные настройки проекта


logger = logging.getLogger("skatinov_leadlab")


def create_app() -> FastAPI:
    """
    Фабрика приложения FastAPI.

    Здесь я:
    - подтягиваю конфигурацию из settings,
    - регистрирую middleware (логирование, CORS),
    - подключаю версионированные роутеры /api/v1/*.
    """
    app = FastAPI(
        title="Skatinov LeadLab",
        version=getattr(settings, "APP_VERSION", "0.1.0"),
        description=getattr(
            settings,
            "APP_DESCRIPTION",
            "Серьёзный FastAPI‑проект для лидогенерации.",
        ),
        debug=getattr(settings, "DEBUG", True),
    )

    # ---------- Middleware логирования ----------

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """
        Простое HTTP‑middleware для логирования.

        Я логирую:
        - метод и путь запроса,
        - код ответа,
        - время обработки.

        Тела запросов и ответов не читаю, чтобы не светить секреты и не замедлять обработку.
        """
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as exc:
            process_time = time.time() - start_time
            logger.exception(
                "Unhandled error: %s %s (%.3f s)",
                request.method,
                request.url.path,
                process_time,
            )
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

        process_time = time.time() - start_time
        logger.info(
            "%s %s -> %s (%.3f s)",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )
        return response

    # ---------- CORS для фронтенда ----------

    # Разрешаю запросы с локального фронтенда (React/Vue и т.п.)
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------- Роутеры ----------

    # Подключаю роутер версии API v1 с префиксом /api/v1
    app.include_router(api_v1_router, prefix="/api/v1")

    return app


# Экземпляр приложения, который будет запускать Uvicorn
app = create_app()
