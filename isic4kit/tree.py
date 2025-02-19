class Tree:
    """Handles hierarchical tree visualization of ISIC4 nodes.

    This class provides methods to display and format hierarchical relationships
    between ISIC4 nodes (Sections, Divisions, Groups, and Classes) using ASCII
    branch lines for visual clarity.

    Attributes:
        None

    Methods:
        print(node, prefix="", is_last=True): Displays a hierarchical tree visualization
            of ISIC4 nodes.

    Example:
        >>> section = Section("A", "Agriculture")
        >>> Tree.print(section)
        └── A: Agriculture
            └── 01: Crop and animal production
                └── 011: Growing of non-perennial crops
    """

    @staticmethod
    def print(node, prefix: str = "", is_last: bool = True) -> None:
        """Display a hierarchical tree visualization of ISIC4 nodes.

        Prints a tree structure showing the hierarchical relationship between
        ISIC4 nodes using ASCII branch lines for visual clarity. The tree
        can start from any level in the ISIC4 hierarchy (Section, Division,
        Group, or Class).

        Args:
            node: An ISIC4 node object representing the root of the tree to display.
                Can be a Section, Division, Group, or Class.
            prefix: The current line prefix used for indentation and branch formatting.
                Defaults to an empty string.
            is_last: Indicates if the current node is the last child in its level.
                Affects the branch line style. Defaults to True.

        Returns:
            None

        Example:
            >>> division = Division("01", "Crop and animal production")
            >>> Tree.print(division)
            └── 01: Crop and animal production
                └── 011: Growing of non-perennial crops
        """
        branch = "└── " if is_last else "├── "
        print(f"{prefix}{branch}{node.code}: {node.description}")

        child_prefix = prefix + ("    " if is_last else "│   ")

        children = []
        if hasattr(node, "divisions"):
            children = node.divisions
        elif hasattr(node, "groups"):
            children = node.groups
        elif hasattr(node, "classes"):
            children = node.classes

        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            Tree.print(child, child_prefix, is_last_child)
