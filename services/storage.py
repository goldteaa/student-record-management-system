"""
services/storage.py
Handles file input/output (CSV load, JSON save) for student records.
"""

import csv
import json
from typing import List, Set

from models.student import Student
from models.graduate_student import GraduateStudent
from services.validation import is_valid_student_id


def parse_courses(courses_field: str) -> dict:
    """
    Parses: "COS3040:95;MAT2020:88" -> {"COS3040": 95.0, "MAT2020": 88.0}
    """
    grades = {}
    courses_field = (courses_field or "").strip()
    if not courses_field:
        return grades

    parts = courses_field.split(";")
    for item in parts:
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError(f"Invalid course format (missing ':'): {item}")

        course, grade_str = item.split(":", 1)
        course = course.strip()
        grade_str = grade_str.strip()

        try:
            grade = float(grade_str)
        except ValueError as e:
            raise ValueError(f"Invalid grade value '{grade_str}' for course '{course}'.") from e

        grades[course] = grade

    return grades


def load_students_from_csv(filename: str, existing_ids: Set[str]) -> List[Student]:
    """
    Loads students from CSV. Uses 'existing_ids' set to avoid duplicates.
    Returns a list of Student/GraduateStudent objects.

    Expected CSV columns:
    type,name,id,email,major,thesis_title,courses

    type must start with S or G (we accept values like 'S', 'Student', 'G ', etc.)
    """
    students: List[Student] = []

    # utf-8-sig automatically removes a BOM if Excel wrote one at the start of the file.
    with open(filename, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for line_num, row in enumerate(reader, start=1):
            # Skip empty or whitespace-only rows safely
            if not row or all(not str(cell).strip() for cell in row):
                continue

            # Expected:
            # type,name,id,email,major,thesis_title,courses
            if len(row) < 7:
                raise ValueError(f"Line {line_num}: Expected 7 columns, got {len(row)}")

            # --- IMPORTANT: robust type cleaning ---
            raw_type = str(row[0]) if row[0] is not None else ""
            rec_type = raw_type.strip().upper().replace("\ufeff", "")

            if not rec_type:
                raise ValueError(f"Line {line_num}: Missing student type in first column (use S or G).")

            # If someone wrote "Student" or "S " we only take the first character
            rec_type = rec_type[0]

            name = str(row[1]).strip()
            sid = str(row[2]).strip()
            email = str(row[3]).strip()
            major = str(row[4]).strip()
            thesis_title = str(row[5]).strip()
            courses_field = str(row[6]).strip()

            if not is_valid_student_id(sid):
                raise ValueError(f"Line {line_num}: Invalid student ID format: {sid}")

            if sid in existing_ids:
                # skip duplicates safely
                continue

            if rec_type == "G":
                student = GraduateStudent(name, sid, email, major, thesis_title)
            elif rec_type == "S":
                student = Student(name, sid, email, major)
            else:
                raise ValueError(f"Line {line_num}: Unknown type '{rec_type}' (use S or G)")

            grades = parse_courses(courses_field)
            for course, grade in grades.items():
                student.add_or_update_grade(course, grade)

            students.append(student)
            existing_ids.add(sid)

    return students


def save_students_to_json(filename: str, students: List[Student]) -> None:
    """
    Saves all students to a JSON file using each object's to_dict() method.
    """
    data = [s.to_dict() for s in students]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
