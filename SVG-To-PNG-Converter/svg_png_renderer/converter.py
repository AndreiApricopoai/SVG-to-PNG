from abc import ABC, abstractmethod
from .deserialization import DeserializedObject


class Converter(ABC):
    """
    Abstract base class that represents a converter.

    This class is intended to be subclassed with implementations that convert
    deserialized objects into a specified format and save them to a file.

    Attributes:
        deserialized_objects (list[DeserializedObject]): A list of deserialized objects
        that represent the file to be converted.
        output_file_path (str): The path to the file where the converted output will be saved.
    """

    def __init__(
            self,
            deserialized_objects: list[DeserializedObject],
            output_file_path: str
    ):
        """
        Initializes the Converter with deserialized objects and an output file path.

        Params:
            deserialized_objects (list[DeserializedObject]): A list of deserialized objects
            that represent the file to be converted.
            output_file_path (str): The path to the file where the converted output will be saved.
        """
        self.deserialized_objects = deserialized_objects
        self.output_file_path = output_file_path

    @abstractmethod
    def convert(self):
        """
        Abstract method to be implemented by subclasses for conversion.

        This method should contain the logic to convert the deserialized objects
        into the desired format and save them to the specified output file path.
        """
        pass
