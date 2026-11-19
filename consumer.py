"""
Moduł consumer.py - pobieranie i obsługa zadań z kolejki RabbitMQ.
Działa w pętli (while True), co 5s sprawdza obecność zadań.
Po napotkaniu zadania konsumuje je, zmienia status na 'in_progress',
symuluje wykonywanie pracy przez 30s i zatwierdza status jako 'done'.
"""

import argparse
import json
import os
import time
from queue_manager import (
    QUEUE_NAME,
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    STATUS_DONE,
    STATUS_IN_PROGRESS,
    get_connection,
    setup_queue,
)


def parse_arguments() -> argparse.Namespace:
    """
    Parsuje parametry wiersza poleceń dla konsumenta.
    """
    default_id = f"Konsument-{os.getpid()}"
    parser = argparse.ArgumentParser(
        description="Consumer - wykonywanie zadań z kolejki RabbitMQ."
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
        help="Czas trwania zadania w sekundach (domyślnie 30s).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Interwał sprawdzania kolejki w sekundach (domyślnie 5s).",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=RABBITMQ_HOST,
        help="Adres hosta RabbitMQ.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=RABBITMQ_PORT,
        help="Port AMQP RabbitMQ (domyślnie 8081).",
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
    host: str = RABBITMQ_HOST,
    port: int = RABBITMQ_PORT,
    run_once: bool = False,
) -> None:
    """
    Główna pętla konsumenta odpytująca RabbitMQ co określony interwał.
    """
    connection = get_connection(host=host, port=port)
    channel = connection.channel()
    setup_queue(channel)
    channel.basic_qos(prefetch_count=1)

    print(
        f"[{worker_id}] Konsument uruchomiony (RabbitMQ: {host}:{port}).\n"
        f"[{worker_id}] Czas obsługi: {duration}s, interwał: {interval}s."
    )

    try:
        while True:
            method_frame, header_frame, body = channel.basic_get(
                queue=QUEUE_NAME, auto_ack=False
            )

            if method_frame:
                task = json.loads(body.decode("utf-8"))
                task_id = task.get("id")
                topic = task.get("topic", "Brak tematu")
                phone = task.get("client_phone", "Brak numeru")

                task["status"] = STATUS_IN_PROGRESS
                task["worker_id"] = worker_id

                print(
                    f"\n[{worker_id}] POBRANO ZADANIE ID: {task_id} "
                    f"| {topic} ({phone})"
                )
                print(
                    f"[{worker_id}] Status zmieniony na '{task['status']}'. "
                    f"Obsługa rozmowy przez {duration}s..."
                )

                time.sleep(duration)

                task["status"] = STATUS_DONE
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                print(
                    f"[{worker_id}] ZAKOŃCZONO ZADANIE ID: {task_id}. "
                    f"Status zmieniony na '{task['status']}'."
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
        print(f"\n[{worker_id}] Konsument zatrzymany przez użytkownika.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    args = parse_arguments()
    run_consumer(
        worker_id=args.id,
        duration=args.duration,
        interval=args.interval,
        host=args.host,
        port=args.port,
        run_once=args.once,
    )
