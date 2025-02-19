from .models import ISICHierarchy, ISICSearchResult, ISICSearchResults


class ISICSearchMixin:
    """Mixin class providing search functionality for ISIC classifications.

    This mixin provides methods to search through ISIC (International Standard Industrial
    Classification) hierarchy levels including sections, divisions, groups, and classes.
    The search can be performed on both classification codes and descriptions.

    The mixin assumes the implementing class has a `sections` attribute containing
    the ISIC classification hierarchy.
    """

    def search(self, query: str) -> ISICSearchResults:
        """Search ISIC classifications for matching codes or descriptions.

        Performs a case-insensitive search across all levels of the ISIC hierarchy
        (sections, divisions, groups, and classes) looking for matches in either
        the code or description fields.

        The search is performed by checking if the query string is contained within
        either the code or description of any classification item. The search is
        case-insensitive and ignores leading/trailing whitespace.

        Args:
            query: A string to search for within ISIC codes and descriptions.
                  Can be a partial or complete code or description.

        Returns:
            ISICSearchResults: A container of search results. Each result includes:
                - type: The hierarchy level ('section', 'division', 'group', or 'class')
                - code: The classification code
                - description: The classification description
                - hierarchy: An ISICHierarchy object containing the full path information
                - path: A string representation of the hierarchical path, joined by '/'

        Example:
            >>> isic = ISICClassification()
            >>> results = isic.search("agriculture")
            >>> print(results.results[0].code)  # First matching result's code
            'A'
        """
        query = query.lower().strip()
        results = []

        def add_result(item_type, code, description, hierarchy):
            results.append(
                ISICSearchResult(
                    type=item_type,
                    code=code,
                    description=description,
                    hierarchy=ISICHierarchy(
                        section=hierarchy[0] if len(hierarchy) > 0 else None,
                        division=hierarchy[1] if len(hierarchy) > 1 else None,
                        group=hierarchy[2] if len(hierarchy) > 2 else None,
                        class_=hierarchy[3] if len(hierarchy) > 3 else None,
                    ),
                    path="/".join(hierarchy),
                )
            )

        for section in self.sections:
            if query in section.code.lower() or query in section.description.lower():
                add_result("section", section.code, section.description, [section.code])

            for division in section.divisions:
                if query in division.code or query in division.description.lower():
                    add_result(
                        "division",
                        division.code,
                        division.description,
                        [section.code, division.code],
                    )

                for group in division.groups:
                    if query in group.code or query in group.description.lower():
                        add_result(
                            "group",
                            group.code,
                            group.description,
                            [section.code, division.code, group.code],
                        )

                    for class_ in group.classes:
                        if query in class_.code or query in class_.description.lower():
                            add_result(
                                "class",
                                class_.code,
                                class_.description,
                                [section.code, division.code, group.code, class_.code],
                            )

        return ISICSearchResults(results=results)
