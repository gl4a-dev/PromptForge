from promptforge.formatters.content_formatter import ContentFormatter
from promptforge.formatters.tree_formatter import TreeFormatter
from promptforge.models.project_file import ProjectFile
from promptforge.models.tree_node import TreeNode
from promptforge.models.scan_result import ScanResult
from promptforge.readers.file_reader import FileReader
from promptforge.tree.tree_builder import TreeBuilder


class PromptBuilder:

    def __init__(self) -> None:
        self._tree_builder = TreeBuilder()
        self._tree_formatter = TreeFormatter()
        self._file_reader = FileReader()
        self._content_formatter = ContentFormatter()

    def build(self, scan_result: ScanResult) -> str:
        tree = self._tree_builder.build(scan_result)

        tree_output = self._tree_formatter.format(tree)
        content_output = self._format_files(tree, scan_result)

        return (
            "# Project Structure\n\n"
            f"{tree_output}\n\n"
            "# File Contents\n\n"
            f"{content_output}"
        )

    def _format_files(self, tree:TreeNode, scan_result: ScanResult) -> str:
        sections: list[str] = []

        for node in tree.walk():
            if node.is_directory:
                continue

            content = self._file_reader.read(node.entry)

            sections.append(
                self._content_formatter.format(
                    node.entry,
                    content,
                    scan_result,
                )
            )

        return "\n".join(sections)