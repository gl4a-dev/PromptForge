from promptforge.models.tree_node import TreeNode


class TreeFormatter:

    def format(self, tree: TreeNode) -> str:
        lines = [tree.name]

        for index, child in enumerate(tree.children):
            is_last = index == len(tree.children) - 1

            self._append_node(
                child,
                lines,
                prefix="",
                is_last=is_last,
            )

        return "\n".join(lines)

    def _append_node(self, node: TreeNode, lines: list[str], prefix: str, is_last: bool) -> None:
        connector = "└── " if is_last else "├── "

        lines.append(f"{prefix}{connector}{node.name}")

        child_prefix = prefix + ("    " if is_last else "│   ")

        for index, child in enumerate(node.children):
            child_is_last = (index == len(node.children) - 1)

            self._append_node(
                child,
                lines,
                child_prefix,
                child_is_last,
            )