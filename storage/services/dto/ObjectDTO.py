from dataclasses import dataclass


@dataclass
class ObjectDTO:
    name: str
    path: str
    hash: str
    size: int
    last_modified: str
    is_dir: bool