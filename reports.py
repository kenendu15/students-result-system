"""reports.py - builds text reports and saves them to files."""

import os
from datetime import datetime

from results import class_statistics, remark_for, sort_by_average

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "reports")
LINE = "=" * 64


def report_card_text(student):
    """Return one student's report card as a string."""
    lines = [LINE, "STUDENT REPORT CARD".center(64), LINE,
             f"Student ID : {student.student_id}",
             f"Name       : {student.name}",
             f"Class/Form : {student.form}",
             f"Gender     : {student.gender}",
             f"Birth date : {student.dob}",
             "-" * 64,
             f"{'Subject':<30}{'Score':>10}",
             "-" * 64]
    if not student.scores:
        lines.append("No scores recorded yet.")
    else:
        for subject, score in student.scores.items():
            lines.append(f"{subject:<30}{score:>10.1f}")
        lines += ["-" * 64,
                  f"{'Total':<30}{student.total:>10.1f}",
                  f"{'Average':<30}{student.average:>10.2f}",
                  f"{'Grade':<30}{student.grade:>10}",
                  f"{'Remark':<30}{remark_for(student.grade):>10}",
                  f"Result entered: {student.result_date}"]
    lines.append(LINE)
    return "\n".join(lines)


def student_list_text(students, title="ALL STUDENTS"):
    """Return a table of students with total, average and grade."""
    lines = [title, "-" * 72,
             f"{'ID':<10}{'Name':<24}{'Form':<10}"
             f"{'Total':>10}{'Average':>10}{'Grade':>8}",
             "-" * 72]
    for s in students:
        lines.append(f"{s.student_id:<10}{s.name[:22]:<24}{s.form:<10}"
                     f"{s.total:>10.1f}{s.average:>10.2f}{s.grade:>8}")
    if not students:
        lines.append("(no students)")
    lines.append("-" * 72)
    return "\n".join(lines)


def statistics_text(students):
    """Return class statistics as a string."""
    stats = class_statistics(students)
    if stats is None:
        return "CLASS STATISTICS\nNo scores recorded yet."
    hi, lo = stats["highest"], stats["lowest"]
    return "\n".join([
        "CLASS STATISTICS", "-" * 72,
        f"Students with scores : {stats['count']}",
        f"Highest score        : {hi[0]:.1f}  ({hi[1]}, {hi[2]})",
        f"Lowest score         : {lo[0]:.1f}  ({lo[1]}, {lo[2]})",
        f"Class average        : {stats['class_average']:.2f}",
        f"Top student          : {stats['top_student'].name} "
        f"({stats['top_student'].average:.2f})",
        f"Lowest student       : {stats['bottom_student'].name} "
        f"({stats['bottom_student'].average:.2f})",
        "-" * 72])


def full_report_text(students):
    """Return the complete class report (ranked list + statistics)."""
    stamp = datetime.now().strftime("%d %B %Y, %H:%M")
    ranked = sort_by_average(students)
    return "\n\n".join([
        f"STUDENT RESULT REPORT - generated {stamp}",
        student_list_text(ranked, "CLASS RANKING (highest average first)"),
        statistics_text(students)])


def save_report(text, directory=REPORTS_DIR):
    """Save report text to a time-stamped .txt file; return its path."""
    os.makedirs(directory, exist_ok=True)
    name = datetime.now().strftime("report_%Y%m%d_%H%M%S.txt")
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text + "\n")
    return path
