"""Module responsible for scanning directories and moving files cleanly and safely."""

import logging
from pathlib import Path
import shutil
from typing import List, Optional, Set, Tuple

from file_organizer.classifier import FileClassifier
from file_organizer.models import (
    FileCategory,
    FileOperationResult,
    OperationStatus,
    OrganizerSummary,
    OrganizeOptions,
)

logger = logging.getLogger(__name__)


class FileOrganizer:
    """Orchestrates file organization within a target directory."""

    def __init__(
        self,
        options: OrganizeOptions,
        classifier: Optional[FileClassifier] = None,
    ):
        """Initialize the organizer with options and optional custom classifier."""
        self.options = options
        self.target_dir = options.directory.resolve()
        self.dry_run = options.dry_run
        self.recursive = options.recursive
        self.classifier = classifier or FileClassifier()

        # Known category folder names to avoid re-scanning organized subdirectories
        self.category_names: Set[str] = {c.value for c in FileCategory}

        self.log_file: Optional[Path] = options.log_file.resolve() if options.log_file else None
        self.output_path: Optional[Path] = options.output_path.resolve() if options.output_path else None

    def _should_skip_path(self, path: Path) -> bool:
        """Check if a path should be skipped during scanning."""
        if path.is_symlink():
            logger.debug("Skipping symlink: %s", path)
            return True

        if path.is_dir():
            return True

        resolved_item = path.resolve()
        if self.log_file and resolved_item == self.log_file:
            logger.debug("Skipping active log file: %s", path)
            return True

        if self.output_path and resolved_item == self.output_path:
            logger.debug("Skipping active report output file: %s", path)
            return True

        # Check if the file is inside one of the category directories
        try:
            rel_path = path.relative_to(self.target_dir)
            top_level = rel_path.parts[0] if rel_path.parts else ""
            if top_level in self.category_names:
                logger.debug("Skipping file inside category directory '%s': %s", top_level, path)
                return True
        except ValueError:
            pass

        return False

    def _scan_files(self) -> List[Path]:
        """Scan the target directory for candidate files."""
        if not self.target_dir.exists():
            raise FileNotFoundError(f"Target directory does not exist: {self.target_dir}")
        if not self.target_dir.is_dir():
            raise NotADirectoryError(f"Target path is not a directory: {self.target_dir}")

        files: List[Path] = []
        if self.recursive:
            iterator = self.target_dir.rglob("*")
        else:
            iterator = self.target_dir.iterdir()

        for item in iterator:
            if not self._should_skip_path(item):
                files.append(item)

        return sorted(files)

    def _resolve_unique_destination(self, dest_dir: Path, file_name: str, claimed_paths: Set[Path]) -> Path:
        """Generate a non-colliding destination path by appending numeric suffixes if necessary.

        Never overwrites existing files or paths claimed in the current run.
        """
        initial_dest = dest_dir / file_name
        if not initial_dest.exists() and initial_dest not in claimed_paths:
            return initial_dest

        # Deconstruct filename into stem and extension
        p = Path(file_name)
        stem = p.stem
        suffix = p.suffix

        counter = 1
        while True:
            if suffix:
                candidate_name = f"{stem} ({counter}){suffix}"
            else:
                candidate_name = f"{file_name} ({counter})"

            candidate_path = dest_dir / candidate_name
            if not candidate_path.exists() and candidate_path not in claimed_paths:
                return candidate_path

            counter += 1

    def organize(self) -> Tuple[List[FileOperationResult], OrganizerSummary]:
        """Perform the file organization workflow.

        :return: Tuple containing a list of operation results and a summary object.
        """
        files_to_process = self._scan_files()
        results: List[FileOperationResult] = []
        summary = OrganizerSummary()
        summary.files_scanned = len(files_to_process)

        claimed_destinations: Set[Path] = set()

        logger.info(
            "Found %d candidate files in '%s' (dry_run=%s, recursive=%s)",
            summary.files_scanned,
            self.target_dir,
            self.dry_run,
            self.recursive,
        )

        for file_path in files_to_process:
            category = self.classifier.classify(file_path)
            dest_dir = self.target_dir / category
            dest_path = self._resolve_unique_destination(dest_dir, file_path.name, claimed_destinations)

            if self.dry_run:
                claimed_destinations.add(dest_path)
                result = FileOperationResult(
                    source=file_path,
                    destination=dest_path,
                    category=category,
                    status=OperationStatus.DRY_RUN,
                )
                results.append(result)
                summary.files_organized += 1
                summary.category_counts[category] = summary.category_counts.get(category, 0) + 1
                logger.info("[DRY-RUN] Would move '%s' -> '%s'", file_path, dest_path)
                continue

            # Real movement logic
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest_path))
                claimed_destinations.add(dest_path)

                result = FileOperationResult(
                    source=file_path,
                    destination=dest_path,
                    category=category,
                    status=OperationStatus.MOVED,
                )
                results.append(result)
                summary.files_organized += 1
                summary.category_counts[category] = summary.category_counts.get(category, 0) + 1
                logger.info("Moved '%s' -> '%s'", file_path, dest_path)

            except Exception as exc:
                err_msg = str(exc)
                logger.error("Failed to move '%s' to '%s': %s", file_path, dest_path, err_msg)
                result = FileOperationResult(
                    source=file_path,
                    destination=dest_path,
                    category=category,
                    status=OperationStatus.ERROR,
                    error=err_msg,
                )
                results.append(result)
                summary.errors += 1

        return results, summary
