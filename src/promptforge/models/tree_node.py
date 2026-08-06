from dataclasses import dataclass, field

from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


@dataclass(slots=True)
class TreeNode:
    entry: ProjectDirectory | ProjectFile
    children: list["TreeNode"] = field(default_factory=list)