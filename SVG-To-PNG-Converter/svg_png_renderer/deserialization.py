from abc import ABC, abstractmethod


class DeserializedObject(ABC):
    """
    Abstract base class that represents a deserialized object.

    This class is intended to be subclassed with implementations specific to a
    file format being deserialized.
    """
    @abstractmethod
    def __str__(self):
        """
        This method will return the string representation of the deserialized object
        and needs to be implemented by subclasses for their specific file format.
        """
        pass


class Deserializer(ABC):
    """
    Abstract base class that represents a deserializer that converts
    the file into a list of deserialized objects.

    This class is intended to be subclassed with implementations that deserialize the file
    into deserialized objects that represent the format of the specific file format.

    Attributes:
        file_path (str): The path to the file that needs to be deserialized.
    """
    def __init__(self, file_path: str):
        """
        Initializes the Deserializer with the path of the file that needs to be deserialized.

        Params:
        file_path (str): The path to the file that needs to be deserialized.
        """
        self.file_path = file_path

    @abstractmethod
    def deserialize(self) -> list[DeserializedObject]:
        """
        Abstract method to be implemented by subclasses for deserialization.
        This method should contain the logic to deserialize the file into a list of deserialized objects.

        Returns:
            list[DeserializedObject]: A list of deserialized objects that represent the file.
        """
        pass
