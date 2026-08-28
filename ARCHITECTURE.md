# System Architecture Document

This document provides a comprehensive overview of the design, modular architecture, data flows, error handling strategy, and component responsibilities for the `file-organization-automation` project.

---

## 1. High-Level Architecture

The project follows a clean, single-responsibility, layered architecture designed with standard Python components:

```
[ Command Line Interface (cli.py) ]
               │
               ▼
[ Logging Setup (logger.py) ]
               │
               ▼
[ File Organizer Engine (organizer.py) ]
     │                         │
     ▼                         ▼
[ File Classifier ]   [ Data Models (models.py) ]
 (classifier.py)               │
                               ▼
                    [ Report Generator ]
                      (reporter.py)
                               │
                               ▼
                     [ Console / Disk Output ]
```

---

## 2. Component Responsibilities

### `models.py`
- Defines strongly-typed dataclasses (`FileOperationResult`, `OrganizerSummary`, `OrganizeOptions`) and Enums (`OperationStatus`, `FileCategory`).
- Enforces data validation and uniform serialization via `to_dict()` methods.

### `classifier.py`
- Encapsulates extension-to-category mapping.
- Normalizes file extension inputs (lowercasing, handling files without extensions, compound extensions like `.tar.gz`).
- Decoupled from filesystem state to allow independent testing.

### `organizer.py`
- Scans target directories using `pathlib.Path`.
- Filters out directories, symlinks, and existing category subfolders.
- Resolves non-colliding destination paths deterministically with counter suffixes.
- Executes safe `shutil.move` operations or simulates planned movements in dry-run mode.
- Aggregates execution results into `OrganizerSummary`.

### `reporter.py`
- Transforms execution results and summary statistics into presentation formats:
  - `table`: ASCII formatted text table for terminal display.
  - `json`: Machine-readable JSON structured object.
  - `csv`: RFC-4180 compliant CSV formatting for spreadsheet analysis.

### `logger.py`
- Configures Python standard `logging` handlers for stream (console) and file output.
- Eliminates raw `print` statements from operational code.

### `cli.py`
- Parses command-line flags and parameters via `argparse`.
- Validates user input paths and parameters.
- Catches runtime exceptions gracefully to present clean error messages without raw stack traces.

---

## 3. Key Workflows & Data Flows

### A. Classification Flow
1. `organizer` passes file `Path` to `FileClassifier.classify(path)`.
2. Classifier inspects `path.name` for compound extensions (e.g. `.tar.gz`).
3. If no match, classifier inspects lowercased `path.suffix`.
4. Returns category name string (or `Other` if unmapped/missing).

### B. File Movement & Conflict Resolution Flow
1. Target category folder `target_dir / category` path is constructed.
2. `organizer._resolve_unique_destination` checks if `dest_dir / filename` exists or has been claimed in the current run.
3. If path collision detected, appends numeric counter: `filename (1).ext`, `filename (2).ext`.
4. In normal mode: target category directory is created with `mkdir(parents=True, exist_ok=True)` and file is moved via `shutil.move()`.
5. In dry-run mode: filesystem write operations are skipped; destination is recorded with status `DRY_RUN`.

### C. Reporting Flow
1. `organizer` returns `List[FileOperationResult]` and `OrganizerSummary`.
2. `ReportGenerator.generate(results, summary, format_type)` formats the data string.
3. Printed to standard output and optionally written to `--output` file.

---

## 4. Error-Handling Strategy

- **Granular Exception Trapping**: Individual file move failures are caught and recorded as `OperationStatus.ERROR` with error messages attached to `FileOperationResult`. One failing file move does not abort the processing of remaining files.
- **CLI Input Validation**: Invalid target directories or unwriteable output paths return non-zero exit codes (1 or 2) with user-friendly diagnostics.
- **Traceback Suppression**: Unhandled stack traces are suppressed during normal user CLI execution.

---

## 5. Extension Points

- **Custom Extension Mappings**: `FileClassifier` accepts custom dictionary mappings to support custom file types or categories.
- **New Report Formats**: Add format generator methods in `ReportGenerator` and update choices in `cli.py`.
