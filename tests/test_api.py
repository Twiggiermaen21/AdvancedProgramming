"""
Testy jednostkowe i integracyjne dla endpointów API oraz bazy SQLite.
"""

from pathlib import Path
import sys
import warnings

# Dodanie katalogu głównego projektu do sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import SessionLocal  # noqa: E402
from main import app  # noqa: E402
from models import Link, Movie, Rating, Tag  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

# Wyciszenie ostrzeżeń deprecation podczas testów
warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_read_root() -> None:
    """
    Test weryfikujący odpowiedź endpointu głównego GET /.
    """
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"hello": "world"}


def test_read_hello() -> None:
    """
    Test weryfikujący odpowiedź endpointu pomocniczego GET /hello.
    """
    with TestClient(app) as client:
        response = client.get("/hello")
        assert response.status_code == 200
        assert response.json() == {"hello": "world"}


def test_read_movies_limit() -> None:
    """
    Test weryfikujący pobieranie listy filmów z parametrem limit.
    """
    with TestClient(app) as client:
        response = client.get("/movies?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert set(data[0].keys()) == {"movieId", "title", "genres"}


def test_read_links_limit() -> None:
    """
    Test weryfikujący pobieranie listy odnośników z parametrem limit.
    """
    with TestClient(app) as client:
        response = client.get("/links?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert set(data[0].keys()) == {"movieId", "imdbId", "tmdbId"}


def test_read_ratings_limit() -> None:
    """
    Test weryfikujący pobieranie listy ocen z parametrem limit.
    """
    with TestClient(app) as client:
        response = client.get("/ratings?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert set(data[0].keys()) == {
            "userId",
            "movieId",
            "rating",
            "timestamp",
        }


def test_read_tags_limit() -> None:
    """
    Test weryfikujący pobieranie listy tagów z parametrem limit.
    """
    with TestClient(app) as client:
        response = client.get("/tags?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert set(data[0].keys()) == {"userId", "movieId", "tag", "timestamp"}


def test_database_counts() -> None:
    """
    Test weryfikujący poprawność liczby rekordów w bazie danych SQLite.
    """
    with SessionLocal() as db:
        assert db.query(Movie).count() == 9742
        assert db.query(Link).count() == 9742
        assert db.query(Rating).count() == 100836
        assert db.query(Tag).count() == 3683


def test_models_to_dict() -> None:
    """
    Test weryfikujący metodę serializacji to_dict dla modeli.
    """
    movie = Movie(movie_id=1, title="Toy Story", genres="Animation")
    assert movie.to_dict() == {
        "movieId": 1,
        "title": "Toy Story",
        "genres": "Animation",
    }
