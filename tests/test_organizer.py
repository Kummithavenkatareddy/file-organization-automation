"""Unit tests for FileOrganizer module."""

from pathlib import Path
import pytest

from file_organizer.models import OperationStatus, OrganizeOptions
from file_organizer.organizer import FileOrganizer


def test_organize_basic_success(tmp_path: Path):
    # Create test files
    img = tmp_path / "pic.png"
    doc = tmp_path / "notes.txt"
    code = tmp_path / "app.py"
    unknown = tmp_path / "random.xyz"

    img.write_text("image content")
    doc.write_text("doc content")
    code.write_text("code content")
    unknown.write_text("xyz content")

    options = OrganizeOptions(directory=tmp_path)
    organizer = FileOrganizer(options)

    results, summary = organizer.organize()

    assert summary.files_scanned == 4
    assert summary.files_organized == 4
    assert summary.errors == 0

    # Check that category folders were created and files moved
    assert (tmp_path / "Images" / "pic.png").exists()
    assert (tmp_path / "Documents" / "notes.txt").exists()
    assert (tmp_path / "Code" / "app.py").exists()
    assert (tmp_path / "Other" / "random.xyz").exists()

    # Check original files no longer exist at root
    assert not img.exists()
    assert not doc.exists()
    assert not code.exists()
    assert not unknown.exists()


def test_dry_run_mode_does_not_modify_filesystem(tmp_path: Path):
    file1 = tmp_path / "test.jpg"
    file2 = tmp_path / "data.csv"
    file1.write_text("jpg")
    file2.write_text("csv")

    options = OrganizeOptions(directory=tmp_path, dry_run=True)
    organizer = FileOrganizer(options)

    results, summary = organizer.organize()

    assert summary.files_scanned == 2
    assert summary.files_organized == 2
    assert all(r.status == OperationStatus.DRY_RUN for r in results)

    # Verify original files still exist
    assert file1.exists()
    assert file2.exists()

    # Verify category folders were NOT created
    assert not (tmp_path / "Images").exists()
    assert not (tmp_path / "Spreadsheets").exists()


def test_duplicate_filename_handling(tmp_path: Path):
    # Create category dir with existing file
    docs_dir = tmp_path / "Documents"
    docs_dir.mkdir()
    existing_doc = docs_dir / "report.pdf"
    existing_doc.write_text("existing content")

    # Create root file with same name
    new_doc = tmp_path / "report.pdf"
    new_doc.write_text("new content")

    options = OrganizeOptions(directory=tmp_path)
    organizer = FileOrganizer(options)

    results, summary = organizer.organize()

    assert summary.files_organized == 1

    # Verify existing file was not overwritten
    assert existing_doc.read_text() == "existing content"

    # Verify new file was renamed to report (1).pdf
    renamed_doc = docs_dir / "report (1).pdf"
    assert renamed_doc.exists()
    assert renamed_doc.read_text() == "new content"


def test_multiple_duplicate_collisions(tmp_path: Path):
    docs_dir = tmp_path / "Documents"
    docs_dir.mkdir()
    (docs_dir / "data.txt").write_text("v0")
    (docs_dir / "data (1).txt").write_text("v1")

    (tmp_path / "data.txt").write_text("v2")

    options = OrganizeOptions(directory=tmp_path)
    organizer = FileOrganizer(options)

    results, summary = organizer.organize()

    target_file = docs_dir / "data (2).txt"
    assert target_file.exists()
    assert target_file.read_text() == "v2"


def test_missing_directory_raises_error(tmp_path: Path):
    non_existent = tmp_path / "does_not_exist"
    options = OrganizeOptions(directory=non_existent)
    organizer = FileOrganizer(options)

    with pytest.raises(FileNotFoundError):
        organizer.organize()


def test_not_a_directory_raises_error(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")

    options = OrganizeOptions(directory=file_path)
    organizer = FileOrganizer(options)

    with pytest.raises(NotADirectoryError):
        organizer.organize()


def test_recursive_mode_skips_category_dirs(tmp_path: Path):
    sub_dir = tmp_path / "subdir"
    sub_dir.mkdir()
    nested_file = sub_dir / "picture.png"
    nested_file.write_text("png")

    options = OrganizeOptions(directory=tmp_path, recursive=True)
    organizer = FileOrganizer(options)

    results, summary = organizer.organize()

    assert summary.files_scanned == 1
    assert (tmp_path / "Images" / "picture.png").exists()
    assert not nested_file.exists()
