"""
Aplikacja FastAPI udostępniająca endpointy z danymi filmowymi.
"""

import csv
import os
from typing import Any, Optional
from fastapi import FastAPI
from models import Link, Movie, Rating, Tag

app = FastAPI(title="Movie API")

DATA_DIR: str = os.path.join(os.path.dirname(__file__), "data")


def load_movies(file_path: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Wczytuje filmy z pliku movies.csv, tworzy obiekty Movie
    i serializuje je przy użyciu metody magicznej __dict__.
    """
    path = file_path or os.path.join(DATA_DIR, "movies.csv")
    movies_list: list[dict[str, Any]] = []

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = Movie(
                movie_id=int(row["movieId"]),
                title=row["title"],
                genres=row["genres"],
            )
            movies_list.append(movie.__dict__)

    return movies_list


def load_links(file_path: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Wczytuje odnośniki z pliku links.csv, tworzy obiekty Link
    i serializuje je przy użyciu metody magicznej __dict__.
    """
    path = file_path or os.path.join(DATA_DIR, "links.csv")
    links_list: list[dict[str, Any]] = []

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            link = Link(
                movie_id=int(row["movieId"]),
                imdb_id=row["imdbId"],
                tmdb_id=row["tmdbId"],
            )
            links_list.append(link.__dict__)

    return links_list


def load_ratings(file_path: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Wczytuje oceny z pliku ratings.csv, tworzy obiekty Rating
    i serializuje je przy użyciu metody magicznej __dict__.
    """
    path = file_path or os.path.join(DATA_DIR, "ratings.csv")
    ratings_list: list[dict[str, Any]] = []

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rating = Rating(
                user_id=int(row["userId"]),
                movie_id=int(row["movieId"]),
                rating=float(row["rating"]),
                timestamp=int(row["timestamp"]),
            )
            ratings_list.append(rating.__dict__)

    return ratings_list


def load_tags(file_path: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Wczytuje tagi z pliku tags.csv, tworzy obiekty Tag
    i serializuje je przy użyciu metody magicznej __dict__.
    """
    path = file_path or os.path.join(DATA_DIR, "tags.csv")
    tags_list: list[dict[str, Any]] = []

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tag = Tag(
                user_id=int(row["userId"]),
                movie_id=int(row["movieId"]),
                tag=row["tag"],
                timestamp=int(row["timestamp"]),
            )
            tags_list.append(tag.__dict__)

    return tags_list


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
def read_movies(limit: Optional[int] = None) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę filmów zserializowanych przez __dict__.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    movies = load_movies()
    if limit is not None:
        return movies[:limit]
    return movies


@app.get("/links")
def read_links(limit: Optional[int] = None) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę odnośników zserializowanych przez __dict__.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    links = load_links()
    if limit is not None:
        return links[:limit]
    return links


@app.get("/ratings")
def read_ratings(limit: Optional[int] = None) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę ocen zserializowanych przez __dict__.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    ratings = load_ratings()
    if limit is not None:
        return ratings[:limit]
    return ratings


@app.get("/tags")
def read_tags(limit: Optional[int] = None) -> list[dict[str, Any]]:
    """
    Endpoint zwracający listę tagów zserializowanych przez __dict__.
    Opcjonalny parametr 'limit' pozwala ograniczyć liczbę wyników.
    """
    tags = load_tags()
    if limit is not None:
        return tags[:limit]
    return tags


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
