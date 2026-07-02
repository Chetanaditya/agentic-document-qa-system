from sqlalchemy.orm import Session

from auth.models import User
from auth.schemas import RegisterRequest
from auth.security import hash_password


def register_user(
    db: Session,
    user_data: RegisterRequest
) -> User:
    """
    Register a new user.
    """

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise ValueError(
            "Email is already registered."
        )

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user