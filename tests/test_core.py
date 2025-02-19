import pytest
from isic4kit.core import ISICClassification
from pathlib import Path


def test_init_with_default_values():
    isic = ISICClassification()
    assert isic.language == "en"
    assert not isic.case_sensitive
    assert len(isic.sections) > 0


def test_init_with_custom_values():
    isic = ISICClassification(language="ar", case_sensitive=True)
    assert isic.language == "ar"
    assert isic.case_sensitive
    assert len(isic.sections) > 0


def test_invalid_language():
    with pytest.raises(ValueError) as exc_info:
        ISICClassification(language="invalid")
    assert "Invalid language specified" in str(exc_info.value)
    assert "en, ar" in str(exc_info.value)


def test_supported_languages():
    isic = ISICClassification()
    languages = isic.supported_languages
    assert isinstance(languages, set)
    assert "en" in languages
    assert "ar" in languages
    assert len(languages) == 2


def test_case_sensitive_property():
    isic = ISICClassification()
    assert not isic.case_sensitive

    isic.case_sensitive = True
    assert isic.case_sensitive

    isic.case_sensitive = False
    assert not isic.case_sensitive


def test_language_property():
    isic = ISICClassification()
    assert isic.language == "en"

    isic.language = "ar"
    assert isic.language == "ar"

    with pytest.raises(ValueError) as exc_info:
        isic.language = "invalid"
    assert "Invalid language specified" in str(exc_info.value)


def test_load_data_file_not_found():
    # Temporarily rename or move the data file to simulate missing file
    data_file = Path(__file__).parent.parent / "isic4kit" / "data" / "en.json"
    temp_file = data_file.with_suffix(".json.bak")

    if data_file.exists():
        data_file.rename(temp_file)

        with pytest.raises(FileNotFoundError) as exc_info:
            ISICClassification()
        assert "Data file not found" in str(exc_info.value)

        # Restore the file
        temp_file.rename(data_file)


def test_language_case_insensitivity():
    isic1 = ISICClassification(language="EN")
    assert isic1.language == "en"

    isic2 = ISICClassification(language="Ar")
    assert isic2.language == "ar"

    isic1.language = "AR"
    assert isic1.language == "ar"
