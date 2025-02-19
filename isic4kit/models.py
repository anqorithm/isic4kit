from dataclasses import dataclass
from pydantic import BaseModel
from .tree import print_tree


@dataclass
class ISICClass:
    code: str
    description: str

    def print_tree(self, indent=""):
        print_tree(self, indent)


@dataclass
class ISICGroup:
    code: str
    description: str
    classes: list

    def print_tree(self, indent=""):
        print_tree(self, indent)


@dataclass
class ISICDivision:
    code: str
    description: str
    groups: list

    def print_tree(self, indent=""):
        print_tree(self, indent)


@dataclass
class ISICSection:
    code: str
    description: str
    divisions: list

    def print_tree(self, indent=""):
        print_tree(self, indent)


# Search-related models
class ISICHierarchy(BaseModel):
    section: str | None = None
    division: str | None = None
    group: str | None = None
    class_: str | None = None


class ISICSearchResult(BaseModel):
    type: str
    code: str
    description: str
    hierarchy: ISICHierarchy
    path: str

    def print_tree(self, indent=""):
        print(f"{indent}├── {self.code}: {self.description}")


class ISICSearchResults(BaseModel):
    results: list[ISICSearchResult]

    def print_tree(self, indent=""):
        # Group results by section
        sections = {}
        for result in self.results:
            section = result.hierarchy.section
            division = result.hierarchy.division
            group = result.hierarchy.group
            class_ = result.hierarchy.class_

            if section not in sections:
                sections[section] = {"item": None, "divisions": {}}

            if division:
                if division not in sections[section]["divisions"]:
                    sections[section]["divisions"][division] = {
                        "item": None,
                        "groups": {},
                    }
                if result.type == "division":
                    sections[section]["divisions"][division]["item"] = result

                if group:
                    if group not in sections[section]["divisions"][division]["groups"]:
                        sections[section]["divisions"][division]["groups"][group] = {
                            "item": None,
                            "classes": {},
                        }
                    if result.type == "group":
                        sections[section]["divisions"][division]["groups"][group][
                            "item"
                        ] = result

                    if class_ and result.type == "class":
                        sections[section]["divisions"][division]["groups"][group][
                            "classes"
                        ][class_] = result

        # Print the tree
        for section, section_data in sections.items():
            for division, division_data in section_data["divisions"].items():
                if division_data["item"]:
                    print(
                        f"{indent}├── {division_data['item'].code}: {division_data['item'].description}"
                    )

                for group, group_data in division_data["groups"].items():
                    if group_data["item"]:
                        print(
                            f"{indent}│   ├── {group_data['item'].code}: {group_data['item'].description}"
                        )

                    for class_, class_result in group_data["classes"].items():
                        if class_result:
                            print(
                                f"{indent}│   │   ├── {class_result.code}: {class_result.description}"
                            )
