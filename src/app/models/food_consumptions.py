# Standard Library
import datetime as dt

# External
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase): ...


class FoodConsumption(Base):
    __tablename__ = "food_consumptions"
    id_food_consumption: Mapped[int] = mapped_column(primary_key=True)
    id_breeding: Mapped[int]
    date: Mapped[dt.datetime]
    animals_age: Mapped[int]
    entity_daily_consumption: Mapped[float]
    animal_daily_consumption: Mapped[float]
    entity_daily_standard_consumption: Mapped[float]
    animal_daily_standard_consumption: Mapped[float]
    entity_accumulated_consumption: Mapped[float]
    animal_accumulated_consumption: Mapped[float]
    entity_accumulated_standard_consumption: Mapped[float]
    animal_accumulated_standard_consumption: Mapped[float]
    imputated: Mapped[int]
    calculation_formula_version: Mapped[str]
    created_at: Mapped[dt.datetime]
    updated_at: Mapped[dt.datetime]
    deleted_at: Mapped[dt.datetime]
