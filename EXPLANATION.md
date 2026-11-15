# What makes what do what, and why

## The big idea
The program is split by **responsibility**, so each file has one job:

| File | Job | Why separate? |
|------|-----|---------------|
| `student.py` | Defines what a student *is* | Data and its behaviour live together |
| `results.py` | Grades, sorting, statistics | Pure maths/logic, no `input()`/`print()`, so it is reusable |
| `storage.py` | Disk reading/writing | If you switch JSON to CSV, only this file changes |
| `reports.py` | Builds report text | Display logic is kept apart from calculation |
| `main.py` | Menus and user input | The only file that talks to the user |

Dependency direction: `main` -> everything; `student` -> `results`;
`storage` -> `student`; `reports` -> `results`. `results` imports nothing,
which avoids circular imports.

---

## student.py
- **`Student` class (OOP):** `__init__` stores ID, name, form, gender, dob,
  a `scores` dictionary and `result_date`. One object = one student.
- **`scores` is a dict** like `{"English": 80.0}` - subject name -> score.
  A dictionary fits because you look scores up by subject.
- **`set_score()`** converts with `float()` (type conversion), rejects
  anything outside 0-100 by raising `ValueError`, and stamps
  `result_date` with `datetime.now()` (dates and times requirement).
- **`@property` total/average/grade:** calculated every time they are read,
  so they can never be out of date after a score changes. Nothing extra is
  stored.
- **`to_dict()` / `from_dict()`:** JSON can only store basic types (dict,
  list, str, number), not custom objects. `to_dict` flattens a Student for
  saving; `from_dict` (a `@classmethod`, i.e. an alternative constructor)
  rebuilds it on loading.
- **Regex `^[A-Za-z0-9]{3,12}$`:** `^`/`$` mean the whole text must match;
  `[A-Za-z0-9]` allows letters and digits; `{3,12}` sets the length. This
  rejects IDs like `ab`, `STU 01` or `STU-01`.
- **`parse_dob()`:** `datetime.strptime` checks the text really is a date
  (rejects `2008-13-45`); we also refuse future dates.

## results.py
- **`grade_for()`:** a list of `(minimum, letter)` pairs checked from high to
  low; the first one the average reaches wins, otherwise `"F"`. Changing the
  grading scale means editing one list, not the logic.
- **`sort_by_average` / `sort_by_name`:** use `sorted(..., key=lambda ...)`.
  `key` says *what to compare*; `reverse=True` gives highest first;
  `.lower()` makes name sorting ignore capital letters. `sorted` returns a
  new list and leaves the original untouched.
- **`class_statistics()`:** loops through every score of every student,
  keeping the best and worst as tuples `(score, name, subject)`. Class
  average = mean of each student's average. Returns `None` if there are no
  scores, so callers must handle the "empty" case instead of crashing on
  division by zero.

## storage.py
- **Load:** `try/except/else`.
  - `FileNotFoundError` -> first run, start empty (the "file does not exist"
    requirement).
  - `JSONDecodeError/KeyError/TypeError` -> damaged file; it is renamed to
    `.bak` so your old data is not wiped by the next save.
  - `else` runs only if nothing failed (prints how many loaded).
- **Save:** `try/except/else/finally`. It writes to `students.json.tmp`
  first and then `os.replace()` swaps it in, so a crash mid-write can't
  corrupt the real file. `finally` always runs and deletes a leftover temp
  file. `os.makedirs(..., exist_ok=True)` creates `data/` if missing.
- **Paths via `os.path`:** `BASE_DIR` is built from `__file__`, so the
  program finds `data/` no matter which folder you run it from.
- **`with open(...)`:** closes the file automatically, even on errors.
- Students are held in a dict `{id: Student}`: lookup by ID is instant and
  duplicate IDs are impossible.

## reports.py
- Functions *return strings* instead of printing. The same string can be
  shown on screen **and** written to a file - write once, use twice.
- f-string formats like `{subject:<30}{score:>10.1f}` mean "left-align in 30
  characters" and "right-align in 10, one decimal place", which makes tidy
  columns.
- `save_report()` names the file with a timestamp (`report_20261110_...txt`)
  so reports never overwrite each other.

## main.py
- **Input helpers (`ask_*`)** use `while True` loops: keep asking until the
  input is valid, then `return`. This is where bad input is caught
  (try/except around `float()`), so the program never crashes on typos.
- **Menu dictionaries:** `{"1": ("Add student", add_student), ...}` map a
  choice to a label *and a function*. `run_menu()` is one generic loop that
  prints any menu and calls `options[choice][1](students)`. Adding a feature
  = adding one line. (Functions are values in Python, so they can be stored
  in a dictionary.)
- **Save after every change** so closing the window never loses data.
- **`if __name__ == "__main__":`** runs `main()` only when the file is
  executed directly, not when imported. Catching `KeyboardInterrupt`
  (Ctrl+C) lets the program exit politely.

---

## Brief requirement -> where it is
| Requirement | Location |
|-------------|----------|
| Variables, types, conversion | `float()` in `set_score`, `ask_score` |
| if/elif/else, loops | everywhere; `main()`, `grade_for` |
| Lists, tuples, dicts | list of boundaries; stats tuples; `scores`, `students` dicts |
| Functions | all files |
| Sorting | `results.py` |
| try/except/else/finally | `storage.py` (+ `main.py` helpers) |
| File handling | `storage.py`, `save_report` |
| Modules/packages | 5 `.py` files |
| OOP | `Student` class |
| Dates and times | `result_date`, `parse_dob`, report names |
| Standard library | `json`, `os`, `re`, `datetime` |
| Regex | student ID validation |

## Suggested Git commits (make these over the next days - the brief wants regular commits)
1. `Initial commit: project structure and README`
2. `Add Student class and validation`
3. `Add grading and statistics logic`
4. `Add JSON storage with error handling`
5. `Add report generation and export`
6. `Add menu interface in main.py`
7. `Test and polish; update documentation`

## Likely questions from your lecturer
- **Why `@property` for average?** It's computed on demand so it's never stale.
- **Why a temp file when saving?** Protects data if saving fails midway.
- **What does `finally` do?** Runs no matter what; used for cleanup.
- **Why does `results.py` not use `print`?** Keeps logic separate from display.
- **Difference between `sort()` and `sorted()`?** `sort` changes the list in
  place; `sorted` returns a new one.
- **Why a dict for students?** Fast lookup by ID and no duplicate IDs.
