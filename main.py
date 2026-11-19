"""
Główny moduł demonstracyjny i monitorujący system kolejkowy SQLite.
Umożliwia:
- sprawdzenie statystyk kolejki (pending, in_progress, done),
- dodanie 100 zadań za pośrednictwem producera,
- uruchomienie wielu konsumentów w osobnych procesach.
"""

import argparse
import subprocess
import sys
import time
from queue_manager import (
    DB_FILE,
    STATUS_DONE,
    STATUS_IN_PROGRESS,
    STATUS_PENDING,
    add_task,
    get_queue_stats,
    init_db,
)


def display_stats() -> None:
    """
    Wyświetla bieżący stan zadań w bazie SQLite.
    """
    init_db()
    stats = get_queue_stats()

    print("=" * 45)
    print("         STATUS KOLEJKI ZADAŃ (SQLITE)       ")
    print("=" * 45)
    print(f" Łączna liczba zadań:   {stats['total']}")
    print(f" Oczekujące (pending):  {stats[STATUS_PENDING]}")
    print(f" W toku (in_progress):  {stats[STATUS_IN_PROGRESS]}")
    print(f" Ukończone (done):      {stats[STATUS_DONE]}")
    print("=" * 45)


def populate_queue(count: int = 100) -> None:
    """
    Dodaje wskazaną liczbę zadań do bazy danych.
    """
    print(f"Dodawanie {count} zadań do bazy {DB_FILE}...")
    for i in range(1, count + 1):
        add_task(topic=f"Rozmowa telefoniczna z klientem #{i}")
    print(f"Pomyślnie dodano {count} zadań o statusie 'pending'.")


def run_multiple_consumers(
    consumers_count: int = 3, duration: float = 30.0
) -> None:
    """
    Uruchamia wskazaną liczbę procesów konsumentów.
    """
    processes = []
    print(
        f"Uruchamianie {consumers_count} konsumentów "
        f"(czas zadania: {duration}s)..."
    )

    try:
        for i in range(1, consumers_count + 1):
            worker_id = f"Konsument-{i}"
            cmd = [
                sys.executable,
                "consumer.py",
                "--id",
                worker_id,
                "--duration",
                str(duration),
            ]
            proc = subprocess.Popen(cmd)
            processes.append(proc)
            time.sleep(0.2)

        print(
            f"Wszyscy konsumenci ({consumers_count}) zostali uruchomieni. "
            f"Naciśnij Ctrl+C, aby zatrzymać."
        )

        while True:
            time.sleep(5)
            display_stats()
    except KeyboardInterrupt:
        print("\nZatrzymywanie konsumentów...")
        for proc in processes:
            proc.terminate()
        for proc in processes:
            proc.wait()
        print("Wszystkie procesy konsumentów zostały zatrzymane.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Skrypt pomocniczy do zarządzania kolejką SQLite."
    )
    parser.add_argument(
        "--populate",
        type=int,
        metavar="N",
        help="Dodaje N zadań do kolejki (np. --populate 100).",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Wyświetla bieżące statystyki kolejki.",
    )
    parser.add_argument(
        "--start-consumers",
        type=int,
        metavar="K",
        help="Uruchamia K konsumentów w tle (np. --start-consumers 3).",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Czas trwania zadania dla konsumentów (domyślnie 30s).",
    )
    args = parser.parse_args()

    if args.populate:
        populate_queue(args.populate)
        display_stats()
    elif args.start_consumers:
        run_multiple_consumers(
            consumers_count=args.start_consumers, duration=args.duration
        )
    else:
        display_stats()


if __name__ == "__main__":
    main()
