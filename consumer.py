"""
Moduł consumer.py - pobieranie i wykonywanie zadań z pliku kolejki.
Działa w nieskończonej pętli (while True), co 5s sprawdza plik.
Po pobraniu zadania zmienia status na 'in_progress',
wykonuje pracę przez 30s i zmienia status na 'done'.
"""

import argparse
import os
import time
from queue_manager import (
    claim_next_pending_task,
    init_queue_file,
    mark_task_done,
)


def parse_arguments() -> argparse.Namespace:
    """
    Parsuje parametry wiersza poleceń dla consumera.
    """
    default_id = f"Konsument-{os.getpid()}"
    parser = argparse.ArgumentParser(
        description="Consumer - wykonywanie zadań z kolejki plikowej."
    )
    parser.add_argument(
        "--id",
        type=str,
        default=default_id,
        help="Unikalny identyfikator konsumenta/operatora.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Czas trwania wykonywania zadania w sekundach (domyślnie 30s).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Interwał sprawdzania kolejki w sekundach (domyślnie 5s).",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Zakończ działanie po 1 zadaniu (użyteczne w testach).",
    )
    return parser.parse_args()


def run_consumer(
    worker_id: str,
    duration: float = 30.0,
    interval: float = 5.0,
    run_once: bool = False,
) -> None:
    """
    Główna pętla konsumenta.
    """
    init_queue_file()
    print(
        f"[{worker_id}] Konsument uruchomiony. "
        f"Czas pracy: {duration}s, interwał sprawdzania: {interval}s."
    )

    try:
        while True:
            task = claim_next_pending_task(worker_id=worker_id)

            if task:
                task_id = task["id"]
                topic = task.get("topic", "Brak tematu")
                phone = task.get("client_phone", "Brak numeru")

                print(
                    f"\n[{worker_id}] POBRANO ZADANIE ID: {task_id} "
                    f"| {topic} ({phone})"
                )
                print(
                    f"[{worker_id}] Status zmieniony na 'in_progress'. "
                    f"Obsługa rozmowy przez {duration}s..."
                )

                time.sleep(duration)

                mark_task_done(task_id=task_id, worker_id=worker_id)
                print(
                    f"[{worker_id}] ZAKOŃCZONO ZADANIE ID: {task_id}. "
                    f"Status zmieniony na 'done'."
                )

                if run_once:
                    print(
                        f"[{worker_id}] Zakończono tryb pojedynczy (--once)."
                    )
                    break
            else:
                print(
                    f"[{worker_id}] Brak oczekujących zadań (pending). "
                    f"Kolejne sprawdzenie za {interval}s..."
                )
                if run_once:
                    break
                time.sleep(interval)
    except KeyboardInterrupt:
        print(
            f"\n[{worker_id}] Konsument zatrzymany przez użytkownika."
        )


if __name__ == "__main__":
    args = parse_arguments()
    run_consumer(
        worker_id=args.id,
        duration=args.duration,
        interval=args.interval,
        run_once=args.once,
    )
