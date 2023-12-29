from abc import ABC, abstractmethod
from converter.deserialization import DeserializedObject


class Converter(ABC):
    def __init__(self, deserialized_objects: list[DeserializedObject], output_file_path: str):
        self.deserialized_objects = deserialized_objects
        self.output_file_path = output_file_path

    @abstractmethod
    def convert(self):
        pass
