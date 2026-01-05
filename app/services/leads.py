# app/services/leads.py — сервисы для CRUD операций с лидами (бизнес-логика).
"""Сервисы для CRUD операций с лидами — бизнес-логика."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from uuid import UUID

from app.models import Lead  # Предполагаем, что модель Lead уже существует
from app.schemas.leads import LeadCreate, LeadUpdate, LeadOut, LeadList


def create_lead(db: Session, lead_in: LeadCreate) -> LeadOut:
    """Создать новый лид."""
    db_lead = Lead(**lead_in.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return LeadOut.model_validate(db_lead)


def get_lead(db: Session, lead_id: UUID) -> Optional[LeadOut]:
    """Получить лид по ID."""
    query = select(Lead).where(Lead.id == lead_id)
    db_lead = db.scalar(query)
    return LeadOut.model_validate(db_lead) if db_lead else None


def get_leads(db: Session, skip: int = 0, limit: int = 100) -> LeadList:
    """Получить список лидов с пагинацией."""
    query = select(Lead).offset(skip).limit(limit)
    leads = db.scalars(query).all()
    total = db.scalar(select(func.count()).select_from(Lead))
    return LeadList(leads=[LeadOut.model_validate(l) for l in leads], total=total)


def update_lead(db: Session, lead_id: UUID, lead_update: LeadUpdate) -> Optional[LeadOut]:
    """Обновить лид по ID."""
    data = lead_update.model_dump(exclude_unset=True)
    if not data:
        return get_lead(db, lead_id)
    
    query = update(Lead).where(Lead.id == lead_id).values(**data).returning(Lead)
    db_lead = db.scalar(query)
    db.commit()
    return LeadOut.model_validate(db_lead) if db_lead else None


def delete_lead(db: Session, lead_id: UUID) -> bool:
    """Мягко удалить лид (пометить как закрытый — добавь поле is_closed в модель позже)."""
    # Пока просто удаляем, потом сделаем soft delete
    query = update(Lead).where(Lead.id == lead_id).values(is_deleted=True)  # TODO: добавить поле is_deleted
    result = db.execute(query)
    db.commit()
    return result.rowcount > 0
