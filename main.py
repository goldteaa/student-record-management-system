"""
main.py
Console-based Student Record Management System with menu and operations.
"""

from typing import List, Set

from models.student import Student
from models.graduate_student import GraduateStudent
from services.storage import load_students_from_csv, save_students_to_json
from services.validation import is_valid_student_id
from services.utils import safe_int, safe_float, class_min_max_gpa


def find_student_by_id(students: List[Student], sid: str) -> Student | None:
    for s in students:
        if s.get_id() == sid:
            return s
    return None


def search_students(students: List[Student]) -> None:
    query = input("Enter a student ID or name (or part of name): ").strip()
    if not query:
        print("Empty search.")
        return

    # If it matches ID pattern, treat as ID search, else name search
    if is_valid_student_id(query):
        s = find_student_by_id(students, query)
        if s:
            print(s.display_info())
        else:
            print("No student found with that ID.")
        return

    # Name search (case-insensitive substring)
    q = query.lower()
    matches = [s for s in students if q in s.get_name().lower()]
    if not matches:
        print("No student found with that name.")
        return

    for s in matches:
        print(s.display_info())


def list_students(students: List[Student]) -> None:
    if not students:
        print("No students loaded.")
        return

    print("\nSort by:")
    print("1) Name (default __lt__)")
    print("2) GPA")
    print("3) ID")
    print("4) No sorting")
    choice = safe_int("Choose option: ")

    if choice == 1:
        sorted_list = sorted(students)  # uses __lt__ implemented in Student
    elif choice == 2:
        sorted_list = sorted(students, key=lambda s: s.calculate_gpa(), reverse=True)
    elif choice == 3:
        sorted_list = sorted(students, key=lambda s: s.get_id())
    else:
        sorted_list = list(students)

    for s in sorted_list:
        print(s.display_info())

    mn, mx = class_min_max_gpa(students)
    print(f"\nClass GPA range (min,max) = ({mn}, {mx})")


def filter_students(students: List[Student]) -> None:
    if not students:
        print("No students loaded.")
        return

    print("\nFilter by:")
    print("1) GPA threshold")
    print("2) Major")
    choice = safe_int("Choose option: ")

    if choice == 1:
        threshold = safe_float("Enter minimum GPA (average grade): ")
        filtered = [s for s in students if s.calculate_gpa() >= threshold]
    elif choice == 2:
        major = input("Enter major to filter by: ").strip().lower()
        filtered = [s for s in students if s.get_major().lower() == major]
    else:
        print("Invalid option.")
        return

    if not filtered:
        print("No students matched the filter.")
        return

    for s in filtered:
        print(s.display_info())


def add_student_interactive(students: List[Student], id_set: Set[str]) -> None:
    print("\nAdd new student:")
    stype = input("Type (S=Student, G=GraduateStudent): ").strip().upper()
    if stype not in {"S", "G"}:
        print("Invalid type.")
        return

    name = input("Enter student's name: ").strip()
    sid = input("Enter student ID (e.g. STU1001): ").strip()
    email = input("Enter email: ").strip()
    major = input("Enter major: ").strip()

    if not is_valid_student_id(sid):
        print("Invalid ID format.")
        return
    if sid in id_set:
        print("This ID already exists.")
        return

    if stype == "G":
        thesis = input("Enter thesis title: ").strip()
        try:
            student = GraduateStudent(name, sid, email, major, thesis)
        except ValueError as e:
            print(f"Error: {e}")
            return
    else:
        try:
            student = Student(name, sid, email, major)
        except ValueError as e:
            print(f"Error: {e}")
            return

    num_courses = safe_int("Enter number of courses to input grades for: ")
    for i in range(num_courses):
        course = input(f"Course {i+1} name: ").strip()
        grade = safe_float(f"Course {i+1} grade (0-100): ")
        try:
            student.add_or_update_grade(course, grade)
        except ValueError as e:
            print(f"Error: {e}")
            print("This course entry was skipped.")

    print("\nSummary:")
    print(student.display_info())
    confirm = input("Confirm add? (Y/N): ").strip().upper()
    if confirm == "Y":
        students.append(student)
        id_set.add(sid)
        print("Student added successfully.")
    else:
        print("Cancelled.")


def update_grade_interactive(students: List[Student]) -> None:
    if not students:
        print("No students loaded.")
        return

    sid = input("Enter student ID to update: ").strip()
    student = find_student_by_id(students, sid)
    if not student:
        print("Student not found.")
        return

    course = input("Enter course to add/update: ").strip()
    grade = safe_float("Enter new grade (0-100): ")
    try:
        student.add_or_update_grade(course, grade)
        print("Grade updated.")
        print(student.display_info())
    except ValueError as e:
        print(f"Error: {e}")


def load_data_interactive(students: List[Student], id_set: Set[str]) -> None:
    filename = input("Enter CSV filename/path to load: ").strip()
    try:
        new_students = load_students_from_csv(filename, id_set)
        students.extend(new_students)
        print(f"{len(new_students)} student records loaded successfully.")
    except FileNotFoundError:
        print("File not found. Please check the filename/path.")
    except ValueError as e:
        print(f"Data error: {e}")
    except Exception as e:
        print(f"Unexpected error while loading: {e}")


def save_data_interactive(students: List[Student]) -> None:
    if not students:
        print("No students to save.")
        return

    filename = input("Enter JSON filename to save (e.g., students_out.json): ").strip()
    if not filename.lower().endswith(".json"):
        filename += ".json"

    try:
        save_students_to_json(filename, students)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error while saving: {e}")


def main() -> None:
    students: List[Student] = []
    id_set: Set[str] = set()

    while True:
        print("\nStudent Record Management - Main Menu")
        print("1. Load student records from CSV")
        print("2. List all students")
        print("3. Search for a student by ID or name")
        print("4. Filter students")
        print("5. Add a new student record")
        print("6. Update/Add a course grade for a student")
        print("7. Save student records to JSON")
        print("8. Exit")

        choice = safe_int("Choose an option: ")

        if choice == 1:
            load_data_interactive(students, id_set)
        elif choice == 2:
            list_students(students)
        elif choice == 3:
            search_students(students)
        elif choice == 4:
            filter_students(students)
        elif choice == 5:
            add_student_interactive(students, id_set)
        elif choice == 6:
            update_grade_interactive(students)
        elif choice == 7:
            save_data_interactive(students)
        elif choice == 8:
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
