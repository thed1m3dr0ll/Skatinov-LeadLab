"""
Модель лида (потенциального клиента) для CRM Skatinov LeadLab.

В этой таблице мы храним основную информацию о лиде:
- имя и email для связи;
- источник (откуда пришёл лид: сайт, реклама, офлайн);
- статус (новый, в работе, завершён и т.д.);
- ответственный менеджер;
- даты создания и обновления записи.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Lead(Base):
    """Модель лида. Каждая запись — один потенциальный клиент."""

    __tablename__ = "leads"

    # Уникальный идентификатор лида
    id = Column(Integer, primary_key=True, index=True)

    # Имя лида (как к нему обращаться)
    name = Column(String(200), nullable=False, index=True)

    # Основной email для связи
    email = Column(String(255), nullable=False, index=True)

    # Статус лида (например: new, in_progress, won, lost)
    status = Column(String(50), nullable=False, index=True, default="new")

    # Источник лида (например: website, facebook, referral)
    source = Column(String(100), nullable=True, index=True)

    # Ответственный менеджер (пока просто строка с именем)
    assigned_to = Column(String(100), nullable=True, index=True)

    # Время создания записи
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Время последнего обновления записи
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
