# app/schemas/leads.py — Pydantic-схемы для лидов (входные и выходные данные API).

"""Схемы Pydantic для лидов — валидация входных/выходных данных."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    """Схема для создания лида."""
    name: str = Field(..., min_length=1, max_length=200, description="Имя лида")
    email: str = Field(..., max_length=255, description="Email лида")
    status: Optional[str] = Field("new", max_length=50, description="Статус лида")
    source: Optional[str] = Field(None, max_length=100, description="Источник лида")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Ответственный менеджер")


class LeadUpdate(BaseModel):
    """Схема для обновления лида."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=50)
    source: Optional[str] = Field(None, max_length=100)
    assigned_to: Optional[str] = Field(None, max_length=100)


class LeadOut(BaseModel):
    """Схема для чтения лида — полный вывод."""
    id: int
    name: str
    email: str
    status: str
    source: Optional[str]
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # для совместимости с SQLAlchemy


class LeadList(BaseModel):
    """Схема для списка лидов."""
    leads: list[LeadOut]
    total: int
