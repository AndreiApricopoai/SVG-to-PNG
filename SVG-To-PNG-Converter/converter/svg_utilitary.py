from converter.svg_deserialization import SvgDeserializedObject
from PIL import ImageColor


class SvgUtility:
    @staticmethod
    def __extract_attribute_value(svg_object: SvgDeserializedObject, attribute_name: str) -> str:
        for attribute in svg_object.attributes:
            if attribute.name == attribute_name:
                return attribute.value
        return ''

    @staticmethod
    def get_float(svg_object: SvgDeserializedObject, attribute_name: str, default: float = 0):
        try:
            return float(SvgUtility.__extract_attribute_value(svg_object, attribute_name))
        except ValueError:
            return default

    @staticmethod
    def get_string(svg_object: SvgDeserializedObject, attribute_name: str, default: str = None):
        value = SvgUtility.__extract_attribute_value(svg_object, attribute_name)
        if value == '':
            return default
        return value

    @staticmethod
    def get_int(svg_object: SvgDeserializedObject, attribute_name: str, default: int = 0):
        try:
            return int(SvgUtility.__extract_attribute_value(svg_object, attribute_name))
        except ValueError:
            return default

    @staticmethod
    def process_color_and_opacity(obj: SvgDeserializedObject, attribute_name, default_color=None,
                                    default_opacity=1):
        color = SvgUtility.get_string(obj, attribute_name, default=default_color)
        opacity = SvgUtility.get_float(obj, f'{attribute_name}-opacity', default=default_opacity)
        try:
            if 0 <= opacity <= 1:
                opacity = int(opacity * 255)
                color_rgb = ImageColor.getcolor(color, "RGB")
                return color_rgb + (opacity,)
            return None
        except ValueError as ve:
            print(f"Could not process {attribute_name} attributes: {ve}")
