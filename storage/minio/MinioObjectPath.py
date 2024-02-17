from storage.ObjectPath import ObjectPath
from storage.exceptions import ObjectPathError


class MinioObjectPath(ObjectPath):

    def __init__(self, obj_path: str, user_id: int = -1, bucket_name: str = ""):
        self.bucket_name = bucket_name
        self.user_id = str(user_id) if user_id != -1 else ""
        self.obj_path = obj_path

    @classmethod
    def compose(cls, **kwargs):
        try:
            return MinioObjectPath(**kwargs)
        except Exception:
            raise ObjectPathError("Number of arguments/types incorrect")

    def getParent(self):
        pass

    def isRoot(self) -> bool:
        return self.obj_path == '/'

    def isFolder(self) -> bool:
        return self.obj_path.endswith('/')

    def getPartialPath(self):
        if not self.user_id:
            return self.obj_path
        return self.user_id + '/' + self.obj_path

    def getFullPath(self) -> str:
        if not self.bucket_name:
            return self.getPartialPath()
        if not self.user_id:
            return self.bucket_name + '/' + self.obj_path
        return self.bucket_name + '/' + self.user_id + '/' + self.obj_path

    def getPath(self) -> str:
        return self.obj_path

    def getBucketName(self) -> str:
        return self.bucket_name

    def getObjectName(self):
        if self.isFolder() and self.isRoot():
            return self.bucket_name


