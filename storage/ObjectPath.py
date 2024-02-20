from abc import ABC, abstractmethod


class ObjectPath(ABC):

    @classmethod
    @abstractmethod
    def compose(cls, **kwargs):
        pass

    @abstractmethod
    def getPartialPath(self):
        pass

    @abstractmethod
    def getParent(self):
        pass

    @abstractmethod
    def isRoot(self):
        pass

    @abstractmethod
    def isFolder(self):
        pass

    @abstractmethod
    def getFullPath(self):
        pass

    @abstractmethod
    def getPath(self):
        pass

    @abstractmethod
    def getBucketName(self):
        pass

