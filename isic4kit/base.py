from .models import ISICSection, ISICDivision, ISICGroup, ISICClass


class BaseISIC4:
    """Base class with common ISIC4 functionality."""

    def get_section(self, code: str) -> ISICSection | None:
        """Get section by code."""
        return next((s for s in self.sections if s.code == code.lower()), None)

    def get_division(self, code: str) -> ISICDivision | None:
        """Get division by code."""
        for section in self.sections:
            division = next((d for d in section.divisions if d.code == code), None)
            if division:
                return division
        return None

    def get_group(self, code: str) -> ISICGroup | None:
        """Get group by code."""
        for section in self.sections:
            for division in section.divisions:
                group = next((g for g in division.groups if g.code == code), None)
                if group:
                    return group
        return None

    def get_class(self, code: str) -> ISICClass | None:
        """Get class by code."""
        for section in self.sections:
            for division in section.divisions:
                for group in division.groups:
                    class_ = next((c for c in group.classes if c.code == code), None)
                    if class_:
                        return class_
        return None
