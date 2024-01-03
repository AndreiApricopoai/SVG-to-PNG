import os
import xml.etree.ElementTree as ET
from .deserialization import Deserializer, DeserializedObject


class Attribute:
    """
    Represents an attribute of an SVG element.

    Attributes:
        name (str): The name of the attribute.
        value (str): The value of the attribute.
    """
    def __init__(self, name: str, value: str):
        """
        Initializes the Attribute with the name and value.

        Params:
            name (str): The name of the attribute.
            value (str): The value of the attribute.
        """
        self.name = name
        self.value = value

    def __str__(self) -> str:
        """
        Returns the string representation of the attribute.
        """
        return f'{self.name}="{self.value}"'


class SvgDeserializedObject(DeserializedObject):
    """
    A class that represents a deserialized SVG object.

    Attributes:
        tag_name (str): The tag name of the SVG element.
        attributes (list[Attribute]): A list of attributes of the SVG element.
    """
    def __init__(self, tag_name: str):
        """
        Initializes the SVG object with the tag name and the attributes will be
        provided later using the `add_attribute` method that gets called in the
        SVG implementation of the Deserializer.

        Params:
            tag_name (str): The tag name of the SVG element.
        """
        self.attributes: list[Attribute] = []
        self.tag_name = tag_name

    def add_attribute(self, attribute: Attribute):
        """
        Adds an attribute to the list of attributes of the SvgDeserializedObject.
        If an attribute with the same name already exists, it will be replaced.

        Params:
            attribute (Attribute): The attribute to be added.
        """
        for i, attr in enumerate(self.attributes):
            if attr.name == attribute.name:
                self.attributes[i] = attribute
                return
        self.attributes.append(attribute)

    def __str__(self) -> str:
        """
        Returns the string representation of the SvgDeserializedObject.
        """
        attributes_str = ''
        for attribute in self.attributes:
            attributes_str += str(attribute) + ' '
        attributes_str = attributes_str.strip()
        return f'<{self.tag_name} {attributes_str}/>'


class SvgDeserializer(Deserializer):
    """
    A class that represents an SVG deserializer.

    Attributes:
        file_path (str): The path to the svg file that needs to be deserialized.
    """
    def __init__(self, file_path: str):
        """
        Initializes the SvgDeserializer with the path of the svg file that needs to be deserialized.

        Params:
            file_path (str): The path to the svg file that needs to be deserialized.
        """
        super().__init__(file_path)

    def deserialize(self) -> list[SvgDeserializedObject]:
        """
        Deserializes the svg file into a list of SvgDeserializedObjects.
        Iterates over the xml tree and creates a SvgDeserializedObject for each element.

        Returns:
            list[SvgDeserializedObject]: A list of SvgDeserializedObjects that represent the svg file.
        """
        if not self.__is_valid_svg():
            raise Exception('The file is not a valid SVG file')

        tree = ET.parse(self.file_path)
        root = tree.getroot()

        svg_deserialized_elements: list[SvgDeserializedObject] = []
        for element in root.iter():

            tag_name = element.tag
            if '}' in tag_name:
                tag_name = tag_name.split('}')[1]

            svg_element = SvgDeserializedObject(tag_name)
            for name, value in element.attrib.items():
                svg_element.add_attribute(Attribute(name, value))
            svg_deserialized_elements.append(svg_element)

        return svg_deserialized_elements

    def __is_valid_svg(self):
        """
        Checks if the file is a valid SVG file.

        Returns:
            bool: True if the file is a valid SVG file, False otherwise.
        """
        if not os.path.isfile(self.file_path):
            return False

        _, extension = os.path.splitext(self.file_path)
        if extension.lower() != '.svg':
            return False

        try:
            tree = ET.parse(self.file_path)
            tree.getroot()
        except ET.ParseError:
            return False

        return True
