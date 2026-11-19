"""
Moduł producer.py - dodawanie zadań do bazy danych SQLite.
Domyślnie dodaje 1 rekord (np. 1 rozmowę telefoniczną).
Opcjonalnie umożliwia dodanie N rekordów (np. --count 100).
"""

import argparse
from queue_manager import add_task, init_db


def parse_arguments() -> argparse.Namespace:
    """
    Parsuje parametry wiersza poleceń dla producera.
    """
    parser = argparse.ArgumentParser(
        description="Producer - dodawanie zadań do bazy SQLite."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Liczba zadań do dodania (domyślnie 1).",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Rozmowa telefoniczna z klientem",
        help="Temat zadania.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    init_db()

    print(f"[Producer] Generowanie {args.count} zadania/zadań w SQLite...")
    for i in range(1, args.count + 1):
        task = add_task(topic=f"{args.topic} #{i}")
        print(
            f"[Producer] Dodano zadanie ID: {task['id']} | "
            f"Klient: {task['client_phone']} | "
            f"Status: {task['status']}"
        )

    print(f"[Producer] Pomyślnie dodano {args.count} zadań do bazy danych.")


if __name__ == "__main__":
    main()
