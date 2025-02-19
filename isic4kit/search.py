from .models import ISICHierarchy, ISICSearchResult, ISICSearchResults


class ISICSearchMixin:
    def search(self, query: str) -> ISICSearchResults:
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
