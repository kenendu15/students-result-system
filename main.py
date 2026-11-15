"""main.py - entry point and menu-driven interface.

Run with:  python main.py
"""

from student import (DEFAULT_SUBJECTS, MIN_SUBJECTS, Student,
                     is_valid_id, parse_dob)
from results import sort_by_average, sort_by_name
from storage import load_students, save_students
import reports


# ---------------------------------------------------------------- input helpers
def ask_text(prompt, allow_blank=False):
    """Keep asking until the user types something (or blank if allowed)."""
    while True:
        value = input(prompt).strip()
        if value or allow_blank:
            return value
        print("  This field cannot be empty.")


def ask_id(prompt, students, must_exist):
    """Ask for a valid student ID; check it exists / does not exist."""
    while True:
        student_id = input(prompt).strip().upper()
        if not is_valid_id(student_id):
            print("  ID must be 3-12 letters/digits (e.g. STU001).")
        elif must_exist and student_id not in students:
            print("  No student with that ID.")
        elif not must_exist and student_id in students:
            print("  That ID is already registered.")
        else:
            return student_id


def ask_gender(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip().upper()
        if value == "" and allow_blank:
            return ""
        if value in ("M", "F"):
            return value
        print("  Enter M or F.")


def ask_dob(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if value == "" and allow_blank:
            return ""
        try:
            parse_dob(value)
        except ValueError as error:
            print(f"  Invalid date ({error}). Use YYYY-MM-DD.")
        else:
            return value


def ask_score(prompt):
    """Ask for a score between 0 and 100."""
    while True:
        try:
            score = float(input(prompt).strip())
            if not 0 <= score <= 100:
                raise ValueError
        except ValueError:
            print("  Enter a number between 0 and 100.")
        else:
            return score


def confirm(prompt):
    return input(prompt + " (y/n): ").strip().lower() == "y"


def pick_student(students, prompt="Enter Student ID: "):
    if not students:
        print("No students registered yet.")
        return None
    return students[ask_id(prompt, students, must_exist=True)]


def save(students):
    if save_students(students):
        print("  (data saved)")


# ---------------------------------------------------------------- student menu
def add_student(students):
    print("\n--- Add Student ---")
    student_id = ask_id("Student ID: ", students, must_exist=False)
    name = ask_text("Full name: ")
    form = ask_text("Class/Form (e.g. Form 3): ")
    gender = ask_gender("Gender (M/F): ")
    dob = ask_dob("Date of birth (YYYY-MM-DD): ")
    students[student_id] = Student(student_id, name, form, gender, dob)
    print(f"Added {students[student_id]}.")
    save(students)


def view_students(students):
    print()
    print(reports.student_list_text(sort_by_name(students.values())))


def search_students(students):
    term = ask_text("\nSearch by ID or name: ").lower()
    found = [s for s in students.values()
             if term == s.student_id.lower() or term in s.name.lower()]
    if found:
        print(reports.student_list_text(found, f"{len(found)} MATCH(ES)"))
    else:
        print("No matching student.")


def update_student(students):
    student = pick_student(students)
    if not student:
        return
    print("Press Enter to keep the current value.")
    student.name = ask_text(f"Name [{student.name}]: ", True) or student.name
    student.form = ask_text(f"Form [{student.form}]: ", True) or student.form
    student.gender = (ask_gender(f"Gender [{student.gender}]: ", True)
                      or student.gender)
    student.dob = ask_dob(f"DOB [{student.dob}]: ", True) or student.dob
    print("Student updated.")
    save(students)


def delete_student(students):
    student = pick_student(students)
    if student and confirm(f"Delete {student}?"):
        del students[student.student_id]
        print("Student deleted.")
        save(students)


# ---------------------------------------------------------------- score menu
def record_scores(students):
    student = pick_student(students)
    if not student:
        return
    if student.scores and not confirm("Scores already exist. Overwrite them?"):
        return
    student.scores = {}
    print(f"Enter scores (0-100) for {student.name}:")
    for subject in DEFAULT_SUBJECTS:
        student.set_score(subject, ask_score(f"  {subject}: "))
    while confirm("Add another subject?"):
        subject = ask_text("  Subject name: ").title()
        student.set_score(subject, ask_score(f"  {subject}: "))
    print(f"Average {student.average:.2f}, grade {student.grade}.")
    save(students)


def update_score(students):
    student = pick_student(students)
    if not student:
        return
    if not student.scores:
        print("No scores yet - use 'Record scores' first.")
        return
    print("Subjects:", ", ".join(student.scores))
    subject = ask_text("Subject to change: ").title()
    if subject not in student.scores:
        print("That subject is not on this student's record.")
        return
    student.set_score(subject, ask_score(f"New score for {subject}: "))
    print(f"Updated. New average {student.average:.2f} ({student.grade}).")
    save(students)


def show_report_card(students):
    student = pick_student(students)
    if student:
        print()
        print(reports.report_card_text(student))


# ---------------------------------------------------------------- reports menu
def list_results(students):
    print("\n1. Highest average first\n2. By name")
    choice = input("Sort by: ").strip()
    people = students.values()
    ordered = sort_by_name(people) if choice == "2" else sort_by_average(people)
    print()
    print(reports.student_list_text(ordered, "STUDENT RESULTS"))


def show_statistics(students):
    print()
    print(reports.statistics_text(students.values()))


def export_report(students):
    text = reports.full_report_text(list(students.values()))
    try:
        path = reports.save_report(text)
    except OSError as error:
        print(f"Could not save report: {error}")
    else:
        print(f"Report saved to {path}")


# ---------------------------------------------------------------- menus
def run_menu(title, options, students):
    """Show a numbered menu and run the chosen function until 0 (back)."""
    while True:
        print(f"\n=== {title} ===")
        for number, (label, _) in options.items():
            print(f"{number}. {label}")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "0":
            return
        if choice in options:
            options[choice][1](students)
        else:
            print("Invalid choice.")


STUDENT_MENU = {"1": ("Add student", add_student),
                "2": ("View all students", view_students),
                "3": ("Search student", search_students),
                "4": ("Update student", update_student),
                "5": ("Delete student", delete_student)}

SCORE_MENU = {"1": ("Record scores", record_scores),
              "2": ("Update a score", update_score),
              "3": ("Show report card", show_report_card)}

REPORT_MENU = {"1": ("List results (sorted)", list_results),
               "2": ("Class statistics", show_statistics),
               "3": ("Export report to file", export_report)}


def main():
    print("STUDENT RESULT MANAGEMENT SYSTEM")
    students = load_students()
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Student management\n2. Scores / results\n"
              "3. Reports & analysis\n0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            run_menu("STUDENT MANAGEMENT", STUDENT_MENU, students)
        elif choice == "2":
            run_menu("SCORES / RESULTS", SCORE_MENU, students)
        elif choice == "3":
            run_menu("REPORTS & ANALYSIS", REPORT_MENU, students)
        elif choice == "0":
            save(students)
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
