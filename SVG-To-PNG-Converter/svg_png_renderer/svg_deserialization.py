import os
import xml.etree.ElementTree as ET
from .deserialization import Deserializer, DeserializedObject


class Attribute:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.name}="{self.value}"'


class SvgDeserializedObject(DeserializedObject):
    def __init__(self, tag_name: str):
        self.attributes = []
        self.tag_name = tag_name

    def add_attribute(self, attribute: Attribute):
        for i, attr in enumerate(self.attributes):
            if attr.name == attribute.name:
                self.attributes[i] = attribute
                return
        self.attributes.append(attribute)

    def __str__(self) -> str:
        attributes_str = ''
        for attribute in self.attributes:
            attributes_str += str(attribute) + ' '
        attributes_str = attributes_str.strip()
        return f'<{self.tag_name} {attributes_str}/>'


class SvgDeserializer(Deserializer):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def deserialize(self) -> list[SvgDeserializedObject]:
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
