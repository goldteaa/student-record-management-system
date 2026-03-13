"""
models/graduate_student.py
Contains the GraduateStudent class, extending Student with thesis_title.
"""

from models.student import Student


class GraduateStudent(Student):
    def __init__(self, name: str, student_id: str, email: str, major: str, thesis_title: str) -> None:
        super().__init__(name, student_id, email, major)
        self._thesis_title = ""
        self.set_thesis_title(thesis_title)

    def get_thesis_title(self) -> str:
        return self._thesis_title

    def set_thesis_title(self, thesis_title: str) -> None:
        if not isinstance(thesis_title, str) or not thesis_title.strip():
            raise ValueError("Thesis title must be a non-empty string.")
        self._thesis_title = thesis_title.strip()

    # GraduateStudent can override methods (polymorphism)
    def display_info(self) -> str:
        base = super().display_info()
        return f"{base} | Thesis: {self._thesis_title}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "GraduateStudent"
        data["thesis_title"] = self.get_thesis_title()
        return data
