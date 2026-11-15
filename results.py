"""results.py - grading logic, class statistics and sorting.

No input/output happens here: these are pure functions that take data in
and return answers, which makes them easy to test and reuse.
"""

# (minimum average, grade) checked from highest to lowest.
GRADE_BOUNDARIES = [(70, "A"), (60, "B"), (50, "C"), (40, "D")]


def grade_for(average):
    """Return a letter grade for an average score."""
    for minimum, letter in GRADE_BOUNDARIES:
        if average >= minimum:
            return letter
    return "F"


def remark_for(grade):
    """Return a short teacher-style remark for a grade."""
    remarks = {"A": "Excellent", "B": "Very Good", "C": "Good",
               "D": "Fair", "F": "Fail"}
    return remarks[grade]


def sort_by_average(students, highest_first=True):
    """Sort Student objects by average score."""
    return sorted(students, key=lambda s: s.average, reverse=highest_first)


def sort_by_name(students):
    """Sort Student objects alphabetically by name (case-insensitive)."""
    return sorted(students, key=lambda s: s.name.lower())


def class_statistics(students):
    """Work out class-wide statistics.

    Returns None if nobody has scores yet, otherwise a dictionary with the
    highest/lowest single subject score (and who got it), the class average
    (mean of student averages) and the best/worst student.
    """
    scored = [s for s in students if s.scores]
    if not scored:
        return None

    highest = lowest = None  # each becomes a tuple: (score, name, subject)
    for student in scored:
        for subject, score in student.scores.items():
            entry = (score, student.name, subject)
            if highest is None or score > highest[0]:
                highest = entry
            if lowest is None or score < lowest[0]:
                lowest = entry

    averages = [s.average for s in scored]
    return {
        "count": len(scored),
        "highest": highest,
        "lowest": lowest,
        "class_average": sum(averages) / len(averages),
        "top_student": max(scored, key=lambda s: s.average),
        "bottom_student": min(scored, key=lambda s: s.average),
    }
