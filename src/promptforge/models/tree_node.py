from dataclasses import dataclass, field
from collections.abc import Iterator

from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


@dataclass(slots=True)
class TreeNode:
    entry: ProjectDirectory | ProjectFile
    children: list["TreeNode"] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.entry.path.name

    @property
    def is_directory(self) -> bool:
        return isinstance(self.entry, ProjectDirectory)

    def walk(self) -> Iterator["TreeNode"]:
        yield self

        for child in self.children:
            yield from child.walk()

    