# app/services/leads.py — сервисы для CRUD операций с лидами (бизнес-логика).

"""Сервисы для CRUD операций с лидами — бизнес-логика."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Lead  # модель лида
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
    stmt = select(Lead).where(Lead.id == lead_id)
    db_lead = db.scalar(stmt)
    if not db_lead:
        return None
    return LeadOut.model_validate(db_lead)


def get_leads(db: Session, skip: int = 0, limit: int = 100) -> LeadList:
    """Получить список лидов с пагинацией."""
    items_stmt = select(Lead).offset(skip).limit(limit)
    count_stmt = select(func.count()).select_from(Lead)

    db_leads = db.scalars(items_stmt).all()
    total = db.scalar(count_stmt) or 0

    leads_out = [LeadOut.model_validate(l) for l in db_leads]
    return LeadList(leads=leads_out, total=total)


def update_lead(db: Session, lead_id: UUID, lead_update: LeadUpdate) -> Optional[LeadOut]:
    """Обновить данные лида по ID."""
    stmt = select(Lead).where(Lead.id == lead_id)
    db_lead = db.scalar(stmt)
    if not db_lead:
        return None

    data = lead_update.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_lead, field, value)

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return LeadOut.model_validate(db_lead)


def delete_lead(db: Session, lead_id: UUID) -> bool:
    """Пока просто физически удаляем лида по ID (позже сделаем мягкое удаление)."""
    stmt = select(Lead).where(Lead.id == lead_id)
    db_lead = db.scalar(stmt)
    if not db_lead:
        return False

    db.delete(db_lead)
    db.commit()
    return True
