"""Prefect main flow orchestrating the conversion ETL pipeline."""

# External
from prefect import flow

# Project
from app.config import LOGGER
from core.extractors.conversion import (
    extract_initial_parameters,
    extract_standard_conversion,
    extract_weight_consumptions,
)
from core.loaders.conversion import load_conversion_results
from core.transformers.conversion import (
    derive_breeding_identifiers_task,
    transform_conversion_records,
)


@flow(name="main_flow")
def main_flow(tenant: str) -> list[dict]:
    """# FLOW: extract→transform→load
    # STEP: orchestrate_main_conversion_flow
    Orchestrate the conversion ETL process under Prefect control.
    """

    LOGGER.info("Starting Prefect conversion flow for tenant: %s", tenant)

    init_params_future = extract_initial_parameters.submit(tenant=tenant)
    ids_future = derive_breeding_identifiers_task.submit(init_params_future)
    weight_consumptions_future = extract_weight_consumptions.submit(
        tenant=tenant, id_breeding_list=ids_future
    )
    standard_future = extract_standard_conversion.submit()
    transformed_future = transform_conversion_records.submit(
        init_params_future, weight_consumptions_future, standard_future
    )
    load_conversion_results.submit(tenant=tenant, data=transformed_future)

    final_result = transformed_future.result()
    LOGGER.info("Completed Prefect conversion flow for tenant: %s", tenant)
    return final_result


__all__ = ["main_flow"]
