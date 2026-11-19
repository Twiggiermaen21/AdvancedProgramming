"""
Moduł consumer.py - pobieranie i obsługa zadań z kolejki RabbitMQ.
Rejestruje subskrypcję w RabbitMQ (basic_consume), dzięki czemu broker
widzi aktywnych konsumentów (consumer_count).
Po otrzymaniu zadania zmienia status na 'in_progress', wykonuje pracę
przez 30s i zatwierdza status jako 'done'.
"""

import argparse
import json
import os
import time
from typing import Any
import pika
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
    host: str = RABBITMQ_HOST,
    port: int = RABBITMQ_PORT,
    run_once: bool = False,
) -> None:
    """
    Uruchamia subskrypcję konsumenta w RabbitMQ za pomocą basic_consume.
    """
    connection = get_connection(host=host, port=port)
    channel = connection.channel()
    setup_queue(channel)

    # Gwarantuje sprawiedliwy podział pracy (1 zadanie naraz na konsumenta)
    channel.basic_qos(prefetch_count=1)

    def on_message_callback(
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> None:
        task: dict[str, Any] = json.loads(body.decode("utf-8"))
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
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(
            f"[{worker_id}] ZAKOŃCZONO ZADANIE ID: {task_id}. "
            f"Status zmieniony na '{task['status']}'."
        )

        if run_once:
            print(f"[{worker_id}] Zakończono tryb pojedynczy (--once).")
            ch.stop_consuming()

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=on_message_callback,
    )

    print(
        f"[{worker_id}] Konsument zarejestrowany w RabbitMQ ({host}:{port}).\n"
        f"[{worker_id}] Czas obsługi każdego zadania: {duration}s.\n"
        f"[{worker_id}] Oczekiwanie na zadania (naciśnij Ctrl+C, aby wyjść)..."
    )

    try:
        channel.start_consuming()
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
        host=args.host,
        port=args.port,
        run_once=args.once,
    )
