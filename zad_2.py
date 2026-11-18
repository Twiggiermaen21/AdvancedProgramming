from typing import Optional
from zad_1 import Student


class Library:
    """
    Klasa opisująca bibliotekę.
    """

    def __init__(
        self,
        name: str,
        city: str,
        street: str,
        zip_code: str,
        open_hours: str,
        phone: str,
    ) -> None:
        self.name: str = name
        self.city: str = city
        self.street: str = street
        self.zip_code: str = zip_code
        self.open_hours: str = open_hours
        self.phone: str = phone

    def __str__(self) -> str:
        return (
            f"Biblioteka '{self.name}' ({self.street}, {self.zip_code} {self.city}, "
            f"Godziny otwarcia: {self.open_hours}, Tel: {self.phone})"
        )


class Employee:
    """
    Klasa opisująca pracownika biblioteki.
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        hire_date: str,
        birth_date: str,
        city: str,
        street: str,
        zip_code: str,
        phone: str,
    ) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.hire_date: str = hire_date
        self.birth_date: str = birth_date
        self.city: str = city
        self.street: str = street
        self.zip_code: str = zip_code
        self.phone: str = phone

    def __str__(self) -> str:
        return (
            f"Pracownik: {self.first_name} {self.last_name} "
            f"(Zatrudniony: {self.hire_date}, Data ur.: {self.birth_date}, "
            f"Adres: {self.street}, {self.zip_code} {self.city}, Tel: {self.phone})"
        )


class Book:
    """
    Klasa opisująca książkę.
    """

    def __init__(
        self,
        title: str,
        library: Library,
        publication_date: str,
        author_name: str,
        author_surname: str,
        number_of_pages: int,
    ) -> None:
        self.title: str = title
        self.library: Library = library
        self.publication_date: str = publication_date
        self.author_name: str = author_name
        self.author_surname: str = author_surname
        self.number_of_pages: int = number_of_pages

    def __str__(self) -> str:
        return (
            f"Książka: \"{self.title}\" autorstwa {self.author_name} {self.author_surname} "
            f"(Wydano: {self.publication_date}, Stron: {self.number_of_pages})\n"
            f"      Lokalizacja: {self.library}"
        )


class Order:
    """
    Klasa opisująca zamówienie biblioteczne.
    """

    def __init__(
        self,
        employee: Employee,
        student: Student,
        books: list[Book],
        order_date: str,
    ) -> None:
        self.employee: Employee = employee
        self.student: Student = student
        self.books: list[Book] = books
        self.order_date: str = order_date

    def __str__(self) -> str:
        ksiazki_str = "\n".join(f"    - {ksiazka}" for ksiazka in self.books)
        return (
            f"================ ZAMÓWIENIE (Data: {self.order_date}) ================\n"
            f"Obsługujący pracownik:\n  {self.employee}\n"
            f"Zamawiający student:\n  {self.student}\n"
            f"Zamówione książki ({len(self.books)}):\n{ksiazki_str}\n"
            f"=================================================================="
        )


if __name__ == "__main__":
    # 1. Stworzenie 2 bibliotek
    bib_glowna = Library(
        name="Biblioteka Główna UEK",
        city="Katowice",
        street="ul. 1 Maja 50",
        zip_code="40-287",
        open_hours="08:00 - 19:00",
        phone="32 257 70 00",
    )
    bib_filia = Library(
        name="Biblioteka Wydziałowa",
        city="Katowice",
        street="ul. Bogucicka 3",
        zip_code="40-226",
        open_hours="09:00 - 17:00",
        phone="32 257 71 11",
    )

    # 2. Stworzenie 3 pracowników
    pracownik1 = Employee(
        first_name="Marek",
        last_name="Zieliński",
        hire_date="2018-03-01",
        birth_date="1985-06-12",
        city="Katowice",
        street="ul. Francuska 12",
        zip_code="40-028",
        phone="501-111-222",
    )
    pracownik2 = Employee(
        first_name="Beata",
        last_name="Kozłowska",
        hire_date="2020-09-15",
        birth_date="1990-11-23",
        city="Sosnowiec",
        street="ul. Warszawska 5",
        zip_code="41-200",
        phone="502-333-444",
    )
    pracownik3 = Employee(
        first_name="Tomasz",
        last_name="Wójcik",
        hire_date="2022-01-10",
        birth_date="1995-02-18",
        city="Chorzów",
        street="ul. Wolności 44",
        zip_code="41-500",
        phone="503-555-666",
    )

    # 3. Stworzenie 3 studentów
    student1 = Student(name="Kacper Pudełko", marks=[85, 90, 78, 92])
    student2 = Student(name="Michał Wiśniewski", marks=[45, 50, 40, 52])
    student3 = Student(name="Aleksandra Dąbrowska", marks=[95, 88, 92, 100])

    # 4. Stworzenie 5 książek
    ksiazka1 = Book(
        title="Czysty Kod",
        library=bib_glowna,
        publication_date="2008-08-01",
        author_name="Robert",
        author_surname="Martin",
        number_of_pages=464,
    )
    ksiazka2 = Book(
        title="Python. Instrukcje dla programisty",
        library=bib_glowna,
        publication_date="2019-05-15",
        author_name="Eric",
        author_surname="Matthes",
        number_of_pages=560,
    )
    ksiazka3 = Book(
        title="Wprowadzenie do algorytmów",
        library=bib_filia,
        publication_date="2009-07-31",
        author_name="Thomas",
        author_surname="Cormen",
        number_of_pages=1312,
    )
    ksiazka4 = Book(
        title="Wzorce projektowe",
        library=bib_glowna,
        publication_date="1994-10-21",
        author_name="Erich",
        author_surname="Gamma",
        number_of_pages=416,
    )
    ksiazka5 = Book(
        title="Sztuczna Inteligencja. Nowoczesne podejście",
        library=bib_filia,
        publication_date="2020-04-28",
        author_name="Stuart",
        author_surname="Russell",
        number_of_pages=1152,
    )

    # 5. Stworzenie 2 zamówień
    zamowienie1 = Order(
        employee=pracownik1,
        student=student1,
        books=[ksiazka1, ksiazka2],
        order_date="2026-11-18",
    )
    zamowienie2 = Order(
        employee=pracownik2,
        student=student3,
        books=[ksiazka3, ksiazka4, ksiazka5],
        order_date="2026-11-19",
    )

    # 6. Wyświetlenie obu zamówień
    print(zamowienie1)
    print("\n")
    print(zamowienie2)
