def print_tree(node, prefix="", is_last=True):
    """Print a hierarchical tree view of ISIC4 nodes with branch lines.

    Args:
        node: An ISIC node (Section, Division, Group, or Class)
        prefix (str): Current line prefix for formatting
        is_last (bool): Whether this node is the last child
    """
    # Branch symbols
    branch = "└── " if is_last else "├── "

    # Print current node
    print(f"{prefix}{branch}{node.code}: {node.description}")

    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Handle children based on node type
    children = []
    if hasattr(node, "divisions"):
        children = node.divisions
    elif hasattr(node, "groups"):
        children = node.groups
    elif hasattr(node, "classes"):
        children = node.classes

    # Print children
    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        print_tree(child, child_prefix, is_last_child)
