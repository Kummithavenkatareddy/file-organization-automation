"""Data models and structures for file organization operations."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional


class OperationStatus(str, Enum):
    """Status of a file operation."""

    MOVED = "moved"
    SKIPPED = "skipped"
    DRY_RUN = "dry_run"
    ERROR = "error"


class FileCategory(str, Enum):
    """Supported file categories."""

    IMAGES = "Images"
    DOCUMENTS = "Documents"
    SPREADSHEETS = "Spreadsheets"
    PRESENTATIONS = "Presentations"
    AUDIO = "Audio"
    VIDEOS = "Videos"
    ARCHIVES = "Archives"
    CODE = "Code"
    OTHER = "Other"


@dataclass
class FileOperationResult:
    """Represents the result of a single file organization operation."""

    source: Path
    destination: Path
    category: str
    status: OperationStatus
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert operation result to a serializable dictionary."""
        return {
            "source": str(self.source),
            "destination": str(self.destination),
            "category": self.category,
            "status": self.status.value,
            "error": self.error,
        }


@dataclass
class OrganizerSummary:
    """Summary statistics for an organization run."""

    files_scanned: int = 0
    files_organized: int = 0
    files_skipped: int = 0
    errors: int = 0
    category_counts: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert summary statistics to a serializable dictionary."""
        return {
            "files_scanned": self.files_scanned,
            "files_organized": self.files_organized,
            "files_skipped": self.files_skipped,
            "errors": self.errors,
            "category_summary": dict(sorted(self.category_counts.items())),
        }


@dataclass
class OrganizeOptions:
    """Options for configuring a file organization run."""

    directory: Path
    dry_run: bool = False
    report_format: str = "table"
    output_path: Optional[Path] = None
    log_file: Optional[Path] = None
    recursive: bool = False
