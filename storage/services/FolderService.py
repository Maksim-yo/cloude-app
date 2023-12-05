import zipfile
import io
from typing import List

from storage.FileRepository import FileRepository
from storage.ObjectPathFactory import ObjectPathFactory
from storage.services.FileService import FileService
from storage.services.dao.StorageDAO import StorageDAO
from storage.services.dto.StorageItemDTO import StorageDTO
from storage.services.dto.ObjectDTO import ObjectDTO
from storage.services.dto.FileDTO import FileDTO
from storage.utils import split_path, get_parent_path, get_filename, is_folder, get_root_directory,\
    compose_path_w_slashes, get_folder_name, get_relative_path
from storage.exceptions import FolderServiceError, ObjectExistError, NotCorrectTypeError


class FolderService:

    def __init__(self, repository: FileRepository, storage: StorageDAO, object_path_factory: ObjectPathFactory):
        self.repository = repository
        self.storage = storage
        self.object_path_factory = object_path_factory
        self.file_service = FileService(self.repository, self.storage, self.object_path_factory)

    def _create_folder_recursive(self, user_id: int, path: str, parent_hash: str) -> StorageDTO:
        parent_item = self.storage.get_object(user_id, parent_hash)
        parent_item_path = self.object_path_factory.compose(user_id=parent_item.user_id,
                                                 obj_path=parent_item.path).getFullPath()
        parent: StorageDTO = parent_item
        folder_paths = split_path(path)
        folder_paths.pop()  # delete filename

        for folder_path in folder_paths:
            # TODO: get rid off bucket_name depends or ...
            _folder_path = self.object_path_factory.compose(user_id=user_id,
                                                     obj_path=parent_item.path + folder_path)

            if self.storage.is_object_existp(user_id, parent_item.path + folder_path):
                parent = self.storage.get_object_by_path(user_id, parent_item.path + folder_path)
                continue
            parent_folder = self.repository.createFolder(_folder_path, get_folder_name(folder_path))
            parent = self.storage.create_object(parent_folder, parent.hash, user_id)
        return parent

    def _convert_dto(self, item: StorageDTO) -> ObjectDTO:
        return ObjectDTO(
            name=item.name,
            path=item.path,
            size=item.size,
            last_modified=item.last_modified,
            is_dir=item.is_dir,
            hash=item.hash,
        )

    def get_root_folder(self, user_id: int) -> StorageDTO:
        return self.storage.get_root_object(user_id)

    def save_root_folder(self, user_id: int, name: str):
        folder_path = self.object_path_factory.compose(user_id=user_id, obj_path=name)
        folder = self.repository.createFolder(folder_path, name)
        folder.user_id = user_id
        self.storage.create_root_folder(folder)

    def save_empty_folder(self, user_id: int, parent: str, name: str) -> StorageDTO:
        parent_item = self.storage.get_object(user_id, parent)
        folder_path = self.object_path_factory.compose(user_id=user_id, obj_path=parent_item.path + name)
        self.storage.is_object_exist_errs(user_id, parent_item.path + name)
        folder = self.repository.createFolder(folder_path, name)
        self.storage.create_object(folder, parent, user_id)
        folder.user_id = user_id
        return folder

    def save_folder(self, user_id: int, parent: str, files: List[FileDTO]):
        try:
            folder_name = get_root_directory(files[0].path)
            folder = self.save_empty_folder(user_id, parent, folder_name)

            for file in files:
                file_path = file.path
                _parent = self._create_folder_recursive(user_id, file_path, parent)
                filename = get_filename(file_path)
                self.file_service.save_file(user_id, filename, _parent.hash, file.data)
        except ObjectExistError as e:
            raise
        except Exception as e:
            raise FolderServiceError(e)

    def get_items(self, user_id: int, folder_hash: str) -> List[ObjectDTO]:
        try:
            objects = self.storage.list_objects(user_id, folder_hash)
            return list(map(self._convert_dto, objects))
        except Exception as e:
            raise Exception

    def get_folder(self, user_id: int, folder_hash: str) -> ObjectDTO:
        try:
            obj = self.storage.get_object(user_id, folder_hash)
            return self._convert_dto(obj)
        except Exception as e:
            raise Exception

    def folder_parents(self, user_id: int, folder_hash: str) -> List[ObjectDTO]:
        try:
            objects = self.storage.object_parents(user_id, folder_hash)
            return list(map(self._convert_dto, objects))
        except Exception as e:
            raise Exception

    def folder_parent(self, user_id: int, folder_hash: str):
        try:
            parent = self.storage.object_parent(user_id, folder_hash)
            return self._convert_dto(parent) if parent else None
        except Exception as e:
            raise Exception

    def download_folder(self, user_id: int, folder_hash: str) -> bytes:

        # try:
            folder = self.storage.get_object(user_id, folder_hash)
            folder_path = self.object_path_factory.compose(bucket_name=folder.bucket_name, user_id=folder.user_id, obj_path=folder.path)
            objects = self.storage.list_objects(user_id, folder_hash, True)
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                for obj in objects:
                    if obj.is_dir:
                        continue
                    file_content = self.file_service.download_file(user_id, obj.hash)
                    path = folder.name + '/' + get_relative_path(obj.path, folder.path)
                    zf.writestr(path, file_content.data)
            return buffer.getvalue()

    def delete_folder(self, user_id: int, folder_hash: str):
        try:
            item: StorageDTO = self.storage.get_object(user_id, folder_hash)
            result: List[StorageDTO] = self.storage.delete_object(user_id, folder_hash)
            for obj in result:
                path = self.object_path_factory.compose(user_id=obj.user_id, bucket_name=obj.bucket_name, obj_path=obj.path)
                if obj.is_dir:
                    self.repository.deleteFolder(path)
                else:
                    self.repository.deleteFile(path)

        except Exception as e:
            raise FolderServiceError("Error cannot delete folder")

    def rename_folder(self, user_id: int, folder_hash: str, new_name: str):

        try:
            item: StorageDTO = self.storage.get_object(user_id, folder_hash)
            new_item = self.storage.rename_object(user_id, folder_hash, new_name)
            item_path = self.object_path_factory.compose(user_id=item.user_id, bucket_name=item.bucket_name, obj_path=item.path)
            new_item_path = self.object_path_factory.compose(user_id=new_item.user_id, obj_path=new_item.path)
            self.repository.renameFolder(item_path, new_item_path)
        except Exception as e:
            raise FolderServiceError("Error cannot delete folder")
