"""
services/utils.py
Contains helper functions for safe input parsing and computations.
"""

from typing import Tuple, List
from models.student import Student


def safe_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid entry, please enter a number.")


def safe_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Invalid entry, please enter a numeric value.")


def class_min_max_gpa(students: List[Student]) -> Tuple[float, float]:
    """
    Returns (min_gpa, max_gpa) as a tuple.
    If list is empty, returns (0.0, 0.0).
    """
    if not students:
        return (0.0, 0.0)

    gpas = [s.calculate_gpa() for s in students]
    return (min(gpas), max(gpas))
