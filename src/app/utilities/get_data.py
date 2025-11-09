"""Compatibility layer pointing to the Prefect-ready core utilities."""

# External
from sqlmodel import Session

# Project
from core.extractors.conversion import (
    fetch_initial_parameters as get_init_params,
    fetch_standard_reference as get_standard,
    fetch_weight_consumptions as get_weights_consumptions,
)
from core.loaders.conversion import persist_conversion_results as save_conversion

__all__ = [
    "get_init_params",
    "get_weights_consumptions",
    "get_standard",
    "save_conversion",
    "Session",
]
