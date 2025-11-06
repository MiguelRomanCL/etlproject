# Standard Library
import datetime as dt
from typing import Dict

# External
from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase): ...


class Breedings(Base):
    __tablename__ = "breedings"
    __table_args__ = {"extend_existing": True}
    id_breeding: Mapped[int] = mapped_column(primary_key=True)
    idta: Mapped[str]
    start_date: Mapped[dt.date]
    end_date: Mapped[dt.date]
    breeding_code: Mapped[str]
    createdAt: Mapped[dt.datetime]
    updatedAt: Mapped[dt.datetime]
    deletedAt: Mapped[dt.datetime]
    createdBy: Mapped[str]
    updatedBy: Mapped[str]
    deletedBy: Mapped[str]


class BreedingData(Base):
    __tablename__ = "breeding_data"
    __table_args__ = {"extend_existing": True}
    id_breeding_data: Mapped[int] = mapped_column(primary_key=True)
    id_breeding: Mapped[int]
    sex: Mapped[str]
    initial_weight_avg: Mapped[float]
    start_date_loaded: Mapped[dt.date]
    initial_age: Mapped[int]
    initial_male_quantity: Mapped[int]
    initial_female_quantity: Mapped[int]
    initial_total_quantity: Mapped[int]
    extra_json: Mapped[Dict | None] = mapped_column(JSON)
    created_at: Mapped[dt.datetime]
    updated_at: Mapped[dt.datetime]
    deleted_at: Mapped[dt.datetime]
    final_total_quantity: Mapped[int]
    final_weight_avg: Mapped[float]
    final_age: Mapped[int]
    created_by: Mapped[str]
    updated_by: Mapped[str]
    deleted_by: Mapped[str]


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
