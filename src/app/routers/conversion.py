from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlmodel import Session

# Project
from app.db import get_db
from app.services import get_conversion

conversion_router = APIRouter(prefix="/conversion", tags=["Conversion"])


@conversion_router.post("", status_code=status.HTTP_200_OK)
def calculate_conversion(
    payload: dict = Body(..., example={"client": "tecnoandina"}),
    session: Session = Depends(get_db),
) -> list[dict]:
    try:
        result = get_conversion(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
