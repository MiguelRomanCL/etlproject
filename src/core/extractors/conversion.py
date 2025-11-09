"""Data extraction utilities for conversion workflows."""

# Standard Library
from typing import Any

# External
import polars as pl
from prefect import task
from sqlmodel import Session

# Project
from app.config import LOGGER
from app.db import (
    get_session,
    select_breeding_weights_consumption_data,
    select_init_params,
)


def fetch_initial_parameters(session: Session) -> list[Any]:
    """Retrieve the initial breeding parameters required for conversion."""
    try:
        result = session.exec(select_init_params()).all()
        return result
    except Exception as error:  # pragma: no cover - defensive logging
        LOGGER.error(f"Error fetching init params: {error}")
        raise


def fetch_weight_consumptions(session: Session, id_breeding_list: list[int]) -> list[Any]:
    """Retrieve weight and consumption records for the provided breeding identifiers."""
    try:
        result = session.exec(
            select_breeding_weights_consumption_data(id_breeding_list)
        ).all()
        return result
    except Exception as error:  # pragma: no cover - defensive logging
        LOGGER.error(
            "Error fetching weights and consumptions for breeding list %s: %s",
            id_breeding_list,
            error,
        )
        raise


def fetch_standard_reference() -> pl.DataFrame:
    """Load the standard conversion reference from CSV sources."""
    pollos = pl.read_csv("maestroestandargenetica_202510160912_pollos.csv")
    cerdos = pl.read_csv("maestroestandargenetica_202510161619_cerdos.csv")
    pollos = pollos.with_columns(id_stage=pl.lit(1))
    cerdos = cerdos.with_columns(id_stage=pl.lit(2))

    std = pl.concat(
        items=[
            pollos[
                "edad",
                "sexo",
                "nombreGenetica",
                "conversion",
                "conversionAcumulada",
                "id_stage",
            ],
            cerdos[
                "edad",
                "sexo",
                "nombreGenetica",
                "conversion",
                "conversionAcumulada",
                "id_stage",
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


@task(name="Extract initial parameters", retries=2, log_prints=True)
def extract_initial_parameters(tenant: str) -> list[Any]:
    """# FLOW: extract→transform→load
    # STEP: extract_initial_parameters
    Extract the initial breeding parameters for the Prefect-managed conversion flow.
    """

    with get_session(tenant) as session:
        return fetch_initial_parameters(session)


@task(name="Extract weight consumptions", retries=2, log_prints=True)
def extract_weight_consumptions(tenant: str, id_breeding_list: list[int]) -> list[Any]:
    """# FLOW: extract→transform→load
    # STEP: extract_weight_consumptions
    Extract weight and consumption measurements required to compute conversions.
    """

    with get_session(tenant) as session:
        return fetch_weight_consumptions(session, id_breeding_list)


@task(name="Extract standard conversion", retries=1, log_prints=True)
def extract_standard_conversion() -> pl.DataFrame:
    """# FLOW: extract→transform→load
    # STEP: extract_standard_conversion
    Load the standard conversion reference table from the local CSV catalogue.
    """

    return fetch_standard_reference()


__all__ = [
    "extract_initial_parameters",
    "extract_standard_conversion",
    "extract_weight_consumptions",
    "fetch_initial_parameters",
    "fetch_standard_reference",
    "fetch_weight_consumptions",
]
