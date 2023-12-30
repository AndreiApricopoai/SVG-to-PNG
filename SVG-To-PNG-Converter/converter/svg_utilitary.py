from converter.svg_deserialization import SvgDeserializedObject


class SvgUtility:
    @staticmethod
    def extract_attribute_value(self, svg_object: SvgDeserializedObject, attribute_name: str) -> str:
        for attribute in svg_object.attributes:
            if attribute.name == attribute_name:
                return attribute.value
        return ''

    @staticmethod
    def get_float(self, svg_object: SvgDeserializedObject, attribute_name: str, default: float = 0):
        try:
            return float(self.extract_attribute_value(svg_object, attribute_name))
        except ValueError:
            return default

    @staticmethod
    def get_string(self, svg_object: SvgDeserializedObject, attribute_name: str, default: str = None):
        value = self.extract_attribute_value(svg_object, attribute_name)
        if value == '':
            return default
        return value

    @staticmethod
    def get_int(self, svg_object: SvgDeserializedObject, attribute_name: str, default: int = 0):
        try:
            return int(self.extract_attribute_value(svg_object, attribute_name))
        except ValueError:
            return default
