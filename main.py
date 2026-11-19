"""
Główny moduł demonstracyjny i monitorujący system kolejkowy RabbitMQ.
Umożliwia:
- sprawdzenie statystyk kolejki w RabbitMQ (liczba wiadomości i konsumentów),
- dodanie 100 zadań za pośrednictwem producera,
- uruchomienie wielu konsumentów w osobnych procesach.
"""

import argparse
import subprocess
import sys
import time
from queue_manager import (
    QUEUE_NAME,
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    get_queue_stats,
    send_task,
)


def display_stats() -> None:
    """
    Wyświetla bieżący stan zadań w kolejce RabbitMQ.
    """
    try:
        stats = get_queue_stats()
        print("=" * 45)
        print("        STATUS KOLEJKI ZADAŃ (RABBITMQ)      ")
        print("=" * 45)
        print(f" Nazwa kolejki:         {QUEUE_NAME}")
        print(f" Broker AMQP:           {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        print(f" Oczekujące wiadomości: {stats['message_count']}")
        print(f" Aktywni konsumenci:    {stats['consumer_count']}")
        print(f" Panel Management UI:   http://localhost:8080")
        print("=" * 45)
    except Exception as error:
        print(f"Błąd połączenia z RabbitMQ: {error}")


def populate_queue(count: int = 100) -> None:
    """
    Dodaje wskazaną liczbę zadań do kolejki RabbitMQ.
    """
    print(f"Dodawanie {count} zadań do kolejki '{QUEUE_NAME}' w RabbitMQ...")
    for i in range(1, count + 1):
        send_task(topic=f"Rozmowa telefoniczna z klientem #{i}", task_id=i)
    print(f"Pomyślnie wysłano {count} zadań o statusie 'pending'.")


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
        description="Skrypt pomocniczy do zarządzania kolejką RabbitMQ."
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
        help="Wyświetla bieżące statystyki kolejki w RabbitMQ.",
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
