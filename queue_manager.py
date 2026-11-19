"""
Moduł zarządzania kolejką zadań w RabbitMQ.
Udostępnia funkcje pomocnicze dla producenta oraz konsumenta.
"""

from datetime import datetime
import json
import random
import time
from typing import Any, Optional
import pika

RABBITMQ_HOST: str = "localhost"
RABBITMQ_PORT: int = 8081
QUEUE_NAME: str = "calls_queue"

STATUS_PENDING: str = "pending"
STATUS_IN_PROGRESS: str = "in_progress"
STATUS_DONE: str = "done"


def get_connection(
    host: str = RABBITMQ_HOST,
    port: int = RABBITMQ_PORT,
    heartbeat: int = 0,
) -> pika.BlockingConnection:
    """
    Tworzy połączenie z serwerem RabbitMQ z wyłączonym lub wydłużonym
    heartbeatem, aby zapobiec rozłączeniu podczas długich zadań (30s).
    """
    params = pika.ConnectionParameters(
        host=host,
        port=port,
        heartbeat=heartbeat,
    )
    return pika.BlockingConnection(params)


def setup_queue(
    channel: pika.adapters.blocking_connection.BlockingChannel,
    queue_name: str = QUEUE_NAME,
) -> Any:
    """
    Deklaruje trwałą (durable) kolejkę zadań w RabbitMQ.
    """
    return channel.queue_declare(queue=queue_name, durable=True)


def generate_phone_number() -> str:
    """
    Generuje losowy numer telefonu w polskim formacie.
    """
    prefix = random.choice(["501", "502", "503", "601", "602", "701", "888"])
    part1 = random.randint(100, 999)
    part2 = random.randint(100, 999)
    return f"+48 {prefix} {part1} {part2}"


def send_task(
    topic: str = "Konsultacja telefoniczna",
    task_id: Optional[int] = None,
    host: str = RABBITMQ_HOST,
    port: int = RABBITMQ_PORT,
    queue_name: str = QUEUE_NAME,
) -> dict[str, Any]:
    """
    Wysyła jedno zadanie (rozmowę) do kolejki RabbitMQ ze statusem 'pending'.
    """
    connection = get_connection(host=host, port=port)
    channel = connection.channel()
    setup_queue(channel, queue_name)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tid = task_id or int(time.time() * 1000) % 1000000

    task_payload = {
        "id": tid,
        "topic": topic,
        "client_phone": generate_phone_number(),
        "status": STATUS_PENDING,
        "worker_id": None,
        "created_at": now_str,
    }

    body = json.dumps(task_payload)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ),
    )
    connection.close()
    return task_payload


def get_queue_stats(
    host: str = RABBITMQ_HOST,
    port: int = RABBITMQ_PORT,
    queue_name: str = QUEUE_NAME,
) -> dict[str, int]:
    """
    Pobiera liczbę oczekujących wiadomości oraz aktywnych konsumentów.
    """
    connection = get_connection(host=host, port=port)
    channel = connection.channel()
    declare_ok = channel.queue_declare(
        queue=queue_name, durable=True, passive=False
    )
    msg_count = declare_ok.method.message_count
    consumer_count = declare_ok.method.consumer_count
    connection.close()

    return {
        "message_count": msg_count,
        "consumer_count": consumer_count,
    }
