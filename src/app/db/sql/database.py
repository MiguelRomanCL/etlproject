# Standard Library
from contextlib import contextmanager
from typing import AsyncGenerator, Generator

# External
from fastapi import HTTPException, Request, status
from sqlmodel import Session, create_engine

# Project
from app.config import (
    POSTGRES_DATABASE,
    POSTGRES_PASSWORD,
    POSTGRES_SERVER,
    POSTGRES_USER,
    PROJECT_NAME,
)


DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DATABASE}?application_name={PROJECT_NAME}"
engine = create_engine(DATABASE_URL, echo=True)


@contextmanager
def get_session(tenant_schema: str) -> Generator[Session, None, None]:
    session = engine.execution_options(schema_translate_map={None: tenant_schema})

    try:
        session = Session(autocommit=False, autoflush=False, bind=session)
        yield session
    finally:
        session.close()


async def get_db(req: Request) -> AsyncGenerator[Session, None]:
    body = await req.json()
    if "client" not in body:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing keys in request body",
        )
    tenant = body["client"]
    with get_session(tenant) as db:
        yield db
