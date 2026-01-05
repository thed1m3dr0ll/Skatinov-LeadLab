# Простейшая заглушка FastAPI для Docker-стенда
# Здесь пока нет реальной логики CRM, только проверка, что backend-контейнер живой

from fastapi import FastAPI

app = FastAPI(title="Skatinov LeadLab (Docker stub)")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "backend",
        "env": "docker",
    }
