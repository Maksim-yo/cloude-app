import datetime
from typing import List

from django.contrib.auth.models import User

from storage.models import StorageItem, RootStorageItem
from storage.services.dto.StorageItemDTO import StorageDTO
from storage.exceptions import ObjectExistError, NotCorrectTypeError
from storage.utils import path_hash, is_folder, get_relative_path, get_object_name
from storage.ObjectPathFactory import ObjectPathFactory


class StorageDAO:

    def __init__(self, object_path_factory: ObjectPathFactory):
        self.object_path_factory = object_path_factory

    def _orm_to_entity(self, item: StorageItem) -> StorageDTO:
        return StorageDTO(
            path=item.path,
            bucket_name=item.bucket,
            hash=item.hash,
            size=item.size,
            last_modified=item.last_modified,
            is_dir=item.is_dir,
            user_id=item.user.id,
            name=item.name,
        )

    def get_user(self, user_id: int):
        return User.objects.get(pk=user_id)

    def is_object_exist(self, user_id: int, path: str):
        user = self.get_user(user_id)
        try:
            item = user.storage_items.get(path__exact=path)
            return True
        except:
            return False

    def _get_object(self, user_id: int, item_hash: str) -> StorageItem:
        user = self.get_user(user_id)
        item = user.storage_items.get(hash__exact=item_hash)
        if item is None:
            raise ObjectExistError(f"Object with hash ${item_hash} doesn't exist")
        return item

    def get_object(self, user_id: int, item_hash: str) -> StorageDTO:
        item = self._get_object(user_id, item_hash)
        return self._orm_to_entity(item)

    def get_object_by_path(self, user_id: int, item_path: str) -> StorageItem:
        self.is_object_exist(user_id, item_path)
        user = self.get_user(user_id)
        item = user.storage_items.get(path__exact=item_path)
        return item

    def calculate_hash(self, path: str):
        return path_hash(path)

    def compose_path(self, parent_path: str, obj_path: str) -> str:
        return parent_path + '/' + obj_path

    def get_root_object(self, user_id: int) -> StorageDTO:
        user = self.get_user(user_id)
        return self._orm_to_entity(user.root_item)

    def _list_objects_recursive(self, objects: List[List[StorageItem]], item: StorageItem) -> None:
        objs = item.items.all()
        temp = []
        for obj in objs:
            self._list_objects_recursive(objects, obj)
            temp.append(obj)
        if temp:
            objects.append(temp)

    def object_parents(self, user_id: int, item_hash: str) -> List[StorageDTO]:
        item: StorageItem = self._get_object(user_id, item_hash)
        items: List[StorageDTO] = []
        while item:
            items.append(self._orm_to_entity(item))
            item = item.parent
        return items

    def object_parent(self, user_id: int, item_hash: str) -> StorageDTO:
        item: StorageItem = self._get_object(user_id, item_hash)
        return self._orm_to_entity(item.parent) if item.parent else None

    def list_objects(self, user_id: int, parent_hash: str, recursive: bool = False) -> List[StorageDTO]:
        user = self.get_user(user_id)
        folder: StorageDTO = self.get_object(user_id, parent_hash)
        if folder.is_dir is False:
            raise NotCorrectTypeError(f"Object ${parent_hash} is not directory")
        items = user.storage_items.filter(parent__hash=parent_hash)
        objects: List[StorageDTO] = []
        _objects: List[List[StorageItem]] = []
        for item in items:
            if recursive:
                self._list_objects_recursive(_objects, item)
                cur_objects = [self._orm_to_entity(_obj) for layer in _objects for _obj in layer]
                cur_objects.insert(0, self._orm_to_entity(item))
                objects.extend(cur_objects)
                _objects = []
            else:
                objects.append(self._orm_to_entity(item))
        return objects

    def create_object(self, item: StorageDTO, parent_hash: str, user_id: int) -> StorageDTO:
        user = self.get_user(user_id)
        parent_obj = self._get_object(user_id, parent_hash)
        if not parent_obj.is_dir:
            raise NotCorrectTypeError(f"Object ${parent_obj.path} is not directory")

        obj_path = self.object_path_factory.compose(obj_path=item.path, bucket_name=item.bucket_name).getFullPath()
        item_hash = self.calculate_hash(obj_path)

        item = user.storage_items.create(
            user=user,
            path=item.path,
            bucket=item.bucket_name,
            hash=item_hash,
            size=item.size,
            last_modified=datetime.datetime.now() if item.last_modified is None else item.last_modified,
            is_dir=item.is_dir,
            user_id=user_id,
            name=item.name,
            parent=parent_obj
        )
        return self._orm_to_entity(item)

    def create_root_folder(self, item: StorageDTO):
        obj_path = self.object_path_factory.compose(bucket_name=item.bucket_name, user_id=item.user_id, obj_path=item.path)
        item_hash = self.calculate_hash(obj_path.getFullPath())
        user = self.get_user(item.user_id)
        root_item = RootStorageItem.objects.create(
            user=user,
            path=item.path,
            bucket=item.bucket_name,
            hash=item_hash,
            size=item.size,
            last_modified=datetime.datetime.now() if item.last_modified is None else item.last_modified,
            is_dir=item.is_dir,
            user_root=user,
            name=item.name,
        )
        user.root_item = root_item
        return self._orm_to_entity(user.root_item)

    # TODO: create transaction
    def delete_object(self, user_id: int, item_hash: str) -> List[StorageDTO]:

        item: StorageItem = self._get_object(user_id, item_hash)
        items: List[List[StorageItem]] = [[item]]
        self._list_objects_recursive(items, item)
        deleted_objects: List[StorageDTO] = []
        for level in items:
            for obj in level:
                deleted_objects.append(self._orm_to_entity(obj))
                obj.delete()
        return deleted_objects

    # TODO: Refactor
    def rename_object(self, user_id: int, item_hash: str, new_name: str) -> StorageDTO:
        item: StorageItem = self._get_object(user_id, item_hash)
        parent: StorageItem = item.parent
        new_path = parent.path + new_name
        base_path = item.path
        if (item.is_dir and not is_folder(new_name)) or (not item.is_dir and is_folder(new_name)):
            raise NotCorrectTypeError(f"Object and name have different type")
        items: List[List[StorageItem]] = [[item]]
        self._list_objects_recursive(items, item)
        for level in items:
            for obj in level:
                relative_path = get_relative_path(obj.path, base_path)
                if item == obj:
                    relative_path = ''
                new_object_path = new_path + relative_path
                obj.name = obj.name if not relative_path == '' else get_object_name(new_name)
                obj.path = new_object_path
                obj.hash = self.calculate_hash(new_object_path)
                obj.save()
        return self._orm_to_entity(item)
