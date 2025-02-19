from pydantic import BaseModel
from .tree import Tree


class ISICClass(BaseModel):
    """A class representing an ISIC Class.

    The ISICClass represents the most granular level of the ISIC classification system.
    Each class has a unique code and description.

    Attributes:
        code (str): The unique ISIC code identifier.
        description (str): The text description of the class.

    Examples:
        >>> isic_class = ISICClass(code="0111", description="Growing of cereals")
        >>> isic_class.print_tree()
        0111: Growing of cereals
    """
    code: str
    description: str

    def print_tree(self, indent: str = "") -> None:
        """Display a tree representation of this ISIC Class.

        Prints the ISIC class code and description in a tree-like format.

        Args:
            indent (str, optional): String prefix used for indentation. Defaults to "".

        Returns:
            None
        """
        Tree.print(self, indent)


class ISICGroup(BaseModel):
    """A class representing an ISIC Group.

    The ISICGroup represents a collection of related ISIC classes. Each group
    contains one or more classes and has its own unique code and description.

    Attributes:
        code (str): The unique ISIC code identifier.
        description (str): The text description of the group.
        classes (list[ISICClass]): List of ISICClass objects contained in this group.

    Examples:
        >>> group = ISICGroup(code="011", description="Growing of non-perennial crops")
        >>> group.print_tree()
        011: Growing of non-perennial crops
    """
    code: str
    description: str
    classes: list[ISICClass]

    def print_tree(self, indent: str = "") -> None:
        """Display a tree representation of this ISIC Group.

        Prints the ISIC group and its classes in a hierarchical tree format.

        Args:
            indent (str, optional): String prefix used for indentation. Defaults to "".

        Returns:
            None
        """
        Tree.print(self, indent)


class ISICDivision(BaseModel):
    """A class representing an ISIC Division.

    The ISICDivision represents a broader category that contains multiple ISIC groups.
    Each division has a unique code, description, and contains one or more groups.

    Attributes:
        code (str): The unique ISIC code identifier.
        description (str): The text description of the division.
        groups (list[ISICGroup]): List of ISICGroup objects contained in this division.

    Examples:
        >>> division = ISICDivision(code="01", description="Crop and animal production")
        >>> division.print_tree()
        01: Crop and animal production
    """
    code: str
    description: str
    groups: list[ISICGroup]

    def print_tree(self, indent: str = "") -> None:
        """Display a tree representation of this ISIC Division.

        Prints the ISIC division and its groups in a hierarchical tree format.

        Args:
            indent (str, optional): String prefix used for indentation. Defaults to "".

        Returns:
            None
        """
        Tree.print(self, indent)


class ISICSection(BaseModel):
    """A class representing an ISIC Section.

    The ISICSection represents the highest level of the ISIC classification system.
    Each section contains multiple divisions and represents a broad economic sector.

    Attributes:
        code (str): The unique ISIC code identifier.
        description (str): The text description of the section.
        divisions (list[ISICDivision]): List of ISICDivision objects contained in this section.

    Examples:
        >>> section = ISICSection(code="A", description="Agriculture, forestry and fishing")
        >>> section.print_tree()
        A: Agriculture, forestry and fishing
    """
    code: str
    description: str
    divisions: list[ISICDivision]

    def print_tree(self, indent: str = "") -> None:
        """Display a tree representation of this ISIC Section.

        Prints the ISIC section and its divisions in a hierarchical tree format.

        Args:
            indent (str, optional): String prefix used for indentation. Defaults to "".

        Returns:
            None
        """
        Tree.print(self, indent)


class ISICHierarchy(BaseModel):
    """A class representing the hierarchical structure of ISIC classifications.

    This class stores the complete hierarchical path of an ISIC entity,
    from section down to class level, with each level being optional.

    Attributes:
        section (str | None): The section code, if applicable. Defaults to None.
        division (str | None): The division code, if applicable. Defaults to None.
        group (str | None): The group code, if applicable. Defaults to None.
        class_ (str | None): The class code, if applicable. Defaults to None.

    Examples:
        >>> hierarchy = ISICHierarchy(section="A", division="01", group="011", class_="0111")
    """
    section: str | None = None
    division: str | None = None
    group: str | None = None
    class_: str | None = None


class ISICSearchResult(BaseModel):
    """A class representing a single ISIC search result.

    This class contains detailed information about a single ISIC entity found
    during a search operation, including its position in the ISIC hierarchy.

    Attributes:
        type (str): The type of ISIC entity found (section/division/group/class).
        code (str): The ISIC code of the found entity.
        description (str): The text description of the found entity.
        hierarchy (ISICHierarchy): Object showing the position in the ISIC tree.
        path (str): String representation of the path to this entity.

    Examples:
        >>> result = ISICSearchResult(
        ...     type="class",
        ...     code="0111",
        ...     description="Growing of cereals",
        ...     hierarchy=ISICHierarchy(...),
        ...     path="A/01/011/0111"
        ... )
    """
    type: str
    code: str
    description: str
    hierarchy: ISICHierarchy
    path: str

    def print_tree(self, indent=""):
        """Display a tree representation of this search result.

        Prints the search result in a tree format, showing its code and description.

        Args:
            indent (str, optional): String prefix used for indentation. Defaults to "".

        Returns:
            None
        """
        Tree.print(self, indent)


class ISICSearchResults(BaseModel):
    """A class containing a collection of ISIC search results.

    This class manages multiple search results and provides functionality to
    display them in a hierarchical tree structure.

    Attributes:
        results (list[ISICSearchResult]): List of ISICSearchResult objects.

    Examples:
        >>> search_results = ISICSearchResults(results=[result1, result2])
        >>> search_results.print_tree()
        └── 01: Crop and animal production
            └── 011: Growing of non-perennial crops
                └── 0111: Growing of cereals
    """
    results: list[ISICSearchResult]

    def print_tree(self, indent=""):
        """Display a hierarchical tree representation of all search results.

        Creates and displays a tree structure showing the hierarchical
        relationship between all search results, organizing them by their
        position in the ISIC classification system.

        Args:
            indent (str, optional): String prefix used for indentation. Defaults to "".

        Returns:
            None

        Example:
            >>> results.print_tree()
            └── A: Agriculture, forestry and fishing
                └── 01: Crop and animal production
                    └── 011: Growing of non-perennial crops
        """
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
