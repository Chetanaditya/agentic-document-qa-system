from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.database import Base, engine, get_db
from auth.schemas import RegisterRequest, RegisterResponse
from auth.service import register_user

# Create database tables
Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201
)
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):

    try:

        created_user = register_user(
            db=db,
            user_data=user
        )

        return created_user

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )