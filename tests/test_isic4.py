import pytest
from isic4kit import ISIC4Classifier


def test_init_default_language():
    classifier = ISIC4Classifier()
    assert classifier.language == "en"
    assert len(classifier.sections) > 0


def test_init_custom_language():
    classifier = ISIC4Classifier(language="ar")
    assert classifier.language == "ar"
    assert len(classifier.sections) > 0


def test_init_invalid_language():
    with pytest.raises(ValueError):
        ISIC4Classifier(language="invalid_language")


def test_load_data():
    classifier = ISIC4Classifier()
    assert len(classifier.sections) > 0
    section = classifier.sections[0]
    assert hasattr(section, "code")
    assert hasattr(section, "description")
    assert isinstance(section.code, str)
    assert isinstance(section.description, str)


@pytest.mark.parametrize("language", ["en", "ar"])
def test_supported_languages(language):
    classifier = ISIC4Classifier(language=language)
    assert classifier.language == language
    assert len(classifier.sections) > 0


def test_data_consistency():
    classifier1 = ISIC4Classifier()
    classifier2 = ISIC4Classifier()
    assert classifier1.sections == classifier2.sections


def test_empty_sections_before_load():
    class TestISIC4Classifier(ISIC4Classifier):
        def __init__(self, language="en"):
            self.language = language
            self.sections = []

    classifier = TestISIC4Classifier()
    assert classifier.sections == []


def test_language_support():
    isic_en = ISIC4Classifier(language="en")
    isic_ar = ISIC4Classifier(language="ar")

    section_en = isic_en.get_section("A")
    section_ar = isic_ar.get_section("A")
    assert section_en.code == section_ar.code
    assert section_en.description != section_ar.description


def test_search():
    isic = ISIC4Classifier()
    results = isic.search("mining")
    assert results is not None
    assert any("mining" in result.description.lower() for result in results.results)
    results_upper = isic.search("MINING")
    assert results.results == results_upper.results


def test_search_result_structure():
    isic = ISIC4Classifier()
    results = isic.search("mining")

    assert results is not None
    assert hasattr(results, "results")
    assert isinstance(results.results, list)
    assert len(results.results) > 0

    for result in results.results:
        assert hasattr(result, "type")
        assert hasattr(result, "code")
        assert hasattr(result, "description")
        assert hasattr(result, "hierarchy")

        assert isinstance(result.type, str)
        assert isinstance(result.code, str)
        assert isinstance(result.description, str)

        assert hasattr(result.hierarchy, "section")
        assert hasattr(result.hierarchy, "division")
        assert hasattr(result.hierarchy, "group")
        assert hasattr(result.hierarchy, "class_")

        assert "mining" in result.description.lower()
        assert result.type in ["section", "division", "group", "class"]


def test_invalid_inputs():
    isic = ISIC4Classifier()

    assert isic.get_section("Z") is None
    assert isic.get_division("00") is None
    assert isic.get_group("000") is None
    assert isic.get_class("0000") is None


def test_tree_structure():
    isic = ISIC4Classifier()
    section = isic.get_section("A")
    assert len(section.divisions) > 0
    division = section.divisions[0]
    assert len(division.groups) > 0
    group = division.groups[0]
    assert len(group.classes) > 0


def test_data_validation():
    isic = ISIC4Classifier()

    section = isic.get_section("A")
    assert len(section.code) == 1
    assert section.code.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    division = isic.get_division("01")
    assert len(division.code) == 2
    assert division.code.isdigit()
    assert 1 <= int(division.code) <= 99

    group = isic.get_group("011")
    assert len(group.code) == 3
    assert group.code.isdigit()
    assert group.code.startswith(division.code)

    class_ = isic.get_class("0111")
    assert len(class_.code) == 4
    assert class_.code.isdigit()
    assert class_.code.startswith(group.code)


def test_hierarchy_navigation():
    isic = ISIC4Classifier()

    section = isic.get_section("A")
    division = isic.get_division("01")
    group = isic.get_group("011")
    class_ = isic.get_class("0111")

    assert division in section.divisions
    assert group in division.groups
    assert class_ in group.classes

    assert division.code[:2] == "01"
    assert group.code[:3] == "011"
    assert class_.code == "0111"


def test_language_switching():
    isic = ISIC4Classifier()
    assert isic.language == "en"
    isic.language = "ar"
    assert isic.language == "ar"
    section_ar = isic.get_section("A")
    assert section_ar is not None
    assert isinstance(section_ar.description, str)


def test_data_loading():
    isic = ISIC4Classifier()
    assert hasattr(isic, "sections")
    assert len(isic.sections) > 0
    section = isic.sections[0]
    assert hasattr(section, "code")
    assert hasattr(section, "description")
    assert hasattr(section, "divisions")


def test_object_structure():
    isic = ISIC4Classifier()
    section = isic.get_section("A")
    division = isic.get_division("01")

    assert hasattr(section, "code")
    assert hasattr(section, "description")
    assert section.code.lower() == "a"
    assert "agriculture" in section.description.lower()

    assert hasattr(division, "code")
    assert hasattr(division, "description")
    assert division.code == "01"
    assert "crop" in division.description.lower()

    section_repr = repr(section)
    assert section.code in section_repr
    assert section.description in section_repr

    division_repr = repr(division)
    assert division.code in division_repr
    assert division.description in division_repr


def test_empty_search():
    isic = ISIC4Classifier()
    results = isic.search("nonexistentterm123456")
    assert results is not None
    assert len(results.results) == 0


def test_case_insensitive_section():
    isic = ISIC4Classifier()
    section_upper = isic.get_section("A")
    section_lower = isic.get_section("a")
    assert section_upper == section_lower
    assert section_upper.code.upper() == "A"


def test_hierarchy_path():
    isic = ISIC4Classifier()

    section = isic.get_section("A")
    division = isic.get_division("01")
    group = isic.get_group("011")
    class_ = isic.get_class("0111")

    assert division.code in [d.code for d in section.divisions]
    assert group.code in [g.code for g in division.groups]
    assert class_.code in [c.code for c in group.classes]


def test_description_content():
    isic = ISIC4Classifier()

    section = isic.get_section("B")
    assert "mining" in section.description.lower()

    division = isic.get_division("05")
    assert "coal" in division.description.lower()

    group = isic.get_group("051")
    assert "hard coal" in group.description.lower()

    class_ = isic.get_class("0510")
    assert "anthracite" in class_.description.lower()


def test_language_specific_content():
    isic_en = ISIC4Classifier(language="en")
    isic_ar = ISIC4Classifier(language="ar")

    section_en = isic_en.get_section("A")
    section_ar = isic_ar.get_section("A")
    assert section_en.description != section_ar.description

    assert any(char in section_ar.description for char in "ةيبرعلا")


def test_invalid_language():
    with pytest.raises(ValueError):
        ISIC4Classifier(language="invalid")

    isic = ISIC4Classifier()
    assert isic.language == "en"

    isic.language = "ar"
    assert isic.language == "ar"

    section = isic.get_section("A")
    assert section is not None
    assert isinstance(section.description, str)


def test_search_special_chars():
    isic = ISIC4Classifier()

    results = isic.search("mining and quarrying")
    assert results is not None
    assert len(results.results) > 0
    assert any("quarrying" in r.description.lower() for r in results.results)

    results = isic.search("mining")
    assert results is not None
    assert len(results.results) > 0

    results = isic.search("mining & extraction")
    assert results is not None
    if len(results.results) > 0:
        assert any("mining" in r.description.lower() for r in results.results)


def test_search_with_numbers():
    isic = ISIC4Classifier()

    results = isic.search("05")
    assert results is not None
    assert len(results.results) > 0
    assert any(r.code.startswith("05") for r in results.results)


def test_hierarchy_consistency():
    isic = ISIC4Classifier()

    for section in isic.sections:
        assert len(section.code) == 1
        assert section.code.isalpha()

        for division in section.divisions:
            assert len(division.code) == 2
            assert division.code.isdigit()

            for group in division.groups:
                assert len(group.code) == 3
                assert group.code.isdigit()
                assert group.code.startswith(division.code)

                for class_ in group.classes:
                    assert len(class_.code) == 4
                    assert class_.code.isdigit()
                    assert class_.code.startswith(group.code)


def test_search_result_ordering():
    isic = ISIC4Classifier()
    results = isic.search("mining")

    if len(results.results) > 1:
        section_indices = [
            i for i, r in enumerate(results.results) if r.type == "section"
        ]
        division_indices = [
            i for i, r in enumerate(results.results) if r.type == "division"
        ]

        if section_indices and division_indices:
            assert min(section_indices) < min(division_indices)


def test_model_equality():
    isic = ISIC4Classifier()

    section1 = isic.get_section("A")
    section2 = isic.get_section("A")
    section3 = isic.get_section("B")

    assert section1 == section2
    assert section1 != section3
    assert section1 != "A"

    div1 = isic.get_division("01")
    div2 = isic.get_division("01")
    div3 = isic.get_division("02")

    assert div1 == div2
    assert div1 != div3
    assert div1 != "01"

    group1 = isic.get_group("011")
    group2 = isic.get_group("011")
    group3 = isic.get_group("012")

    assert group1 == group2
    assert group1 != group3
    assert group1 != "011"

    class1 = isic.get_class("0111")
    class2 = isic.get_class("0111")
    class3 = isic.get_class("0112")

    assert class1 == class2
    assert class1 != class3
    assert class1 != "0111"


def test_tree_traversal():
    isic = ISIC4Classifier()

    class_ = isic.get_class("0111")
    group = isic.get_group("011")
    division = isic.get_division("01")
    section = isic.get_section("A")

    assert class_.code.startswith(group.code)
    assert group.code.startswith(division.code)
    assert any(div.code == division.code for div in section.divisions)

    assert any(cls.code == class_.code for cls in group.classes)
    assert any(grp.code == group.code for grp in division.groups)
    assert any(div.code == division.code for div in section.divisions)


def test_model_str_representations():
    isic = ISIC4Classifier()

    section = isic.get_section("A")
    division = isic.get_division("01")
    group = isic.get_group("011")
    class_ = isic.get_class("0111")

    assert section.code in repr(section)
    assert section.description in repr(section)
    assert division.code in repr(division)
    assert division.description in repr(division)
    assert group.code in repr(group)
    assert group.description in repr(group)
    assert class_.code in repr(class_)
    assert class_.description in repr(class_)


def test_search_result_model():
    isic = ISIC4Classifier()
    results = isic.search("mining")

    for result in results.results:
        assert result.hierarchy is not None
        assert hasattr(result.hierarchy, "section")
        assert hasattr(result.hierarchy, "division")
        assert hasattr(result.hierarchy, "group")
        assert hasattr(result.hierarchy, "class_")

        assert result.code in repr(result)
        assert result.description in repr(result)
        assert result.type in repr(result)

        same_result = next(r for r in results.results if r.code == result.code)
        assert result == same_result
        assert result != "not a search result"


def test_tree_node_operations():
    isic = ISIC4Classifier()

    section = isic.get_section("A")
    division = isic.get_division("01")

    original_divisions = len(section.divisions)
    test_division = division.__class__(
        code="99",
        description="Test Division",
        groups=[],
    )

    section.divisions.append(test_division)
    assert len(section.divisions) == original_divisions + 1
    assert test_division in section.divisions

    section.divisions.remove(test_division)
    assert len(section.divisions) == original_divisions
    assert test_division not in section.divisions


def test_search_results_container():
    isic = ISIC4Classifier()

    empty_results = isic.search("nonexistent")
    assert len(empty_results.results) == 0
    assert "results=[]" in repr(empty_results)

    results = isic.search("mining")
    assert len(results.results) > 0
    assert "results=" in repr(results)

    same_results = isic.search("mining")
    assert results == same_results
    assert results != empty_results
    assert results != "not a results container"
