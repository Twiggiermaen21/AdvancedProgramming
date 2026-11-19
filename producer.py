"""
Moduł producer.py - publikowanie zadań do brokera RabbitMQ.
Domyślnie dodaje 1 rekord (np. 1 rozmowę telefoniczną).
Opcjonalnie umożliwia dodanie N rekordów (np. --count 100).
"""

import argparse
from queue_manager import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    get_connection,
    send_task,
    setup_queue,
)


def parse_arguments() -> argparse.Namespace:
    """
    Parsuje parametry wiersza poleceń dla producera.
    """
    parser = argparse.ArgumentParser(
        description="Producer - wysyłanie zadań do kolejki RabbitMQ."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Liczba zadań do dodania do kolejki (domyślnie 1).",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Rozmowa telefoniczna z klientem",
        help="Temat zadania.",
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
        help="Port AMQP brokera RabbitMQ (domyślnie 8081).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    # Weryfikacja połączenia i kolejki
    connection = get_connection(host=args.host, port=args.port)
    channel = connection.channel()
    setup_queue(channel)
    connection.close()

    print(f"[Producer] Wysyłanie {args.count} zadania/zadań do RabbitMQ...")
    for i in range(1, args.count + 1):
        task = send_task(
            topic=f"{args.topic} #{i}",
            task_id=i,
            host=args.host,
            port=args.port,
        )
        print(
            f"[Producer] Wysłano zadanie ID: {task['id']} | "
            f"Klient: {task['client_phone']} | "
            f"Status: {task['status']}"
        )

    print(f"[Producer] Pomyślnie dodano {args.count} zadań do RabbitMQ.")


if __name__ == "__main__":
    main()
