from .svg_deserialization import SvgDeserializedObject
from PIL import ImageColor


class SvgUtility:
    """
    A class that provides static utility methods for processing SVG objects.
    """
    @staticmethod
    def __extract_attribute_value(
            svg_object: SvgDeserializedObject,
            attribute_name: str
    ) -> str:
        """
        Extracts the value of an attribute from an SvgDeserializedObject.

        Params:
            svg_object (SvgDeserializedObject): The object from which the attribute value will be extracted.
            attribute_name (str): The name of the attribute to be extracted.

        Returns:
            str: The value of the attribute if it exists, otherwise an empty string.
        """
        for attribute in svg_object.attributes:
            if attribute.name == attribute_name:
                return attribute.value
        return ''

    @staticmethod
    def get_float(
            svg_object: SvgDeserializedObject,
            attribute_name: str,
            default: float = 0
    ) -> float:
        """
        Extracts the value of an attribute from an SvgDeserializedObject and converts it to a float.

        Params:
            svg_object (SvgDeserializedObject): The object from which the attribute value will be extracted.
            attribute_name (str): The name of the attribute to be extracted.
            default (float): The default value to be returned if the attribute does not exist.

        Returns:
            float: The value of the attribute if it exists, otherwise the default value of 0.
        """
        try:
            return float(SvgUtility.__extract_attribute_value(svg_object, attribute_name))
        except ValueError:
            return default

    @staticmethod
    def get_string(
            svg_object: SvgDeserializedObject,
            attribute_name: str,
            default: str = None
    ) -> str:
        """
        Extracts the value of an attribute from an SvgDeserializedObject as a string.

        Params:
            svg_object (SvgDeserializedObject): The object from which the attribute value will be extracted.
            attribute_name (str): The name of the attribute to be extracted.
            default (str): The default value to be returned if the attribute does not exist.

        Returns:
            str: The value of the attribute if it exists, otherwise the default value of None.
        """
        value = SvgUtility.__extract_attribute_value(svg_object, attribute_name)
        if value == '':
            return default
        return value

    @staticmethod
    def get_int(
            svg_object: SvgDeserializedObject,
            attribute_name: str,
            default: int = 0
    ) -> int:
        """
        Extracts the value of an attribute from an SvgDeserializedObject and converts it to an int.

        Params:
            svg_object (SvgDeserializedObject): The object from which the attribute value will be extracted.
            attribute_name (str): The name of the attribute to be extracted.
            default (int): The default value to be returned if the attribute does not exist.

        Returns:
            int: The value of the attribute if it exists, otherwise the default value of 0.
        """
        try:
            return int(SvgUtility.__extract_attribute_value(svg_object, attribute_name))
        except ValueError:
            return default

    @staticmethod
    def process_color_and_opacity(
            obj: SvgDeserializedObject,
            attribute_name,
            default_color=None,
            default_opacity=1
    ):
        """
        Processes the color and opacity attributes of an SvgDeserializedObject.

        Params:
            obj (SvgDeserializedObject): The object from which the attributes will be extracted.
            attribute_name (str): The name of the attribute to be processed.
            default_color (str): The default color to be returned if the color attribute does not exist.
            default_opacity (float): The default opacity to be returned if the opacity attribute does not exist.

        Returns:
            tuple: A tuple of the RGBA value if the attributes exist, otherwise None.
        """
        color = SvgUtility.get_string(obj, attribute_name, default=default_color)
        opacity = SvgUtility.get_float(
            obj,
            f'{attribute_name}-opacity',
            default=default_opacity
        )
        try:
            if 0 <= opacity <= 1:
                opacity = int(opacity * 255)
                color_rgb = ImageColor.getcolor(color, "RGB")
                return color_rgb + (opacity,)
            return None
        except ValueError as ve:
            print(f"Could not process {attribute_name} attributes: {ve}")
