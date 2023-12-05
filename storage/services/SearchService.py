from storage.FileRepository import FileRepository
from storage.services.dao.StorageDAO import StorageDAO
from storage.services.dto.ObjectDTO import ObjectDTO
from storage.services.dto.StorageItemDTO import StorageDTO
from typing import List


class SearchService:

    def __init__(self, storage: StorageDAO):
        self.storage = storage

    def _convert_dto(self, item: StorageDTO) -> ObjectDTO:
        return ObjectDTO(
            name=item.name,
            path=item.path,
            size=item.size,
            last_modified=item.last_modified,
            is_dir=item.is_dir,
            hash=item.hash,
        )

    def search(self, user_id: int, query: str) -> List[ObjectDTO]:
        root_item = self.storage.get_root(user_id)
        items = self.storage.list_objects(user_id, root_item.hash, True)
        res = []
        for item in items:
            if query in item.name:
                res.append(item)
        return list(map(self._convert_dto, res))
