import json
from pathlib import Path
from .models import ISICSection, ISICDivision, ISICGroup, ISICClass


class ISICLoaderMixin:
    """Mixin class providing data loading functionality for ISIC4.

    This mixin provides methods to load and parse ISIC4 classification data
    from JSON files in different languages. It handles the loading and parsing
    of hierarchical ISIC4 classification data.

    Attributes:
        sections (list[ISICSection]): List of ISIC sections containing the complete
            hierarchical structure of classifications.
        language (str): The language code for loading classification data.

    Example:
        >>> class ISICLoader(ISICLoaderMixin):
        ...     def __init__(self, language='en'):
        ...         self.language = language
        ...         self._load_data()
        >>> loader = ISICLoader()
        >>> sections = loader.sections
    """

    def _load_data(self):
        """Load and parse ISIC4 classification data from JSON file.

        This method reads the JSON file corresponding to the instance's language
        setting and constructs a hierarchical structure of ISIC4 classifications
        (sections -> divisions -> groups -> classes). The data is stored in the
        sections attribute of the instance.

        The JSON file should be located in the 'data' directory with the filename
        format '{language}.json'.

        Raises:
            ValueError: If the specified language is not supported
                (no corresponding JSON file exists in the data directory).
                The error message includes a list of available languages.

        Note:
            The loaded data structure follows the hierarchy:
            - Sections contain Divisions
            - Divisions contain Groups
            - Groups contain Classes
        """
        data_path = Path(__file__).parent / "data" / f"{self.language}.json"
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            supported_languages = [
                p.stem for p in (Path(__file__).parent / "data").glob("*.json")
            ]
            raise ValueError(
                f"Language '{self.language}' is not supported. "
                f"Available languages: {', '.join(sorted(supported_languages))}"
            )

        self.sections = []
        for section_data in data["sections"]:
            section = ISICSection(
                code=section_data["section"],
                description=section_data["description"],
                divisions=[
                    ISICDivision(
                        code=div_data["division"],
                        description=div_data["description"],
                        groups=[
                            ISICGroup(
                                code=group_data["group"],
                                description=group_data["description"],
                                classes=[
                                    ISICClass(
                                        code=class_data["class"],
                                        description=class_data["description"],
                                    )
                                    for class_data in group_data["classes"]
                                ],
                            )
                            for group_data in div_data["groups"]
                        ],
                    )
                    for div_data in section_data["divisions"]
                ],
            )
            self.sections.append(section)
