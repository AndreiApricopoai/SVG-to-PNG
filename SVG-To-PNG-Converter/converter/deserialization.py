from abc import ABC, abstractmethod


class DeserializedObject(ABC):
    @abstractmethod
    def __str__(self):
        pass


class Deserializer(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def deserialize(self) -> list[DeserializedObject]:
        pass
