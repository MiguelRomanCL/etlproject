# Standard Library
import datetime as dt

# External
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase): ...


class Mortality(Base):
    __tablename__ = "mortalities"

    id_mortality: Mapped[int] = mapped_column(primary_key=True)
    id_mortality_type: Mapped[int]
    id_breeding: Mapped[int]
    date_mortality: Mapped[dt.date]
    animals_age: Mapped[int]
    quantity: Mapped[int]
    created_at: Mapped[dt.datetime]
    updated_at: Mapped[dt.datetime]
    deleted_at: Mapped[dt.datetime]
    created_by: Mapped[str]
    updated_by: Mapped[str]
    deleted_by: Mapped[str]
    change: Mapped[bool]
    stock: Mapped[int]
