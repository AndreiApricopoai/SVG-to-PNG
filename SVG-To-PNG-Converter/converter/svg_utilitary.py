from converter.svg_deserialization import SvgDeserializedObject


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
