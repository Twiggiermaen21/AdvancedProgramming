"""
Moduł producer.py - dodawanie zadań do pliku kolejki.
Domyślnie dodaje 1 rekord (np. 1 rozmowę telefoniczną).
Opcjonalnie umożliwia dodanie N rekordów (np. --count 100).
"""

import argparse
from queue_manager import add_task, init_queue_file


def parse_arguments() -> argparse.Namespace:
    """
    Parsuje parametry wiersza poleceń dla modułu producera.
    """
    parser = argparse.ArgumentParser(
        description="Producer - dodawanie zadań do kolejki plikowej."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Liczba zadań do wygenerowania i dodania (domyślnie 1).",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Rozmowa telefoniczna z klientem",
        help="Tytuł lub temat zadania.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    init_queue_file()

    print(f"[Producer] Generowanie {args.count} zadania/zadań...")
    for i in range(1, args.count + 1):
        task = add_task(topic=f"{args.topic} #{i}")
        print(
            f"[Producer] Dodano zadanie ID: {task['id']} | "
            f"Klient: {task['client_phone']} | "
            f"Status: {task['status']}"
        )

    print(f"[Producer] Pomyślnie dodano {args.count} zadań do kolejki.")


if __name__ == "__main__":
    main()
