"""
tests/test_student.py
Unit tests for Student GPA and ordering.
"""

import unittest
from models.student import Student


class TestStudent(unittest.TestCase):
    def test_gpa_calculation(self):
        s = Student("Ana", "STU1002", "ana@uni.edu", "CS")
        self.assertEqual(s.calculate_gpa(), 0.0)
        s.add_or_update_grade("COS3040", 90)
        s.add_or_update_grade("MAT2020", 80)
        self.assertEqual(s.calculate_gpa(), 85.0)

    def test_lt_ordering_by_name(self):
        a = Student("Ana", "STU1", "ana@uni.edu", "CS")
        b = Student("Bora", "STU2", "bora@uni.edu", "CS")
        self.assertTrue(a < b)


if __name__ == "__main__":
    unittest.main()
