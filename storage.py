"""storage.py - saving and loading students as JSON."""

import json
import os

from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Load students from disk into a {student_id: Student} dictionary.

    A missing file is normal on first run, so an empty dict is returned.
    A corrupted file is renamed to .bak so it is never overwritten.
    """
    students = {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            raw = json.load(file)
        for record in raw:
            student = Student.from_dict(record)
            students[student.student_id] = student
    except FileNotFoundError:
        print("No data file found - starting with an empty system.")
    except (json.JSONDecodeError, KeyError, TypeError):
        backup = path + ".bak"
        os.replace(path, backup)
        print(f"Data file was unreadable. Saved a copy as {backup}.")
        students = {}
    else:
        print(f"Loaded {len(students)} student(s) from {path}.")
    return students


def save_students(students, path=DATA_FILE):
    """Write all students to disk. Returns True on success.

    Writes to a temporary file first, then swaps it in, so a crash in the
    middle of saving cannot destroy the existing data.
    """
    temp_path = path + ".tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump([s.to_dict() for s in students.values()],
                      file, indent=4)
        os.replace(temp_path, path)
    except OSError as error:
        print(f"Could not save data: {error}")
        return False
    else:
        return True
    finally:
        if os.path.exists(temp_path):   # clean up if something went wrong
            os.remove(temp_path)
