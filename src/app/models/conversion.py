# Standard Library
import datetime as dt

# External
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase): ...


class AnimalConversion(Base):
    __tablename__ = "animal_conversion"

    id_animal_conversion: Mapped[int] = mapped_column(primary_key=True)
    id_breeding: Mapped[int]
    date: Mapped[dt.date]
    animals_age: Mapped[int | None]
    entity_accumulated_conversion: Mapped[float | None]
    animal_accumulated_conversion: Mapped[float | None]
    accumulated_standard_conversion: Mapped[float | None]
    calculation_formula_version: Mapped[str | None]
    created_at: Mapped[dt.datetime]
    updated_at: Mapped[dt.datetime | None]
    deleted_at: Mapped[dt.datetime | None]
