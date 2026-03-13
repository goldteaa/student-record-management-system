"""
tests/test_graduate_student.py
Unit tests for GraduateStudent thesis field and display.
"""

import unittest
from models.graduate_student import GraduateStudent


class TestGraduateStudent(unittest.TestCase):
    def test_thesis_title(self):
        g = GraduateStudent("Elio", "STU3001", "elio@uni.edu", "DS", "My Thesis")
        self.assertEqual(g.get_thesis_title(), "My Thesis")
        self.assertIn("Thesis", g.display_info())


if __name__ == "__main__":
    unittest.main()
