import pytest
from isic4kit import ISIC4Classifier


def test_init_default_language():
    """Test initialization with default language."""
    classifier = ISIC4Classifier()
    assert classifier.language == "en"
    assert len(classifier.sections) > 0


def test_init_custom_language():
    """Test initialization with custom language."""
    classifier = ISIC4Classifier(language="ar")
    assert classifier.language == "ar"
    assert len(classifier.sections) > 0


def test_init_invalid_language():
    """Test initialization with invalid language raises ValueError."""
    with pytest.raises(ValueError):
        ISIC4Classifier(language="invalid_language")


def test_load_data():
    """Test that _load_data populates sections."""
    classifier = ISIC4Classifier()
    assert len(classifier.sections) > 0
    section = classifier.sections[0]
    assert hasattr(section, "code")
    assert hasattr(section, "description")
    assert isinstance(section.code, str)
    assert isinstance(section.description, str)


@pytest.mark.parametrize("language", ["en", "ar"])
def test_supported_languages(language):
    """Test initialization with different supported languages."""
    classifier = ISIC4Classifier(language=language)
    assert classifier.language == language
    assert len(classifier.sections) > 0


def test_data_consistency():
    """Test that loaded data is consistent across instances."""
    classifier1 = ISIC4Classifier()
    classifier2 = ISIC4Classifier()
    assert classifier1.sections == classifier2.sections


def test_empty_sections_before_load():
    """Test that sections is empty before _load_data."""

    class TestISIC4Classifier(ISIC4Classifier):
        def __init__(self, language="en"):
            self.language = language
            self.sections = []

    classifier = TestISIC4Classifier()
    assert classifier.sections == []
