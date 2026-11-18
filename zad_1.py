class Student:
    """
    Klasa reprezentująca studenta wraz z ocenami.
    """

    def __init__(self, name: str, marks: list[float | int]) -> None:
        self.name: str = name
        self.marks: list[float | int] = marks

    def is_passed(self) -> bool:
        """
        Zwraca True, gdy średnia ocen jest większa niż 50, w przeciwnym razie False.
        """
        if not self.marks:
            return False
        average: float = sum(self.marks) / len(self.marks)
        return average > 50

    def __str__(self) -> str:
        srednia = sum(self.marks) / len(self.marks) if self.marks else 0.0
        status = "ZALICZONY" if self.is_passed() else "NIEZALICZONY"
        return f"Student: {self.name}, Oceny: {self.marks}, Średnia: {srednia:.2f} -> {status}"


if __name__ == "__main__":
    # Obiekt 1: średnia > 50 (zwraca True)
    student_zdajacy = Student("Jan Kowalski", [60, 75, 80, 55])

    # Obiekt 2: średnia <= 50 (zwraca False)
    student_niezdajacy = Student("Anna Nowak", [30, 45, 50, 40])

    print("--- Test is_passed() ---")
    print(f"{student_zdajacy.name} zaliczył: {student_zdajacy.is_passed()}")
    print(f"{student_niezdajacy.name} zaliczył: {student_niezdajacy.is_passed()}")

    print("\n--- Informacje o studentach ---")
    print(student_zdajacy)
    print(student_niezdajacy)
