"""Integration tests for CLI entry point."""

from pathlib import Path
from file_organizer.cli import main


def test_cli_help():
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0


def test_cli_version():
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0


def test_cli_missing_directory():
    code = main([])
    assert code == 2


def test_cli_non_existent_directory(tmp_path: Path):
    non_existent = tmp_path / "missing_folder"
    code = main(["--directory", str(non_existent)])
    assert code == 1


def test_cli_directory_is_file(tmp_path: Path):
    file_path = tmp_path / "not_a_dir.txt"
    file_path.write_text("hello")

    code = main(["--directory", str(file_path)])
    assert code == 1


def test_cli_successful_run(tmp_path: Path):
    (tmp_path / "doc.pdf").write_text("pdf content")
    (tmp_path / "img.png").write_text("png content")

    code = main(["--directory", str(tmp_path)])
    assert code == 0

    assert (tmp_path / "Documents" / "doc.pdf").exists()
    assert (tmp_path / "Images" / "img.png").exists()


def test_cli_dry_run(tmp_path: Path):
    file_path = tmp_path / "script.py"
    file_path.write_text("print('hi')")

    code = main(["--directory", str(tmp_path), "--dry-run"])
    assert code == 0

    assert file_path.exists()
    assert not (tmp_path / "Code").exists()


def test_cli_report_output_file(tmp_path: Path):
    (tmp_path / "data.csv").write_text("1,2,3")
    report_file = tmp_path / "reports" / "output.json"

    code = main([
        "--directory", str(tmp_path),
        "--report", "json",
        "--output", str(report_file),
    ])
    assert code == 0
    assert report_file.exists()
    assert '"files_scanned": 1' in report_file.read_text()


def test_cli_log_file(tmp_path: Path):
    (tmp_path / "test.txt").write_text("test")
    log_file = tmp_path / "app.log"

    code = main([
        "--directory", str(tmp_path),
        "--log-file", str(log_file),
        "--verbose",
    ])
    assert code == 0
    assert log_file.exists()
    assert "Found 1 candidate files" in log_file.read_text()
