# Developer Guide

This guide details environment setup, running tests, code style guidelines, and steps for adding new features to `file-organization-automation`.

---

## 1. Development Setup

### Prerequisites
- Python 3.8 or higher installed on system.
- Git.

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/example/file-organization-automation.git
   cd file-organization-automation
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install project in editable mode with development dependencies:
   ```bash
   python -m pip install -e ".[dev]"
   ```

---

## 2. Running Application & Tests

### Running CLI Module
```bash
python -m file_organizer --directory ./demo_folder --dry-run
```

### Running Test Suite
```bash
python -m pytest -v
```

---

## 3. Extending Functionality

### Adding a New File Category

To add a new category (e.g. `Ebooks`):

1. Add the category constant in `src/file_organizer/models.py`:
   ```python
   class FileCategory(str, Enum):
       ...
       EBOOKS = "Ebooks"
   ```

2. Add mapped extensions in `src/file_organizer/classifier.py`:
   ```python
   DEFAULT_CATEGORY_MAPPINGS = {
       ...
       FileCategory.EBOOKS.value: {".epub", ".mobi", ".azw3"},
   }
   ```

3. Add corresponding unit tests in `tests/test_classifier.py`.

---

### Adding a New Report Format

To add a new format (e.g. `HTML`):

1. Implement format builder method in `src/file_organizer/reporter.py`:
   ```python
   @staticmethod
   def generate_html(results: List[FileOperationResult], summary: OrganizerSummary) -> str:
       # Generate HTML string
       ...
   ```

2. Update `generate()` dispatcher method in `ReportGenerator`.
3. Add choice to `cli.py` `--report` argument parser:
   ```python
   choices=["table", "json", "csv", "html"]
   ```

---

## 4. Code Quality & Standards

- **PEP 8 Compliance**: Follow standard Python formatting conventions.
- **Path handling**: Always use `pathlib.Path` instead of string manipulation.
- **No side-effects in dry-run**: Ensure any new filesystem feature respects `options.dry_run`.
