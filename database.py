"""
Konfiguracja połączenia z bazą danych SQLite przy użyciu SQLAlchemy.
"""

import os
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DB_FILE: str = os.path.join(BASE_DIR, "movies.db")
SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Generator sesji bazy danych dla FastAPI Depends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
