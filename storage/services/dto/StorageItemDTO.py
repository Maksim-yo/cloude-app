from dataclasses import dataclass


@dataclass
class StorageDTO:
    path: str               # should include real name
    bucket_name: str
    user_id: int
    hash: str
    size: int
    last_modified: str
    is_dir: bool
    name: str


