# External
import polars as pl


weight_consumption_schema = {
    "measured_weight": pl.Float64,
    "animals_age": pl.Int64,
    "date": pl.Datetime,
    "entity_accumulated_consumption": pl.Float64,
    "animal_accumulated_consumption": pl.Float64,
    "stock": pl.Int64,
    "initial_weight_avg": pl.Float64,
    "initial_age": pl.Int64,
    "initial_total_quantity": pl.Int64,
    "id_breeding": pl.Int64,
}
