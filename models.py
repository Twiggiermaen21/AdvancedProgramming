"""
Modele danych SQLAlchemy reprezentujące tabele w bazie SQLite.
"""

from typing import Any, Optional
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Bazowa klasa dla modeli SQLAlchemy z metodą serializacji do słownika.
    """

    def to_dict(self) -> dict[str, Any]:
        """
        Serializuje obiekt modelu do postaci słownika,
        pomijając techniczny klucz 'id'.
        """
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name != "id"
        }

    def as_dict(self) -> dict[str, Any]:
        """
        Alias dla metody to_dict().
        """
        return self.to_dict()


class Movie(Base):
    """
    Model SQLAlchemy reprezentujący tabelę movies.
    """

    __tablename__ = "movies"

    movieId: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    genres: Mapped[str] = mapped_column(String(255), nullable=False)

    def __init__(
        self,
        movie_id: Optional[int] = None,
        title: Optional[str] = None,
        genres: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if movie_id is not None:
            kwargs["movieId"] = movie_id
        if title is not None:
            kwargs["title"] = title
        if genres is not None:
            kwargs["genres"] = genres
        super().__init__(**kwargs)


class Link(Base):
    """
    Model SQLAlchemy reprezentujący tabelę links.
    """

    __tablename__ = "links"

    movieId: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.movieId"), primary_key=True
    )
    imdbId: Mapped[str] = mapped_column(String(20), nullable=False)
    tmdbId: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    def __init__(
        self,
        movie_id: Optional[int] = None,
        imdb_id: Optional[str] = None,
        tmdb_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if movie_id is not None:
            kwargs["movieId"] = movie_id
        if imdb_id is not None:
            kwargs["imdbId"] = imdb_id
        if tmdb_id is not None:
            kwargs["tmdbId"] = tmdb_id
        super().__init__(**kwargs)


class Rating(Base):
    """
    Model SQLAlchemy reprezentujący tabelę ratings.
    """

    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    userId: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    movieId: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.movieId"), nullable=False, index=True
    )
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(
        self,
        user_id: Optional[int] = None,
        movie_id: Optional[int] = None,
        rating: Optional[float] = None,
        timestamp: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        if user_id is not None:
            kwargs["userId"] = user_id
        if movie_id is not None:
            kwargs["movieId"] = movie_id
        if rating is not None:
            kwargs["rating"] = rating
        if timestamp is not None:
            kwargs["timestamp"] = timestamp
        super().__init__(**kwargs)


class Tag(Base):
    """
    Model SQLAlchemy reprezentujący tabelę tags.
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    userId: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    movieId: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.movieId"), nullable=False, index=True
    )
    tag: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(
        self,
        user_id: Optional[int] = None,
        movie_id: Optional[int] = None,
        tag: Optional[str] = None,
        timestamp: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        if user_id is not None:
            kwargs["userId"] = user_id
        if movie_id is not None:
            kwargs["movieId"] = movie_id
        if tag is not None:
            kwargs["tag"] = tag
        if timestamp is not None:
            kwargs["timestamp"] = timestamp
        super().__init__(**kwargs)
