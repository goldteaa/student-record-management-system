"""
models/student.py
Contains the Student class (subclass of Person) with grades dictionary and GPA logic.
"""

from __future__ import annotations
from typing import Dict, Optional

from models.person import Person


class Student(Person):
    def __init__(self, name: str, student_id: str, email: str, major: str) -> None:
        super().__init__(name, student_id, email)
        self._major = ""
        self._grades: Dict[str, float] = {}

        self.set_major(major)

    # --- Getters ---
    def get_major(self) -> str:
        return self._major

    def get_grades(self) -> Dict[str, float]:
        # return a copy to protect encapsulation
        return dict(self._grades)

    # --- Setter ---
    def set_major(self, major: str) -> None:
        if not isinstance(major, str) or not major.strip():
            raise ValueError("Major must be a non-empty string.")
        self._major = major.strip()

    # --- Grade operations ---
    def add_or_update_grade(self, course: str, grade: float) -> None:
        if not isinstance(course, str) or not course.strip():
            raise ValueError("Course name must be a non-empty string.")
        course = course.strip()

        if not isinstance(grade, (int, float)):
            raise ValueError("Grade must be numeric.")

        # Common 0-100 scale (you can change if your course uses another)
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100.")

        self._grades[course] = float(grade)

    def get_grade_for_course(self, course: str) -> Optional[float]:
        return self._grades.get(course)

    def calculate_gpa(self) -> float:
        """
        Calculates the average grade (treated as GPA/average).
        If no courses exist, returns 0.0.
        """
        if not self._grades:
            return 0.0
        total = sum(self._grades.values())
        return round(total / len(self._grades), 2)

    # --- Operator overloading: sort by name by default ---
    def __lt__(self, other: "Student") -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_name().lower() < other.get_name().lower()

    # --- Polymorphism: override display_info ---
    def display_info(self) -> str:
        gpa = self.calculate_gpa()
        return (
            f"{super().display_info()} | Major: {self._major} | GPA: {gpa}"
            f" | Courses: {len(self._grades)}"
        )

    # --- Serialization helper for JSON ---
    def to_dict(self) -> dict:
        return {
            "type": "Student",
            "name": self.get_name(),
            "id": self.get_id(),
            "email": self.get_email(),
            "major": self.get_major(),
            "grades": self.get_grades(),
        }
