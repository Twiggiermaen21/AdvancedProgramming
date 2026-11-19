"""
Aplikacja FastAPI udostępniająca endpointy z danymi filmowymi z bazy SQLite.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Optional
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from load_data import load_all_data
from models import Link, Movie, Rating, Tag


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Kontekst cyklu życia aplikacji: upewnia się, że tabele istnieją
    i ładuje dane początkowe z plików CSV, jeśli baza jest pusta.
    """
    load_all_data()
    yield


app = FastAPI(title="Movie API with SQLite", lifespan=lifespan)


def load_movies(
    db: Optional[Session] = None, limit: Optional[int] = None
) -> list[dict[str, Any]]:
    """
    Pobiera filmy z bazy SQLite przy użyciu SQLAlchemy
    i serializuje je do postaci słowników.
    """
    if db is not None:
        query = db.query(Movie)
        if limit is not None:
            query = query.limit(limit)
        return [movie.to_dict() for movie in query.all()]

    with SessionLocal() as session:
        query = session.query(Movie)
        if limit is not None:
            query = query.limit(limit)
        return [movie.to_dict() for movie in query.all()]


def load_links(
    db: Optional[Session] = None, limit: Optional[int] = None
) -> list[dict[str, Any]]:
    """
    Pobiera odnośniki z bazy SQLite przy użyciu SQLAlchemy
    i serializuje je do postaci słowników.
    """
    if db is not None:
        query = db.query(Link)
        if limit is not None:
            query = query.limit(limit)
        return [link.to_dict() for link in query.all()]

    with SessionLocal() as session:
        query = session.query(Link)
        if limit is not None:
            query = query.limit(limit)
        return [link.to_dict() for link in query.all()]


def load_ratings(
    db: Optional[Session] = None, limit: Optional[int] = None
) -> list[dict[str, Any]]:
    """
    Pobiera oceny z bazy SQLite przy użyciu SQLAlchemy
    i serializuje je do postaci słowników.
    """
    if db is not None:
        query = db.query(Rating)
        if limit is not None:
            query = query.limit(limit)
        return [rating.to_dict() for rating in query.all()]

    with SessionLocal() as session:
        query = session.query(Rating)
        if limit is not None:
            query = query.limit(limit)
        return [rating.to_dict() for rating in query.all()]


def load_tags(
    db: Optional[Session] = None, limit: Optional[int] = None
) -> list[dict[str, Any]]:
    """
    Pobiera tagi z bazy SQLite przy użyciu SQLAlchemy
    i serializuje je do postaci słowników.
    """
    if db is not None:
        query = db.query(Tag)
        if limit is not None:
            query = query.limit(limit)
        return [tag.to_dict() for tag in query.all()]

    with SessionLocal() as session:
        query = session.query(Tag)
        if limit is not None:
            query = query.limit(limit)
        return [tag.to_dict() for tag in query.all()]


@app.get("/")
def read_root() -> dict[str, str]:
    """
    Endpoint główny zwracający {'hello': 'world'}.
    """
    return {"hello": "world"}


@app.get("/hello")
def read_hello() -> dict[str, str]:
    """
    Endpoint pomocniczy /hello zwracający {'hello': 'world'}.
    """
    return {"hello": "world"}


@app.get("/movies")
def read_movies(
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę filmów pobranych z bazy SQLite.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    return load_movies(db=db, limit=limit)


@app.get("/links")
def read_links(
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę odnośników pobranych z bazy SQLite.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    return load_links(db=db, limit=limit)


@app.get("/ratings")
def read_ratings(
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę ocen pobranych z bazy SQLite.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    return load_ratings(db=db, limit=limit)


@app.get("/tags")
def read_tags(
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę tagów pobranych z bazy SQLite.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    return load_tags(db=db, limit=limit)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
