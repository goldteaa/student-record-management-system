"""
tests/test_person.py
Unit tests for the Person class.
"""

import unittest
from models.person import Person


class TestPerson(unittest.TestCase):
    def test_valid_person(self):
        p = Person("John", "STU1001", "john@example.com")
        self.assertEqual(p.get_name(), "John")
        self.assertEqual(p.get_id(), "STU1001")
        self.assertEqual(p.get_email(), "john@example.com")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            Person("John", "STU1001", "not-an-email")


if __name__ == "__main__":
    unittest.main()
