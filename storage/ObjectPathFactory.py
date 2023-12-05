from abc import ABC, abstractmethod
from storage.ObjectPath import ObjectPath


class ObjectPathFactory:

    @classmethod
    @abstractmethod
    def compose(cls, **kwargs) -> ObjectPath:
        pass
