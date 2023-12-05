from storage.ObjectPathFactory import ObjectPathFactory
from storage.minio.MinioObjectPath import MinioObjectPath


class MinioObjectFactory(ObjectPathFactory):

    @classmethod
    def compose(cls, **kwargs) -> MinioObjectPath:
        return MinioObjectPath.compose(**kwargs)