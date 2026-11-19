"""
Skrypt ładujący dane z plików CSV do bazy danych SQLite przy użyciu SQLAlchemy.
"""

import argparse
import csv
import os
from typing import Optional
from sqlalchemy import insert
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Link, Movie, Rating, Tag

DATA_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def create_tables() -> None:
    """
    Tworzy tabele w bazie danych zgodnie ze zdefiniowanymi modelami.
    """
    Base.metadata.create_all(bind=engine)


def load_movies_to_db(
    session: Session, file_path: str, chunk_size: int = 5000
) -> int:
    """
    Wczytuje filmy z pliku CSV i zapisuje w tabeli movies.
    """
    records: list[dict[str, object]] = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(
                {
                    "movieId": int(row["movieId"]),
                    "title": row["title"],
                    "genres": row["genres"],
                }
            )

    for i in range(0, len(records), chunk_size):
        session.execute(insert(Movie), records[i:i + chunk_size])
    session.commit()
    return len(records)


def load_links_to_db(
    session: Session, file_path: str, chunk_size: int = 5000
) -> int:
    """
    Wczytuje odnośniki z pliku CSV i zapisuje w tabeli links.
    """
    records: list[dict[str, object]] = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tmdb_val = row["tmdbId"].strip() if row["tmdbId"] else None
            records.append(
                {
                    "movieId": int(row["movieId"]),
                    "imdbId": row["imdbId"],
                    "tmdbId": tmdb_val if tmdb_val else None,
                }
            )

    for i in range(0, len(records), chunk_size):
        session.execute(insert(Link), records[i:i + chunk_size])
    session.commit()
    return len(records)


def load_ratings_to_db(
    session: Session, file_path: str, chunk_size: int = 10000
) -> int:
    """
    Wczytuje oceny z pliku CSV i zapisuje w tabeli ratings.
    """
    records: list[dict[str, object]] = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(
                {
                    "userId": int(row["userId"]),
                    "movieId": int(row["movieId"]),
                    "rating": float(row["rating"]),
                    "timestamp": int(row["timestamp"]),
                }
            )

    for i in range(0, len(records), chunk_size):
        session.execute(insert(Rating), records[i:i + chunk_size])
    session.commit()
    return len(records)


def load_tags_to_db(
    session: Session, file_path: str, chunk_size: int = 5000
) -> int:
    """
    Wczytuje tagi z pliku CSV i zapisuje w tabeli tags.
    """
    records: list[dict[str, object]] = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(
                {
                    "userId": int(row["userId"]),
                    "movieId": int(row["movieId"]),
                    "tag": row["tag"],
                    "timestamp": int(row["timestamp"]),
                }
            )

    for i in range(0, len(records), chunk_size):
        session.execute(insert(Tag), records[i:i + chunk_size])
    session.commit()
    return len(records)


def load_all_data(
    data_dir: Optional[str] = None, force: bool = False
) -> None:
    """
    Tworzy tabele i ładuje wszystkie dane z plików CSV do bazy danych SQLite.
    Jeśli dane już istnieją i force=False, pomija ładowanie.
    """
    target_dir = data_dir or DATA_DIR

    if force:
        print("Usuwanie istniejących tabel (force=True)...")
        Base.metadata.drop_all(bind=engine)

    create_tables()

    with SessionLocal() as session:
        has_movies = session.query(Movie).first() is not None
        if has_movies and not force:
            print("Baza danych zawiera już dane. Pomijanie ładowania.")
            return

        print("Rozpoczynanie ładowania danych do bazy SQLite...")

        movies_csv = os.path.join(target_dir, "movies.csv")
        links_csv = os.path.join(target_dir, "links.csv")
        ratings_csv = os.path.join(target_dir, "ratings.csv")
        tags_csv = os.path.join(target_dir, "tags.csv")

        count_movies = load_movies_to_db(session, movies_csv)
        print(f"Załadowano {count_movies} rekordów do tabeli movies.")

        count_links = load_links_to_db(session, links_csv)
        print(f"Załadowano {count_links} rekordów do tabeli links.")

        count_ratings = load_ratings_to_db(session, ratings_csv)
        print(f"Załadowano {count_ratings} rekordów do tabeli ratings.")

        count_tags = load_tags_to_db(session, tags_csv)
        print(f"Załadowano {count_tags} rekordów do tabeli tags.")

        print("Pomyślnie załadowano wszystkie dane do bazy SQLite!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ładowanie danych z CSV do SQLite"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Wymuś przebudowanie tabel i ponowne załadowanie danych",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Ścieżka do katalogu z plikami CSV",
    )
    args = parser.parse_args()

    load_all_data(data_dir=args.data_dir, force=args.force)
