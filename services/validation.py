"""
services/validation.py
Contains validation utilities such as regular expression checks.
"""

import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
ID_PATTERN = re.compile(r"^[A-Za-z]{3}\d{4,}$")  # Example: STU1001, ABC12345


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email))


def is_valid_student_id(student_id: str) -> bool:
    return bool(ID_PATTERN.match(student_id))
