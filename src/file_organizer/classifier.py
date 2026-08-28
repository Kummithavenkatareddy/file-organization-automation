"""File classification module mapping extensions to category names."""

from pathlib import Path
from typing import Dict, Optional, Set

from file_organizer.models import FileCategory

# Default extension mappings for file categories
DEFAULT_CATEGORY_MAPPINGS: Dict[str, Set[str]] = {
    FileCategory.IMAGES.value: {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
    },
    FileCategory.DOCUMENTS.value: {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".rtf",
        ".odt",
    },
    FileCategory.SPREADSHEETS.value: {
        ".xls",
        ".xlsx",
        ".csv",
        ".ods",
    },
    FileCategory.PRESENTATIONS.value: {
        ".ppt",
        ".pptx",
        ".odp",
    },
    FileCategory.AUDIO.value: {
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".ogg",
    },
    FileCategory.VIDEOS.value: {
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".wmv",
        ".webm",
    },
    FileCategory.ARCHIVES.value: {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
    },
    FileCategory.CODE.value: {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".css",
        ".html",
        ".json",
        ".xml",
        ".sql",
        ".sh",
        ".ps1",
    },
}


class FileClassifier:
    """Classifies files into categories based on their extension."""

    def __init__(self, custom_mappings: Optional[Dict[str, Set[str]]] = None):
        """Initialize the classifier with default or custom extension mappings.

        :param custom_mappings: Optional dictionary mapping category names to sets of file extensions (e.g. {".png"}).
        """
        self.extension_map: Dict[str, str] = {}
        mappings = custom_mappings if custom_mappings is not None else DEFAULT_CATEGORY_MAPPINGS

        for category, extensions in mappings.items():
            for ext in extensions:
                normalized_ext = ext.lower() if ext.startswith(".") else f".{ext.lower()}"
                self.extension_map[normalized_ext] = category

    def classify(self, file_path: Path) -> str:
        """Determine the category of a given file path based on its extension.

        :param file_path: Path object representing the file to classify.
        :return: Category name string (e.g. 'Images', 'Documents', or 'Other').
        """
        if not file_path.suffix:
            return FileCategory.OTHER.value

        # Handle compound extensions like .tar.gz if full name ends with it
        file_name_lower = file_path.name.lower()
        for ext, category in self.extension_map.items():
            if file_name_lower.endswith(ext) and ext.count(".") > 1:
                return category

        ext = file_path.suffix.lower()
        return self.extension_map.get(ext, FileCategory.OTHER.value)


def classify_file(file_path: Path) -> str:
    """Helper function to classify a single file using default mappings.

    :param file_path: Path to classify.
    :return: Category name string.
    """
    classifier = FileClassifier()
    return classifier.classify(file_path)
