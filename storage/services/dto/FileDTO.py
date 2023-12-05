from dataclasses import dataclass


@dataclass
class FileDTO:
    path: str
    data: bytes
