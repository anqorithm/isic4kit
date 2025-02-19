from .models import ISICSection, ISICDivision, ISICGroup, ISICClass


class BaseISIC4:
    """Base class providing common ISIC4 (International Standard Industrial Classification Revision 4) functionality.

    This class provides methods to retrieve ISIC4 classifications at different levels
    of the hierarchy (section, division, group, and class).

    Attributes:
        sections: A list of ISICSection objects representing all ISIC4 sections.
    """

    def get_section(self, code: str) -> ISICSection | None:
        """Retrieve an ISIC4 section by its code.

        Args:
            code (str): The section code to search for (case-insensitive).

        Returns:
            ISICSection | None: The matching ISICSection object if found, None otherwise.
        """
        return next((s for s in self.sections if s.code == code.lower()), None)

    def get_division(self, code: str) -> ISICDivision | None:
        """Retrieve an ISIC4 division by its code.

        Args:
            code (str): The division code to search for.

        Returns:
            ISICDivision | None: The matching ISICDivision object if found, None otherwise.
        """
        for section in self.sections:
            division = next((d for d in section.divisions if d.code == code), None)
            if division:
                return division
        return None

    def get_group(self, code: str) -> ISICGroup | None:
        """Retrieve an ISIC4 group by its code.

        Args:
            code (str): The group code to search for.

        Returns:
            ISICGroup | None: The matching ISICGroup object if found, None otherwise.
        """
        for section in self.sections:
            for division in section.divisions:
                group = next((g for g in division.groups if g.code == code), None)
                if group:
                    return group
        return None

    def get_class(self, code: str) -> ISICClass | None:
        """Retrieve an ISIC4 class by its code.

        Args:
            code (str): The class code to search for.

        Returns:
            ISICClass | None: The matching ISICClass object if found, None otherwise.
        """
        for section in self.sections:
            for division in section.divisions:
                for group in division.groups:
                    class_ = next((c for c in group.classes if c.code == code), None)
                    if class_:
                        return class_
        return None
