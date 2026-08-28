"""Unit tests for FileClassifier module."""

from pathlib import Path
from file_organizer.classifier import FileClassifier, classify_file
from file_organizer.models import FileCategory


def test_standard_extension_classification():
    classifier = FileClassifier()

    assert classifier.classify(Path("photo.jpg")) == FileCategory.IMAGES.value
    assert classifier.classify(Path("document.pdf")) == FileCategory.DOCUMENTS.value
    assert classifier.classify(Path("sheet.csv")) == FileCategory.SPREADSHEETS.value
    assert classifier.classify(Path("deck.pptx")) == FileCategory.PRESENTATIONS.value
    assert classifier.classify(Path("song.mp3")) == FileCategory.AUDIO.value
    assert classifier.classify(Path("movie.mp4")) == FileCategory.VIDEOS.value
    assert classifier.classify(Path("archive.zip")) == FileCategory.ARCHIVES.value
    assert classifier.classify(Path("script.py")) == FileCategory.CODE.value


def test_case_insensitive_classification():
    classifier = FileClassifier()

    assert classifier.classify(Path("IMAGE.PNG")) == FileCategory.IMAGES.value
    assert classifier.classify(Path("Doc.Txt")) == FileCategory.DOCUMENTS.value
    assert classifier.classify(Path("Data.XLSX")) == FileCategory.SPREADSHEETS.value
    assert classifier.classify(Path("App.Py")) == FileCategory.CODE.value


def test_unknown_extension_classification():
    classifier = FileClassifier()

    assert classifier.classify(Path("file.xyz")) == FileCategory.OTHER.value
    assert classifier.classify(Path("data.dat")) == FileCategory.OTHER.value
    assert classifier.classify(Path("bin.custom")) == FileCategory.OTHER.value


def test_no_extension_classification():
    classifier = FileClassifier()

    assert classifier.classify(Path("Dockerfile")) == FileCategory.OTHER.value
    assert classifier.classify(Path("README")) == FileCategory.OTHER.value
    assert classifier.classify(Path("Makefile")) == FileCategory.OTHER.value


def test_compound_extension_classification():
    classifier = FileClassifier()

    assert classifier.classify(Path("archive.tar.gz")) == FileCategory.ARCHIVES.value


def test_custom_mappings():
    custom = {
        "Ebooks": {".epub", ".mobi"},
        "Models": {".onnx", ".pt"},
    }
    classifier = FileClassifier(custom_mappings=custom)

    assert classifier.classify(Path("book.epub")) == "Ebooks"
    assert classifier.classify(Path("model.onnx")) == "Models"
    assert classifier.classify(Path("image.png")) == FileCategory.OTHER.value


def test_classify_file_helper():
    assert classify_file(Path("test.png")) == FileCategory.IMAGES.value
    assert classify_file(Path("unknown.foo")) == FileCategory.OTHER.value
