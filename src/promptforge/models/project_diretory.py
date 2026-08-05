from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ProjectDirectory:
    path: Path