# app/api/v1/leads.py — API-маршруты FastAPI для лидов (CRUD).

"""Маршруты FastAPI для работы с лидами (CRUD)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db  # зависимость для получения сессии БД
from app.schemas.leads import LeadCreate, LeadUpdate, LeadOut, LeadList
from app.services.leads import (
    create_lead,
    get_lead,
    get_leads,
    update_lead,
    delete_lead,
)

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post(
    "",
    response_model=LeadOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый лид",
)
def create_lead_endpoint(lead_in: LeadCreate, db: Session = Depends(get_db)):
    """Эндпоинт для создания нового лида."""
    return create_lead(db=db, lead_in=lead_in)


@router.get(
    "",
    response_model=LeadList,
    summary="Получить список лидов",
)
def list_leads_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Эндпоинт для получения списка лидов с пагинацией."""
    return get_leads(db=db, skip=skip, limit=limit)


@router.get(
    "/{lead_id}",
    response_model=LeadOut,
    summary="Получить лид по ID",
)
def get_lead_endpoint(lead_id: UUID, db: Session = Depends(get_db)):
    """Эндпоинт для получения одного лида по его ID."""
    lead = get_lead(db=db, lead_id=lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лид не найден")
    return lead


@router.put(
    "/{lead_id}",
    response_model=LeadOut,
    summary="Полное обновление лида по ID",
)
def update_lead_put_endpoint(
    lead_id: UUID,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db),
):
    """Эндпоинт для полного обновления лида по ID."""
    updated = update_lead(db=db, lead_id=lead_id, lead_update=lead_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лид не найден")
    return updated


@router.patch(
    "/{lead_id}",
    response_model=LeadOut,
    summary="Частичное обновление лида по ID",
)
def update_lead_patch_endpoint(
    lead_id: UUID,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db),
):
    """Эндпоинт для частичного обновления лида по ID."""
    updated = update_lead(db=db, lead_id=lead_id, lead_update=lead_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лид не найден")
    return updated


@router.delete(
    "/{lead_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить (временно — физически) лида по ID",
)
def delete_lead_endpoint(lead_id: UUID, db: Session = Depends(get_db)):
    """Эндпоинт для удаления лида по ID (пока без мягкого удаления)."""
    deleted = delete_lead(db=db, lead_id=lead_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лид не найден")
    # 204 без тела ответа
