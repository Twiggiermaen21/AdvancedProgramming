"""
Moduł zarządzania kolejką zadań w pliku CSV oraz blokadą wieloprocesową.
"""

from contextlib import contextmanager
import csv
from datetime import datetime
import os
import random
import time
from typing import Any, Optional

QUEUE_FILE: str = "queue.csv"
LOCK_FILE: str = "queue.lock"
FIELDNAMES: list[str] = [
    "id",
    "topic",
    "client_phone",
    "status",
    "worker_id",
    "created_at",
    "updated_at",
]

STATUS_PENDING: str = "pending"
STATUS_IN_PROGRESS: str = "in_progress"
STATUS_DONE: str = "done"


@contextmanager
def file_lock(lock_path: str = LOCK_FILE, timeout: float = 10.0):
    """
    Zapewnia atomową blokadę pliku dla wielu procesów (Windows i Linux).
    """
    start_time = time.time()
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            break
        except FileExistsError:
            if time.time() - start_time > timeout:
                try:
                    if os.path.exists(lock_path):
                        age = time.time() - os.path.getmtime(lock_path)
                        if age > timeout:
                            os.remove(lock_path)
                            continue
                except OSError:
                    pass
                raise TimeoutError("Przekroczono czas oczekiwania na blokadę.")
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            if os.path.exists(lock_path):
                os.remove(lock_path)
        except OSError:
            pass


def init_queue_file(file_path: str = QUEUE_FILE) -> None:
    """
    Inicjalizuje plik kolejki nagłówkiem, jeśli plik jeszcze nie istnieje.
    """
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_all_tasks(file_path: str = QUEUE_FILE) -> list[dict[str, str]]:
    """
    Odczytuje wszystkie wiersze z pliku kolejki.
    """
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_all_tasks(
    tasks: list[dict[str, str]], file_path: str = QUEUE_FILE
) -> None:
    """
    Zapisuje listę zadań do pliku (zapis atomowy przez plik tymczasowy).
    """
    temp_path = f"{file_path}.tmp"
    with open(temp_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(tasks)
    os.replace(temp_path, file_path)


def generate_phone_number() -> str:
    """
    Generuje losowy numer telefonu w formacie polskim.
    """
    prefix = random.choice(["501", "502", "503", "601", "602", "701", "888"])
    part1 = random.randint(100, 999)
    part2 = random.randint(100, 999)
    return f"+48 {prefix} {part1} {part2}"


def add_task(
    topic: str = "Konsultacja telefoniczna",
    file_path: str = QUEUE_FILE,
    lock_path: str = LOCK_FILE,
) -> dict[str, str]:
    """
    Dodaje 1 zadanie (rozmowę) do kolejki o statusie 'pending'.
    """
    with file_lock(lock_path):
        init_queue_file(file_path)
        tasks = read_all_tasks(file_path)
        next_id = len(tasks) + 1
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_task = {
            "id": str(next_id),
            "topic": topic,
            "client_phone": generate_phone_number(),
            "status": STATUS_PENDING,
            "worker_id": "",
            "created_at": now_str,
            "updated_at": now_str,
        }
        tasks.append(new_task)
        write_all_tasks(tasks, file_path)
        return new_task


def claim_next_pending_task(
    worker_id: str,
    file_path: str = QUEUE_FILE,
    lock_path: str = LOCK_FILE,
) -> Optional[dict[str, str]]:
    """
    Wyszukuje pierwsze zadanie 'pending', zmienia jego status na 'in_progress',
    przypisuje identyfikator pracownika i zapisuje plik.
    """
    with file_lock(lock_path):
        init_queue_file(file_path)
        tasks = read_all_tasks(file_path)

        for task in tasks:
            if task.get("status") == STATUS_PENDING:
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                task["status"] = STATUS_IN_PROGRESS
                task["worker_id"] = worker_id
                task["updated_at"] = now_str
                write_all_tasks(tasks, file_path)
                return task
        return None


def mark_task_done(
    task_id: str,
    worker_id: str,
    file_path: str = QUEUE_FILE,
    lock_path: str = LOCK_FILE,
) -> bool:
    """
    Zmienia status wskazanego zadania na 'done'.
    """
    with file_lock(lock_path):
        tasks = read_all_tasks(file_path)
        found = False
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for task in tasks:
            if task.get("id") == str(task_id):
                task["status"] = STATUS_DONE
                task["worker_id"] = worker_id
                task["updated_at"] = now_str
                found = True
                break

        if found:
            write_all_tasks(tasks, file_path)
        return found
