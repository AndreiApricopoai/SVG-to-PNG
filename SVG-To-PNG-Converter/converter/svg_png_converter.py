from converter.converter import Converter
from converter.svg_deserialization import SvgDeserializedObject
from PIL import Image, ImageDraw, ImageColor


class SvgPngConverter(Converter):
    def __init__(self, svg_deserialized_objects: list[SvgDeserializedObject], output_dim: tuple[int, int] = (500, 500),
                 output_file_path: str = 'output.png'):
        super().__init__(svg_deserialized_objects, output_file_path)
        self.deserialized_objects: list[SvgDeserializedObject] = svg_deserialized_objects
        self.output_dim = output_dim
        self.image = Image.new("RGBA", self.output_dim, "WHITE")
        self.draw = ImageDraw.Draw(self.image)

    def __extract_attribute_value(self, svg_object: SvgDeserializedObject, attribute_name: str) -> str:
        for attribute in svg_object.attributes:
            if attribute.name == attribute_name:
                return attribute.value
        return ''

    def convert(self):
        for svg_deserialized_object in self.deserialized_objects:
            if svg_deserialized_object.tag_name == 'svg':
                print('Drawing svg...')
            elif svg_deserialized_object.tag_name == 'rect':
                self.__draw_rect(svg_deserialized_object)
            elif svg_deserialized_object.tag_name == 'circle':
                self.__draw_circle(svg_deserialized_object)
            elif svg_deserialized_object.tag_name == 'ellipse':
                self.__draw_ellipse(svg_deserialized_object)
            elif svg_deserialized_object.tag_name == 'line':
                self.__draw_line(svg_deserialized_object)
            elif svg_deserialized_object.tag_name == 'polyline':
                self.__draw_polyline(svg_deserialized_object)
            elif svg_deserialized_object.tag_name == 'path':
                self.__draw_path(svg_deserialized_object)
            else:
                print(f'Unknown tag name: {svg_deserialized_object.tag_name} -> could not draw the element')
        try:
            self.image.save(self.output_file_path)
        except Exception as e:
            print(f'Could not save the image: {e}')

    def __draw_rect(self, rect_object: SvgDeserializedObject):
        pass

    def __draw_circle(self, circle_object: SvgDeserializedObject):
        pass

    def __draw_ellipse(self, ellipse_object: SvgDeserializedObject):
        pass

    def __draw_line(self, line_object: SvgDeserializedObject):
        x1 = float(self.__extract_attribute_value(line_object, 'x1'))
        y1 = float(self.__extract_attribute_value(line_object, 'y1'))
        x2 = float(self.__extract_attribute_value(line_object, 'x2'))
        y2 = float(self.__extract_attribute_value(line_object, 'y2'))

        stroke = self.__extract_attribute_value(line_object, 'stroke')
        stroke_width = float(self.__extract_attribute_value(line_object, 'stroke-width'))
        stroke_opacity = float(self.__extract_attribute_value(line_object, 'stroke-opacity'))

        if stroke_opacity < 255:
            color_rgb = ImageColor.getcolor(stroke, "RGB")
            stroke = color_rgb + (stroke_opacity,)

        try:
            self.draw.line((x1, y1, x2, y2), fill=stroke, width=stroke_width)
        except Exception as e:
            print(f"Could not draw the line: {e}")

    def __draw_polyline(self, polyline_object: SvgDeserializedObject):
        pass

    def __draw_path(self, path_object: SvgDeserializedObject):
        pass
