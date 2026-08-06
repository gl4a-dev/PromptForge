from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory
from promptforge.models.scan_result import ScanResult
from promptforge.models.tree_node import TreeNode


class TreeBuilder:

    def build(self, scan_result: ScanResult) -> TreeNode:
        root = TreeNode(scan_result.root)

        nodes = {
            scan_result.root.path: root,
        }

        for directory in scan_result.directories:
            nodes[directory.path] = TreeNode(directory)

        for file in scan_result.files:
            nodes[file.path] = TreeNode(file)

        for path, node in list(nodes.items()):
            if path == scan_result.root.path:
                continue

            parent = nodes.get(path.parent)

            if parent is not None:
                parent.children.append(node)

        self._sort(root)

        return root

    def _sort(self, node: TreeNode) -> None:
        node.children.sort(
            key=lambda child: (
                isinstance(child.entry, ProjectFile),
                child.entry.path.name.lower(),
            )
        )

        for child in node.children:
            self._sort(child)