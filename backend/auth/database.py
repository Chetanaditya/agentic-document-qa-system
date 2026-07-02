from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

#SQLlite Database
DATABASE_URL = "sqlite:///./users.db"

#SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#SessionFactory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#Base Class for all models 

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()