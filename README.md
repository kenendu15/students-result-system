# Student Result Management System

**Author:** David Kenechukwu Ndu

A menu-driven Python application for registering students, recording subject
scores, calculating totals/averages/grades, and producing reports. Data is
saved to JSON so it persists between runs.

## Requirements
Python 3.8+ (standard library only - nothing to install).

## How to run
```bash
git clone https://github.com/<kenendu15>/student-result-system.git
cd student-result-system
python main.py
```

## Features
- **Students:** add, view, search (ID or name), update, delete
- **Scores:** 5 default subjects (extra subjects allowed), total, average,
  grade, update a score, report card
- **Reports:** ranked/sorted lists, class statistics, export to a .txt file
- **Persistence:** `data/students.json`, created automatically

## Grading scale
| Average | Grade |
|---------|-------|
| 70+     | A     |
| 60-69   | B     |
| 50-59   | C     |
| 40-49   | D     |
| below 40| F     |

## Project structure
```
main.py      menu and user interaction
student.py   Student class + validation (regex, dates)
results.py   grading, sorting, class statistics
storage.py   load/save JSON
reports.py   text report builders and file export
data/        students.json lives here
reports/     exported reports are saved here
```

## Author
David Kenechukwu Ndu
