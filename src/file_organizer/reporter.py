"""Reporter module for generating execution summaries in Table, JSON, and CSV formats."""

import csv
import io
import json
from pathlib import Path
from typing import List, Optional

from file_organizer.models import FileOperationResult, OrganizerSummary


class ReportGenerator:
    """Generates structured operation reports in various output formats."""

    @staticmethod
    def generate_table(results: List[FileOperationResult], summary: OrganizerSummary) -> str:
        """Generate a formatted human-readable ASCII terminal report.

        :param results: List of operation results.
        :param summary: Summary statistics object.
        :return: Formatted text table.
        """
        lines = [
            "==================================================================",
            "                   FILE ORGANIZATION REPORT                       ",
            "==================================================================",
            f"Files Scanned   : {summary.files_scanned}",
            f"Files Organized : {summary.files_organized}",
            f"Files Skipped   : {summary.files_skipped}",
            f"Errors          : {summary.errors}",
            "------------------------------------------------------------------",
            "Category Breakdown:",
        ]

        if summary.category_counts:
            for cat, count in sorted(summary.category_counts.items()):
                lines.append(f"  - {cat:<15}: {count}")
        else:
            lines.append("  (No files organized)")

        lines.extend([
            "------------------------------------------------------------------",
            "Detailed Operations:",
            f"{'Category':<13} | {'Status':<8} | {'Filename':<25} | {'Destination'}",
            "-" * 66,
        ])

        if not results:
            lines.append("  (No operations performed)")
        else:
            for res in results:
                src_name = res.source.name
                dest_str = str(res.destination)
                err = f" (Error: {res.error})" if res.error else ""
                lines.append(
                    f"{res.category:<13} | {res.status.value:<8} | {src_name:<25} | {dest_str}{err}"
                )

        lines.append("==================================================================")
        return "\n".join(lines)

    @staticmethod
    def generate_json(results: List[FileOperationResult], summary: OrganizerSummary) -> str:
        """Generate a structured JSON report string.

        :param results: List of operation results.
        :param summary: Summary statistics object.
        :return: Pretty-printed JSON string.
        """
        data = {
            "summary": summary.to_dict(),
            "operations": [res.to_dict() for res in results],
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def generate_csv(results: List[FileOperationResult], summary: OrganizerSummary) -> str:
        """Generate a CSV format report string.

        :param results: List of operation results.
        :param summary: Summary statistics object.
        :return: CSV formatted string.
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["source", "destination", "category", "status", "error"])

        for res in results:
            writer.writerow([
                str(res.source),
                str(res.destination),
                res.category,
                res.status.value,
                res.error or "",
            ])

        return output.getvalue()

    def generate(
        self,
        results: List[FileOperationResult],
        summary: OrganizerSummary,
        format_type: str = "table",
    ) -> str:
        """Generate report string based on specified format type ('table', 'json', 'csv')."""
        fmt = format_type.lower()
        if fmt == "table":
            return self.generate_table(results, summary)
        elif fmt == "json":
            return self.generate_json(results, summary)
        elif fmt == "csv":
            return self.generate_csv(results, summary)
        else:
            raise ValueError(f"Unsupported report format: '{format_type}'. Supported: table, json, csv")

    def save_report(
        self,
        report_content: str,
        output_path: Path,
    ) -> None:
        """Save generated report content to a destination file.

        :param report_content: The text/json/csv report string.
        :param output_path: Destination path where report file should be saved.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_content, encoding="utf-8")
