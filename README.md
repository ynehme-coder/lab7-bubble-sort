# Bubble Sort Lab

A small Python lab project that implements bubble sort and validates behavior with basic `pytest` tests.

## Project Overview

- `main.py`: Contains the `bubble_sort(values: list[int]) -> list[int]` function and a small runnable example.
- `test_main.py`: Contains 5 basic tests using `pytest`.
- `REPORT.md`: Project report/documentation notes.
- `JOURNAL.md`: Chronological interaction log.

## Requirements

- Python 3.13+ (project currently uses a local virtual environment in `.venv`)
- `pytest`

## Setup

1. Create and activate a virtual environment (optional if already using `.venv`).
2. Install test dependencies:

```powershell
pip install pytest
```

## Run the App

```powershell
python main.py
```

This prints the sorted result of the sample `numbers` list from `main.py`.

## Run Tests

```powershell
pytest -q
```

Expected result: 5 tests passing.

## Notes

- `bubble_sort` returns a sorted copy and does not modify the original input list.
- The script output in `main.py` is protected by `if __name__ == "__main__":` so imports stay test-friendly.
