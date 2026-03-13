"""
models/person.py
Contains the Person base class with encapsulated attributes and validation.
"""

from services.validation import is_valid_email


class Person:
    def __init__(self, name: str, person_id: str, email: str) -> None:
        self._name = ""
        self._id = ""
        self._email = ""

        self.set_name(name)
        self.set_id(person_id)
        self.set_email(email)

    # --- Getters ---
    def get_name(self) -> str:
        return self._name

    def get_id(self) -> str:
        return self._id

    def get_email(self) -> str:
        return self._email

    # --- Setters with validation ---
    def set_name(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = name.strip()

    def set_id(self, person_id: str) -> None:
        if not isinstance(person_id, str) or not person_id.strip():
            raise ValueError("ID must be a non-empty string.")
        self._id = person_id.strip()

    def set_email(self, email: str) -> None:
        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email must be a non-empty string.")
        email = email.strip()
        if not is_valid_email(email):
            raise ValueError(f"Invalid email format: {email}")
        self._email = email

    def display_info(self) -> str:
        return f"Name: {self._name} | ID: {self._id} | Email: {self._email}"
