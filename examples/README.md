# Examples and Walkthrough Scenarios

This directory contains practical scenarios demonstrating how to use `file-organization-automation` safely with temporary demonstration files.

> [!NOTE]
> All examples below use a temporary demonstration directory (`./demo_sandbox`) to ensure your personal files remain untouched.

---

## Setup Demo Directory

Create a sandbox folder populated with representative test files:

```bash
# Create demo folder
mkdir -p demo_sandbox

# Create mixed test files
touch demo_sandbox/vacation.jpg
touch demo_sandbox/budget.xlsx
touch demo_sandbox/invoice.pdf
touch demo_sandbox/invoice.pdf    # Duplicate test
touch demo_sandbox/script.py
touch demo_sandbox/backup.zip
touch demo_sandbox/notes.txt
touch demo_sandbox/unknown.dat
```

---

## Scenario 1: Preview Operations with Dry-Run Mode

Run the tool with `--dry-run` to inspect what would happen without altering any files:

```bash
python -m file_organizer --directory ./demo_sandbox --dry-run
```

**Expected Output:**

```
==================================================================
                   FILE ORGANIZATION REPORT                       
==================================================================
Files Scanned   : 7
Files Organized : 7
Files Skipped   : 0
Errors          : 0
------------------------------------------------------------------
Category Breakdown:
  - Archives       : 1
  - Code           : 1
  - Documents      : 2
  - Images         : 1
  - Other          : 1
  - Spreadsheets   : 1
------------------------------------------------------------------
Detailed Operations:
Category      | Status   | Filename                  | Destination
------------------------------------------------------------------
Archives      | dry_run  | backup.zip                | demo_sandbox/Archives/backup.zip
Spreadsheets  | dry_run  | budget.xlsx               | demo_sandbox/Spreadsheets/budget.xlsx
Documents     | dry_run  | invoice.pdf               | demo_sandbox/Documents/invoice.pdf
Documents     | dry_run  | notes.txt                 | demo_sandbox/Documents/notes.txt
Code          | dry_run  | script.py                 | demo_sandbox/Code/script.py
Other         | dry_run  | unknown.dat               | demo_sandbox/Other/unknown.dat
Images        | dry_run  | vacation.jpg              | demo_sandbox/Images/vacation.jpg
==================================================================
```

---

## Scenario 2: Execute File Organization & Save JSON Report

Execute actual file organization and write a detailed audit log in JSON format:

```bash
python -m file_organizer --directory ./demo_sandbox --report json --output ./demo_sandbox/reports/run_report.json
```

**Resulting Directory Structure:**

```
demo_sandbox/
├── Archives/
│   └── backup.zip
├── Code/
│   └── script.py
├── Documents/
│   ├── invoice.pdf
│   └── notes.txt
├── Images/
│   └── vacation.jpg
├── Other/
│   └── unknown.dat
├── Spreadsheets/
│   └── budget.xlsx
└── reports/
    └── run_report.json
```

---

## Scenario 3: Duplicate Handling Demonstration

If you place another `invoice.pdf` into `./demo_sandbox` and run organization again:

```bash
touch demo_sandbox/invoice.pdf
python -m file_organizer --directory ./demo_sandbox
```

The tool detects that `Documents/invoice.pdf` already exists and moves the file to:

```
demo_sandbox/Documents/invoice (1).pdf
```

Your original file is preserved completely.

---

## Cleanup Sandbox

Remove the demo directory after testing:

```bash
rm -rf demo_sandbox
```
