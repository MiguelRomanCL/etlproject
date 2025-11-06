# External
from sqlalchemy import BigInteger, String, and_, cast, literal_column, select
from sqlalchemy.dialects.mysql import Insert as InsertMySQL
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.sql import Select, and_, select

# Project
from app.models import (
    AnimalConversion,
    AnimalWeights,
    BreedingData,
    Breedings,
    Entities,
    FoodConsumption,
    Mortality,
)


def select_init_params() -> Select:
    return (
        select(
            cast(Breedings.idta, BigInteger),
            cast(Entities.parent_id, BigInteger),
            Breedings.breeding_code,
            literal_column("'ROSS - 2020'", String).label("geneticaPredominante"),
            BreedingData.sex,
            Breedings.id_breeding,
            Entities.id_stage,
        )
        .join(Entities, Entities.idta == Breedings.idta)
        .join(BreedingData, BreedingData.id_breeding == Breedings.id_breeding)
        .filter(
            and_(
                Breedings.end_date.is_(None),
                Entities.parent_id.is_not(None),
                Entities.id_stage == 1,
                ## Ensure not None
                Breedings.start_date.is_not(None),
                BreedingData.initial_age.is_not(None),
                BreedingData.initial_weight_avg.is_not(None),
                BreedingData.sex.is_not(None),
            )
        )
    )


def select_breeding_weights_consumption_data(id_breeding: list[int]) -> Select:
    return (
        select(
            AnimalWeights.measured_weight,
            AnimalWeights.animals_age,
            AnimalWeights.date,
            FoodConsumption.entity_accumulated_consumption,
            FoodConsumption.animal_accumulated_consumption,
            Mortality.stock,
            BreedingData.initial_weight_avg,
            BreedingData.initial_age,
            BreedingData.initial_total_quantity,
            BreedingData.id_breeding,
        )
        .join(
            FoodConsumption,
            (FoodConsumption.id_breeding == AnimalWeights.id_breeding)
            & (FoodConsumption.date == AnimalWeights.date)
            & (FoodConsumption.animals_age == AnimalWeights.animals_age),
        )
        .outerjoin(BreedingData, BreedingData.id_breeding == AnimalWeights.id_breeding)
        .outerjoin(
            Mortality,
            (Mortality.id_breeding == AnimalWeights.id_breeding)
            & (Mortality.date_mortality == AnimalWeights.date),
        )
        .outerjoin(Breedings, Breedings.id_breeding == AnimalWeights.id_breeding)
        .filter(and_(Breedings.id_breeding.in_(id_breeding)))
    )


def upsert_animalshed_conversion(
    data: list[dict], constraint_name: str = "animal_conversion_unique"
) -> InsertMySQL:
    statement = pg_insert(AnimalConversion).values(data)

    update_dict = {
        c.name: getattr(statement.excluded, c.name)
        for c in statement.table.columns
        if not c.primary_key
    }

    statement = statement.on_conflict_do_update(constraint=constraint_name, set_=update_dict)

    return statement
