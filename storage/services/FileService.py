from storage.FileRepository import FileRepository
from storage.ObjectPathFactory import ObjectPathFactory
from storage.services.dao.StorageDAO import StorageDAO
from storage.services.dto.StorageItemDTO import StorageDTO
from storage.services.dto.FileDTO import FileDTO
from storage.exceptions import FileServiceError, ObjectExistError, NotCorrectTypeError
from storage.utils import get_filename
import io


class FileService:

    def __init__(self, repository: FileRepository, storage: StorageDAO, object_path_factory: ObjectPathFactory):
        self.repository = repository
        self.storage = storage
        self.object_path_factory = object_path_factory

    def create_empty_file(self, user_id: int, path: str, parent: str):
        pass

    def save_file(self, user_id: int, name: str, parent: str, data: bytes):
        try:
            parent_item = self.storage.get_object(user_id, parent)
            file_path = parent_item.path + name
            self.storage.is_object_exist_errs(user_id, file_path)
            path = self.object_path_factory.compose(user_id=user_id, obj_path=file_path)
            item = self.repository.createFile(path, name, io.BytesIO(data))
            self.storage.create_object(item, parent, user_id)
        except ObjectExistError as e:
            raise
        except Exception as e:
            raise FileServiceError(e)

    def download_file(self, user_id: int, file_hash: str) -> FileDTO:
        try:
            item: StorageDTO = self.storage.get_object(user_id, file_hash)
            path = self.object_path_factory.compose(bucket_name=item.bucket_name, user_id=user_id, obj_path=item.path)
            data = self.repository.getFileContent(path)
            return FileDTO(path=item.name, data=data)
        except Exception:
            raise FileServiceError("Error occur during downloading file")

    def delete_file(self, user_id: int, file_hash: str):
        try:
            item: StorageDTO = self.storage.get_object(user_id, file_hash)
            if item.is_dir:
                raise NotCorrectTypeError
            path = self.object_path_factory.compose(user_id=item.user_id, bucket_name=item.bucket_name, obj_path=item.path)
            self.repository.deleteFile(path)
            self.storage.delete_object(user_id, file_hash)
        except Exception as e:
            raise FileServiceError("Error cannot delete file")

