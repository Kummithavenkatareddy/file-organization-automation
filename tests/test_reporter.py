"""Unit tests for ReportGenerator module."""

import csv
import json
from pathlib import Path
import pytest

from file_organizer.models import (
    FileCategory,
    FileOperationResult,
    OperationStatus,
    OrganizerSummary,
)
from file_organizer.reporter import ReportGenerator


@pytest.fixture
def sample_data(tmp_path: Path):
    src = tmp_path / "photo.jpg"
    dest = tmp_path / "Images" / "photo.jpg"
    results = [
        FileOperationResult(
            source=src,
            destination=dest,
            category=FileCategory.IMAGES.value,
            status=OperationStatus.MOVED,
        )
    ]
    summary = OrganizerSummary(
        files_scanned=1,
        files_organized=1,
        files_skipped=0,
        errors=0,
        category_counts={FileCategory.IMAGES.value: 1},
    )
    return results, summary


def test_table_report_generation(sample_data):
    results, summary = sample_data
    reporter = ReportGenerator()
    table_text = reporter.generate(results, summary, format_type="table")

    assert "FILE ORGANIZATION REPORT" in table_text
    assert "Files Scanned   : 1" in table_text
    assert "Images" in table_text
    assert "photo.jpg" in table_text


def test_json_report_generation(sample_data):
    results, summary = sample_data
    reporter = ReportGenerator()
    json_text = reporter.generate(results, summary, format_type="json")

    data = json.loads(json_text)
    assert "summary" in data
    assert "operations" in data
    assert data["summary"]["files_scanned"] == 1
    assert data["summary"]["files_organized"] == 1
    assert data["summary"]["category_summary"]["Images"] == 1
    assert len(data["operations"]) == 1
    assert data["operations"][0]["category"] == "Images"
    assert data["operations"][0]["status"] == "moved"


def test_csv_report_generation(sample_data):
    results, summary = sample_data
    reporter = ReportGenerator()
    csv_text = reporter.generate(results, summary, format_type="csv")

    rows = list(csv.reader(csv_text.strip().splitlines()))
    assert len(rows) == 2  # Header + 1 data row
    assert rows[0] == ["source", "destination", "category", "status", "error"]
    assert rows[1][2] == "Images"
    assert rows[1][3] == "moved"


def test_invalid_format_raises_error(sample_data):
    results, summary = sample_data
    reporter = ReportGenerator()

    with pytest.raises(ValueError, match="Unsupported report format"):
        reporter.generate(results, summary, format_type="invalid_format")


def test_save_report_to_file(sample_data, tmp_path: Path):
    results, summary = sample_data
    reporter = ReportGenerator()
    report_content = reporter.generate(results, summary, format_type="json")

    output_file = tmp_path / "reports" / "summary.json"
    reporter.save_report(report_content, output_file)

    assert output_file.exists()
    assert json.loads(output_file.read_text())["summary"]["files_scanned"] == 1
