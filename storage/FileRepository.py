from abc import ABC, abstractmethod
from storage.ObjectPath import ObjectPath
import io


class FileRepository(ABC):

    @abstractmethod
    def isObjectExist(self, file_path: ObjectPath):
        pass

    @abstractmethod
    def createFile(self, file_path: ObjectPath, name: str, data: io.BytesIO):
        pass

    @abstractmethod
    def createFolder(self, folder_path: ObjectPath, name: str):
        pass

    @abstractmethod
    def deleteFolder(self, folder_path: ObjectPath):
        pass

    @abstractmethod
    def deleteFile(self, file_path: ObjectPath):
        pass

    @abstractmethod
    def renameFolder(self, item_path: ObjectPath, new_path: ObjectPath):
        pass

    @abstractmethod
    def renameFile(self, item_path: ObjectPath, new_path: ObjectPath):
        pass

    @abstractmethod
    def moveFile(self, str_path: ObjectPath, destination_path: ObjectPath):
        pass

    @abstractmethod
    def moveFolder(self, src_path: ObjectPath, destination_path: ObjectPath):
        pass

    @abstractmethod
    def copyFolder(self):
        pass

    @abstractmethod
    def copyFile(self):
        pass

    @abstractmethod
    def listFolderObjects(self, folder_path: ObjectPath):
        pass

    @abstractmethod
    def getFileContent(self, fil: ObjectPath):
        pass