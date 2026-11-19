"""
Moduł zarządzania kolejką zadań z wykorzystaniem bazy danych SQLite.
Zapewnia atomowe transakcje i bezpieczeństwo wieloprocesowe.
"""

from datetime import datetime
import os
import random
import sqlite3
from typing import Any, Optional

DB_FILE: str = "queue.db"

STATUS_PENDING: str = "pending"
STATUS_IN_PROGRESS: str = "in_progress"
STATUS_DONE: str = "done"


def get_connection(db_path: str = DB_FILE) -> sqlite3.Connection:
    """
    Tworzy i konfiguruje połączenie z bazą SQLite.
    Włącza tryb WAL oraz timeout dla bezpiecznej pracy wieloprocesowej.
    """
    conn = sqlite3.connect(db_path, timeout=15.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_FILE) -> None:
    """
    Tworzy tabelę tasks oraz indeks po statusie, jeśli nie istnieją.
    """
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                client_phone TEXT NOT NULL,
                status TEXT NOT NULL CHECK(
                    status IN ('pending', 'in_progress', 'done')
                ),
                worker_id TEXT DEFAULT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);"
        )


def generate_phone_number() -> str:
    """
    Generuje losowy numer telefonu w polskim formacie.
    """
    prefix = random.choice(["501", "502", "503", "601", "602", "701", "888"])
    part1 = random.randint(100, 999)
    part2 = random.randint(100, 999)
    return f"+48 {prefix} {part1} {part2}"


def add_task(
    topic: str = "Konsultacja telefoniczna",
    db_path: str = DB_FILE,
) -> dict[str, Any]:
    """
    Dodaje 1 zadanie (rozmowę telefoniczną) o statusie 'pending'.
    """
    init_db(db_path)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    phone = generate_phone_number()

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO tasks (
                topic, client_phone, status, worker_id, created_at, updated_at
            )
            VALUES (?, ?, ?, NULL, ?, ?);
            """,
            (topic, phone, STATUS_PENDING, now_str, now_str),
        )
        task_id = cursor.lastrowid

    return {
        "id": task_id,
        "topic": topic,
        "client_phone": phone,
        "status": STATUS_PENDING,
        "worker_id": None,
        "created_at": now_str,
        "updated_at": now_str,
    }


def claim_next_pending_task(
    worker_id: str,
    db_path: str = DB_FILE,
) -> Optional[dict[str, Any]]:
    """
    Wyszukuje pierwsze zadanie 'pending' i atomowo zmienia status
    na 'in_progress' oraz przypisuje do konsumenta.
    """
    init_db(db_path)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection(db_path)

    try:
        conn.execute("BEGIN IMMEDIATE;")
        cursor = conn.execute(
            """
            SELECT id, topic, client_phone, status, created_at
            FROM tasks
            WHERE status = ?
            ORDER BY id ASC
            LIMIT 1;
            """,
            (STATUS_PENDING,),
        )
        row = cursor.fetchone()

        if row:
            task_id = row["id"]
            conn.execute(
                """
                UPDATE tasks
                SET status = ?, worker_id = ?, updated_at = ?
                WHERE id = ?;
                """,
                (STATUS_IN_PROGRESS, worker_id, now_str, task_id),
            )
            conn.commit()
            return {
                "id": task_id,
                "topic": row["topic"],
                "client_phone": row["client_phone"],
                "status": STATUS_IN_PROGRESS,
                "worker_id": worker_id,
                "created_at": row["created_at"],
                "updated_at": now_str,
            }

        conn.commit()
        return None
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def mark_task_done(
    task_id: int | str,
    worker_id: str,
    db_path: str = DB_FILE,
) -> bool:
    """
    Zmienia status zadania na 'done'.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            UPDATE tasks
            SET status = ?, worker_id = ?, updated_at = ?
            WHERE id = ?;
            """,
            (STATUS_DONE, worker_id, now_str, int(task_id)),
        )
        return cursor.rowcount > 0


def get_queue_stats(db_path: str = DB_FILE) -> dict[str, int]:
    """
    Zwraca zliczenia zadań według statusu w bazie danych.
    """
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT status, COUNT(*) AS count
            FROM tasks
            GROUP BY status;
            """
        )
        rows = cursor.fetchall()

    stats = {
        STATUS_PENDING: 0,
        STATUS_IN_PROGRESS: 0,
        STATUS_DONE: 0,
    }
    for row in rows:
        stats[row["status"]] = row["count"]

    stats["total"] = sum(stats.values())
    return stats
