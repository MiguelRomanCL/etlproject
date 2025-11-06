# Standard Library
import datetime as dt
from typing import Dict

# External
from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase): ...


class Entities(Base):
    __tablename__ = "entities"
    __table_args__ = {"extend_existing": True}
    id_entity: Mapped[int] = mapped_column(primary_key=True)
    idta: Mapped[str]
    parent_id: Mapped[str | None]
    name: Mapped[str]
    operational_state: Mapped[int]
    extra_json: Mapped[Dict | None] = mapped_column(JSON)
    id_entity_type: Mapped[int]
    id_stage: Mapped[int]
    created_at: Mapped[dt.datetime]
    updated_at: Mapped[dt.datetime | None]
    deleted_at: Mapped[dt.datetime | None]
    order: Mapped[int | None]
