"""Command-Line Interface (CLI) entry point for File Organization Automation tool."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from file_organizer import __version__
from file_organizer.logger import setup_logging
from file_organizer.models import OrganizeOptions
from file_organizer.organizer import FileOrganizer
from file_organizer.reporter import ReportGenerator


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Automate organizing files in a directory by file extension into category subfolders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--directory",
        "-d",
        type=Path,
        required=True,
        help="Target directory to organize.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview operations without moving files or creating directories.",
    )
    parser.add_argument(
        "--report",
        "-r",
        choices=["table", "json", "csv"],
        default="table",
        help="Summary report format (table, json, csv). Default: table.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Optional destination path to save the generated report.",
    )
    parser.add_argument(
        "--log-file",
        "-l",
        type=Path,
        help="Optional file path to write detailed operational log messages.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan subdirectories (skips generated category folders).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose DEBUG logging.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Display the application version and exit.",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main execution function for the CLI.

    :param argv: Command-line arguments list. If None, uses sys.argv[1:].
    :return: Exit code integer (0 for success, non-zero for error).
    """
    parser = build_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2

    # Configure logging
    logger = setup_logging(log_file=args.log_file, verbose=args.verbose)

    # Validate directory
    target_dir: Path = args.directory
    if not target_dir.exists():
        logger.error("Error: Target directory does not exist: %s", target_dir)
        return 1

    if not target_dir.is_dir():
        logger.error("Error: Target path is not a directory: %s", target_dir)
        return 1

    # Validate report output path parent directory if specified
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.error("Error: Cannot write report to output path '%s': %s", args.output, exc)
            return 1

    options = OrganizeOptions(
        directory=target_dir,
        dry_run=args.dry_run,
        report_format=args.report,
        output_path=args.output,
        log_file=args.log_file,
        recursive=args.recursive,
    )

    try:
        organizer = FileOrganizer(options)
        results, summary = organizer.organize()

        # Report generation
        reporter = ReportGenerator()
        report_text = reporter.generate(results, summary, format_type=args.report)

        # Output report to console
        print(report_text)

        # Output report to file if requested
        if args.output:
            reporter.save_report(report_text, args.output)
            logger.info("Saved report to '%s'", args.output)

        return 0

    except Exception as exc:
        logger.error("Execution failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
