import json
from pathlib import Path
from .models import ISICSection, ISICDivision, ISICGroup, ISICClass


class ISICLoaderMixin:
    """Mixin class providing data loading functionality for ISIC4."""

    def _load_data(self):
        """Load ISIC4 data from JSON file.

        Raises:
            ValueError: If the specified language is not supported (JSON file not found).
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
