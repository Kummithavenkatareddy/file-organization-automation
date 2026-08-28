# File Organization & Reporting Automation Tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A reusable, production-quality Python command-line utility that automates file organization from cluttered directories into categorized subfolders based on file extensions, complete with dry-run previews, conflict-free duplicate handling, logging, and multi-format operation reporting (Table, JSON, CSV).

---

## Problem Statement

Computer users and systems frequently accumulate hundreds of unorganized files—downloads, exports, media assets, documents, and code snippets—in a single directory. Manually sifting through files, creating subdirectories, and moving files one by one is repetitive, error-prone, and time-consuming.

## Automating the Task

`file-organization-automation` automates this repetitive file management task:
- Scans target directories automatically.
- Classifies files by extension into logical categories (`Images`, `Documents`, `Spreadsheets`, `Presentations`, `Audio`, `Videos`, `Archives`, `Code`, `Other`).
- Safely creates destination subdirectories on demand.
- Moves files without risk of overwriting existing data.
- Generates transparent operation reports for auditing.

---

## Features

- **Automated Classification**: Maps file extensions to standard categories using customizable extension rules.
- **Safety First**: **Never overwrites** existing files. Resolves filename collisions deterministically by appending counter suffixes (`report (1).pdf`).
- **Dry-Run Mode**: Preview planned directory changes without modifying disk contents.
- **Multi-Format Reporting**: Export reports in human-readable ASCII tables, structured JSON, or CSV formats.
- **Operational Logging**: Full support for file and console logging with configurable verbosity levels (`DEBUG`/`INFO`).
- **Recursive Scan**: Option to organize nested subdirectories while ignoring previously generated category directories.
- **Standard Library Core**: Built strictly with Python's standard library (`pathlib`, `dataclasses`, `enum`, `argparse`, `shutil`, `logging`).

---

## Technology Stack

- **Language**: Python 3.8+
- **Standard Library Modules**: `pathlib`, `argparse`, `logging`, `dataclasses`, `enum`, `json`, `csv`, `shutil`, `sys`
- **Testing Framework**: `pytest`

---

## Project Structure

```
file-organization-automation/
├── src/
│   └── file_organizer/
│       ├── __init__.py          # Package initialization & version
│       ├── __main__.py          # CLI module entry point (python -m file_organizer)
│       ├── cli.py               # Argument parsing & execution control
│       ├── classifier.py        # File extension classification logic
│       ├── organizer.py         # Directory scanning & file movement orchestrator
│       ├── reporter.py          # Summary report generation (Table, JSON, CSV)
│       ├── logger.py            # Console & file logging configuration
│       └── models.py            # Data structures, dataclasses, and enums
├── tests/
│   ├── __init__.py
│   ├── test_classifier.py     # Unit tests for classification logic
│   ├── test_organizer.py      # Unit tests for organization & safety
│   ├── test_reporter.py       # Unit tests for report formatting
│   └── test_cli.py            # Integration tests for command-line options
├── examples/
│   └── README.md                # Demonstration workflows and examples
├── README.md                    # Project documentation
├── ARCHITECTURE.md              # Technical architecture details
├── DEVELOPMENT.md               # Developer setup & extension guide
├── pyproject.toml               # Project build & packaging specification
├── .gitignore                   # Version control ignore list
└── LICENSE                      # Open-source MIT license
```

---

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/example/file-organization-automation.git
cd file-organization-automation

# Install package with development dependencies
python -m pip install -e ".[dev]"
```

Verify installation:

```bash
python -m file_organizer --help
```

---

## CLI Usage

### Basic Usage

Organize files in a target directory:

```bash
python -m file_organizer --directory ./my_downloads
```

Or using the installed binary script:

```bash
file-organizer -d ./my_downloads
```

### Dry-Run Mode (Preview Only)

To preview what files will be organized without creating folders or moving files:

```bash
python -m file_organizer --directory ./my_downloads --dry-run
```

### Generating Reports

Generate a JSON or CSV report and save it to a file:

```bash
# Export JSON report
python -m file_organizer -d ./my_downloads --report json --output ./reports/summary.json

# Export CSV report
python -m file_organizer -d ./my_downloads --report csv --output ./reports/summary.csv
```

### Enable Logging & Recursive Scanning

```bash
python -m file_organizer --directory ./unorganized --recursive --log-file ./app.log --verbose
```

---

## Supported File Categories

| Category | Supported Extensions |
| :--- | :--- |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp` |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt` |
| **Spreadsheets** | `.xls`, `.xlsx`, `.csv`, `.ods` |
| **Presentations** | `.ppt`, `.pptx`, `.odp` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg` |
| **Videos** | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.webm` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz` |
| **Code** | `.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.h`, `.css`, `.html`, `.json`, `.xml`, `.sql`, `.sh`, `.ps1` |
| **Other** | Any extension not listed above or files without extensions |

---

## Duplicate File Collision Handling

The tool guarantees that **existing destination files are never overwritten**.

If `report.pdf` already exists in `Documents/`, a new `report.pdf` will automatically be moved as:

```
Documents/report (1).pdf
```

Subsequent collisions increment the counter:

```
Documents/report (2).pdf
```

---

## Safety Behavior & Guarantees

1. **Non-Destructive**: Files are moved, never deleted or overwritten.
2. **File Integrity**: File contents are untouched; metadata is preserved by system moves.
3. **Category Directory Protection**: Automatically skips generated category folders (`Images`, `Documents`, etc.) to prevent recursive self-sorting loops.
4. **Symlink Safety**: Symlinks are logged and skipped by default to prevent accidental traversal out of the target directory.

---

## Sample Reports

### Table Report (Default)

```
==================================================================
                   FILE ORGANIZATION REPORT                       
==================================================================
Files Scanned   : 3
Files Organized : 3
Files Skipped   : 0
Errors          : 0
------------------------------------------------------------------
Category Breakdown:
  - Code           : 1
  - Documents      : 1
  - Images         : 1
------------------------------------------------------------------
Detailed Operations:
Category      | Status   | Filename                  | Destination
------------------------------------------------------------------
Documents     | moved    | contract.pdf              | /path/to/target/Documents/contract.pdf
Images        | moved    | screenshot.png            | /path/to/target/Images/screenshot.png
Code          | moved    | script.py                 | /path/to/target/Code/script.py
==================================================================
```

### JSON Report

```json
{
  "summary": {
    "files_scanned": 2,
    "files_organized": 2,
    "files_skipped": 0,
    "errors": 0,
    "category_summary": {
      "Documents": 1,
      "Images": 1
    }
  },
  "operations": [
    {
      "source": "/path/to/target/report.pdf",
      "destination": "/path/to/target/Documents/report.pdf",
      "category": "Documents",
      "status": "moved",
      "error": null
    },
    {
      "source": "/path/to/target/photo.jpg",
      "destination": "/path/to/target/Images/photo.jpg",
      "category": "Images",
      "status": "moved",
      "error": null
    }
  ]
}
```

---

## Testing

Run the full pytest suite:

```bash
python -m pytest -v
```

All 20+ unit and integration tests execute against isolated temporary directories (`tmp_path`).

---

## Limitations

- File classification is based on file extension matching, not magic MIME-type header inspection.
- Cloud storage sync folders (e.g. OneDrive, Dropbox) should sync completely before running to avoid file lock permissions during movement.

---

## Future Improvements

- Content-based MIME-type classification using standard `mimetypes` or magic bytes.
- Undo/rollback operation support using saved JSON run logs.
- Custom YAML configuration file support for user-defined categories.
