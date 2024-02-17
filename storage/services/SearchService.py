import storage.config as config
from storage.services.dto.ObjectDTO import ObjectDTO
from storage.services.dto.StorageItemDTO import StorageDTO
from typing import List


class SearchService:

    def _convert_dto(self, item: StorageDTO) -> ObjectDTO:
        return ObjectDTO(
            name=item.name,
            path=item.path,
            size=item.size,
            last_modified=item.last_modified,
            is_dir=item.is_dir,
            hash=item.hash,
        )

    def search(self, user_id: int, current_folder_hash: str, query: str) -> List[ObjectDTO]:
        items = config.folder_service.get_items(user_id, current_folder_hash, True)
        res = []
        for item in items:
            if query.lower() in item.name.lower():
                res.append(item)
        return list(map(self._convert_dto, res))
