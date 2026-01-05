"""Схемы Pydantic для лидов — валидация входных/выходных данных."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class LeadCreate(BaseModel):
    """Схема для создания лида."""
    name: str = Field(..., min_length=1, max_length=255, description="Имя лида")
    email: str = Field(..., description="Email лида")
    phone: Optional[str] = Field(None, max_length=20, description="Телефон лида")
    company: Optional[str] = Field(None, max_length=255, description="Компания")
    assigned_to_id: Optional[UUID] = Field(None, description="ID ответственного (для авторизации позже)")


class LeadUpdate(BaseModel):
    """Схема для обновления лида."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=255)
    assigned_to_id: Optional[UUID] = Field(None)


class LeadOut(BaseModel):
    """Схема для чтения лида — полный вывод."""
    id: UUID
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    assigned_to_id: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy/SqlModel


class LeadList(BaseModel):
    """Схема для списка лидов."""
    leads: list[LeadOut]
    total: int
