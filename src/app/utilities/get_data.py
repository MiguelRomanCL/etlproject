# Standard Library
from typing import Any

# External
import polars as pl
from sqlmodel import Session

# Project
from app.config import LOGGER
from app.db import (
    select_breeding_weights_consumption_data,
    select_init_params,
    upsert_animalshed_conversion,
)


def get_init_params(session: Session) -> list[Any]:
    try:
        result = session.exec(select_init_params())
        result = result.all()
        return result
    except Exception as e:
        LOGGER.error(f"Error fetching init params: {e}")
        raise


def get_weights_consumptions(session: Session, id_breeding_list: list[int]) -> list[Any]:
    try:
        result = session.exec(select_breeding_weights_consumption_data(id_breeding_list))
        result = result.all()
        return result
    except Exception as e:
        LOGGER.error(
            f"Error fetching weights and consumptions for breeding list {id_breeding_list}: {e}"
        )
        raise


def get_standard() -> pl.DataFrame:
    pollos = pl.read_csv("maestroestandargenetica_202510160912_pollos.csv")
    cerdos = pl.read_csv("maestroestandargenetica_202510161619_cerdos.csv")
    pollos = pollos.with_columns(id_stage=pl.lit(1))
    cerdos = cerdos.with_columns(id_stage=pl.lit(2))

    std = pl.concat(
        items=[
            pollos[
                "edad", "sexo", "nombreGenetica", "conversion", "conversionAcumulada", "id_stage"
            ],
            cerdos[
                "edad", "sexo", "nombreGenetica", "conversion", "conversionAcumulada", "id_stage"
            ],
        ]
    )
    std = std.filter(pl.col("nombreGenetica") == "ROSS - 2020")
    std = std.rename(
        {
            "conversionAcumulada": "animal_daily_standard_conversion",
            "conversion": "animal_accumulated_standard_conversion",
            "edad": "animals_age",
            "sexo": "sex",
        }
    )

    return std


def save_conversion(session: Session, data: list[dict]) -> None:
    try:
        session.exec(upsert_animalshed_conversion(data))
        session.commit()
    except Exception as e:
        LOGGER.error(f"Error saving conversion data: {e}")
        session.rollback()
        raise
