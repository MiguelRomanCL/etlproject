from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError, SQLAlchemyError
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
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}",
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Data validation error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
