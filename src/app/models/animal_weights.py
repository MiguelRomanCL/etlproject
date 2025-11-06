# Standard Library
import datetime as dt

# External
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase): ...


class AnimalWeights(Base):
    __tablename__ = "animal_weights"
    id_animal_weight: Mapped[int] = mapped_column(primary_key=True)
    animals_age: Mapped[int]
    id_breeding: Mapped[int]
    date: Mapped[dt.datetime]
    standard_weight: Mapped[float]
    measured_weight: Mapped[float]
    trending_weight: Mapped[float]
    imputated: Mapped[int]
    profit: Mapped[float]
    standar_increase: Mapped[float]
    mean_increase_period: Mapped[float]
    total_mean_increase: Mapped[float]
    standard_mean_increase: Mapped[float]
    uniformity: Mapped[float]
    calculation_formula_version: Mapped[str]
    created_at: Mapped[dt.datetime]
    updated_at: Mapped[dt.datetime]
    deleted_at: Mapped[dt.datetime]
