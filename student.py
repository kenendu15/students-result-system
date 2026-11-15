"""student.py - the Student class and input-validation helpers."""

import re
from datetime import date, datetime

from results import grade_for

ID_PATTERN = re.compile(r"^[A-Za-z0-9]{3,12}$")  # 3-12 letters/digits
DATE_FORMAT = "%Y-%m-%d"
MIN_SUBJECTS = 5
DEFAULT_SUBJECTS = ["English", "Mathematics", "Science",
                    "Social Studies", "ICT"]


def is_valid_id(student_id):
    """True if the ID is 3-12 letters/digits (checked with a regex)."""
    return bool(ID_PATTERN.match(student_id))


def parse_dob(text):
    """Convert 'YYYY-MM-DD' text into a date; raise ValueError if invalid."""
    dob = datetime.strptime(text, DATE_FORMAT).date()
    if dob > date.today():
        raise ValueError("Date of birth cannot be in the future.")
    return dob


class Student:
    """One student and their subject scores."""

    def __init__(self, student_id, name, form, gender, dob,
                 scores=None, result_date=None):
        self.student_id = student_id.upper()
        self.name = name
        self.form = form
        self.gender = gender
        self.dob = dob                    # stored as 'YYYY-MM-DD' text
        self.scores = scores or {}        # {"Mathematics": 78.0, ...}
        self.result_date = result_date    # when scores were last entered

    # ---- scores -------------------------------------------------------
    def set_score(self, subject, score):
        """Add or change a subject score (0-100) and stamp today's date."""
        score = float(score)              # ValueError if not a number
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")
        self.scores[subject] = score
        self.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    @property
    def total(self):
        return sum(self.scores.values())

    @property
    def average(self):
        return self.total / len(self.scores) if self.scores else 0.0

    @property
    def grade(self):
        return grade_for(self.average) if self.scores else "-"

    def has_enough_scores(self):
        return len(self.scores) >= MIN_SUBJECTS

    # ---- saving / loading ----------------------------------------------
    def to_dict(self):
        """Turn the object into a plain dict so it can be saved as JSON."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "form": self.form,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Student from a dict loaded from JSON."""
        return cls(data["student_id"], data["name"], data["form"],
                   data["gender"], data["dob"],
                   data.get("scores", {}), data.get("result_date"))

    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.form})"
