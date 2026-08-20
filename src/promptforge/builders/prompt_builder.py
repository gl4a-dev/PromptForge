from promptforge.formatters.content_formatter import ContentFormatter
from promptforge.formatters.tree_formatter import TreeFormatter
from promptforge.models.project_file import ProjectFile
from promptforge.models.tree_node import TreeNode
from promptforge.models.scan_result import ScanResult
from promptforge.readers.file_reader import FileReader
from promptforge.tree.tree_builder import TreeBuilder


class PromptBuilder:

    def __init__(self, build_tree: bool = True, build_content: bool = True) -> None:
        if (build_tree == False) and (build_content == False):
            raise ValueError("build_tree and build_content can't be both False")

        self.build_tree = build_tree
        self.build_content = build_content

        self._tree_builder = TreeBuilder()
        self._tree_formatter = TreeFormatter()
        self._file_reader = FileReader()
        self._content_formatter = ContentFormatter()

    def build(self, scan_result: ScanResult) -> str:
        tree = self._tree_builder.build(scan_result)

        prompt_list: list[str] = []
        if self.build_tree:
            tree_output = self._tree_formatter.format(tree)
            prompt_list.append("# Project Structure")
            prompt_list.append(tree_output)

        if self.build_content:
            content_output = self._format_files(tree, scan_result)
            prompt_list.append("# File Contents")
            prompt_list.append(content_output)

        return "\n\n".join(prompt_list)

    def _format_files(self, tree:TreeNode, scan_result: ScanResult) -> str:
        sections: list[str] = []

        for node in tree.walk():
            if node.is_directory:
                continue

            content = self._file_reader.read(node.entry)

            if content is None:
                continue

            sections.append(
                self._content_formatter.format(
                    node.entry,
                    content,
                    scan_result,
                )
            )

        return "\n".join(sections)