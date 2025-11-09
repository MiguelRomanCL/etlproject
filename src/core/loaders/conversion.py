"""Data loading utilities for conversion calculations."""

# Standard Library
from typing import Any

# External
from prefect import task
from sqlmodel import Session

# Project
from app.config import LOGGER
from app.db import get_session, upsert_animalshed_conversion


def persist_conversion_results(session: Session, data: list[dict]) -> None:
    """Persist the calculated conversion data into the database."""
    if not data:
        LOGGER.info("No conversion data to persist. Skipping database upsert.")
        return

    try:
        session.exec(upsert_animalshed_conversion(data))
        session.commit()
    except Exception as error:  # pragma: no cover - defensive logging
        LOGGER.error(f"Error saving conversion data: {error}")
        session.rollback()
        raise


def persist_conversion_results_from_any(session: Session, data: list[Any]) -> None:
    """Normalise an arbitrary list of conversion records prior to persistence."""
    parsed_data = [dict(item) if not isinstance(item, dict) else item for item in data]
    persist_conversion_results(session, parsed_data)


@task(name="Load conversion results", retries=2, log_prints=True)
def load_conversion_results(tenant: str, data: list[dict]) -> None:
    """# FLOW: extract→transform→load
    # STEP: load_conversion_results
    Load the conversion computation results into the transactional database.
    """

    with get_session(tenant) as session:
        persist_conversion_results(session, data)


__all__ = [
    "load_conversion_results",
    "persist_conversion_results",
    "persist_conversion_results_from_any",
]
