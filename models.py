"""
Modele danych reprezentujące rekordy z plików CSV.
"""


class Movie:
    """
    Model danych reprezentujący film z pliku movies.csv.
    """

    def __init__(self, movie_id: int, title: str, genres: str) -> None:
        self.movieId: int = movie_id
        self.title: str = title
        self.genres: str = genres


class Link:
    """
    Model danych reprezentujący odnośniki z pliku links.csv.
    """

    def __init__(
        self, movie_id: int, imdb_id: str, tmdb_id: str
    ) -> None:
        self.movieId: int = movie_id
        self.imdbId: str = imdb_id
        self.tmdbId: str = tmdb_id


class Rating:
    """
    Model danych reprezentujący ocenę z pliku ratings.csv.
    """

    def __init__(
        self, user_id: int, movie_id: int, rating: float, timestamp: int
    ) -> None:
        self.userId: int = user_id
        self.movieId: int = movie_id
        self.rating: float = rating
        self.timestamp: int = timestamp


class Tag:
    """
    Model danych reprezentujący tag z pliku tags.csv.
    """

    def __init__(
        self, user_id: int, movie_id: int, tag: str, timestamp: int
    ) -> None:
        self.userId: int = user_id
        self.movieId: int = movie_id
        self.tag: str = tag
        self.timestamp: int = timestamp
