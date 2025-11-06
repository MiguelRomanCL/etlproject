# External
import polars as pl

###################
from sqlmodel import Session

# Project
from app.config import LOGGER, VERSION
from app.schemas import weight_consumption_schema
from app.utilities import get_init_params, get_standard, get_weights_consumptions, save_conversion

def get_conversion(session: Session) -> list[dict]:
    init_params = get_init_params(session)
    init_params

    id_breeding_list = list(set([i.id_breeding for i in init_params]))
    convert_data_df = get_weights_consumptions(session, id_breeding_list)

    init_df = pl.DataFrame(data=init_params)
    convert_data_df = pl.DataFrame(
        data=convert_data_df, orient="row", schema=weight_consumption_schema
    )

    if convert_data_df.is_empty():
        LOGGER.warning("No conversion data found for the breeding list. Returning empty result.")
        return []

    standard_df = get_standard()
    if init_df.is_empty():
        LOGGER.warning("No initial parameters found. Returning empty result.")
        return []

    convert_data_df = convert_data_df.with_columns(
        stock=pl.when(pl.col("animals_age") == pl.col("initial_age"))
        .then(pl.col("initial_total_quantity"))
        .otherwise(pl.col("stock"))
    )
    prodhouse_del = (
        convert_data_df.filter(pl.col("stock").is_null())["id_breeding"].unique().to_list()
    )

    for idbreeding_i in prodhouse_del:
        clean_df = convert_data_df.filter(pl.col("id_breeding") == idbreeding_i).drop_nulls(
            subset=pl.col("stock")
        )
        initial_stock = (
            convert_data_df.filter(pl.col("id_breeding") == idbreeding_i)["initial_total_quantity"]
            .unique()
            .item()
        )

        if clean_df.is_empty() and initial_stock:
            convert_data_df = convert_data_df.with_columns(
                stock=pl.when(pl.col("id_breeding") == idbreeding_i)
                .then(pl.col("initial_total_quantity"))
                .otherwise(pl.col("stock"))
            )
        elif not clean_df.is_empty():
            ## Imputar stocks por ultimo valor disponible
            latest_stock = (
                clean_df.filter(pl.col("id_breeding") == idbreeding_i)
                .sort("date")
                .tail(n=1)["stock"]
                .item()
            )
            convert_data_df = convert_data_df.with_columns(
                stock=pl.when(pl.col("id_breeding") == idbreeding_i)
                .then(pl.lit(latest_stock))
                .otherwise(pl.col("stock"))
            )
        else:
            convert_data_df = convert_data_df.remove((pl.col("id_breeding") == idbreeding_i))
            LOGGER.warning(f"No stock values for {idbreeding_i}. Impossible to replace or impute.")

    convert_data_df = convert_data_df.with_columns(
        animal_accumulated_conversion=(
            pl.col("animal_accumulated_consumption")
            / (pl.col("measured_weight") - pl.col("initial_weight_avg"))
        ).round(6),
        weight_delta=(pl.col("measured_weight") * pl.col("stock"))
        - (pl.col("initial_weight_avg") * pl.col("initial_total_quantity")),
    )
    convert_data_df = convert_data_df.with_columns(
        entity_accumulated_conversion=(
            pl.col("entity_accumulated_consumption") / pl.col("weight_delta")
        ).round(6),
        calculation_formula_version=pl.lit(VERSION),
    )
    zero_cond_entity = (pl.col("entity_accumulated_conversion") < 0) | (
        pl.col("entity_accumulated_conversion").is_infinite()
    )
    zero_cond_animal = (pl.col("animal_accumulated_conversion") < 0) | (
        pl.col("animal_accumulated_conversion").is_infinite()
    )
    convert_data_df = convert_data_df.with_columns(
        entity_accumulated_conversion=pl.when(zero_cond_entity)
        .then(pl.lit(0))
        .otherwise(pl.col("entity_accumulated_conversion")),
        animal_accumulated_conversion=pl.when(zero_cond_animal)
        .then(pl.lit(0))
        .otherwise(pl.col("animal_accumulated_conversion")),
    )
    convert_data_df = convert_data_df.join(other=init_df, on="id_breeding", how="left").join(
        other=standard_df, on=["animals_age", "sex", "id_stage"], how="left"
    )

    convert_data_df = convert_data_df[
        [
            "id_breeding",
            "animals_age",
            "date",
            "animal_accumulated_conversion",
            "animal_accumulated_standard_conversion",
            "entity_accumulated_conversion",
        ]
    ]
    convert_data_df = convert_data_df.rename(
        {"animal_accumulated_standard_conversion": "accumulated_standard_conversion"}
    )
    convert_data_df = convert_data_df.with_columns(
        date=pl.col("date").cast(pl.Date), calculation_formula_version=pl.lit(VERSION)
    )

    result_data = convert_data_df.to_dicts()
    save_conversion(session, data=result_data)
    return result_data
