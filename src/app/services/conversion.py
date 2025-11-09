# External
from sqlmodel import Session

# Project
from core.extractors.conversion import (
    fetch_initial_parameters,
    fetch_standard_reference,
    fetch_weight_consumptions,
)
from core.loaders.conversion import persist_conversion_results
from core.transformers.conversion import (
    build_conversion_payload,
    derive_breeding_identifiers,
)


def get_conversion(session: Session) -> list[dict]:
    init_params = fetch_initial_parameters(session)
    id_breeding_list = derive_breeding_identifiers(init_params)
    raw_conversion_rows = fetch_weight_consumptions(session, id_breeding_list)
    standard_df = fetch_standard_reference()

    result_data = build_conversion_payload(init_params, raw_conversion_rows, standard_df)
    persist_conversion_results(session, result_data)
    return result_data
