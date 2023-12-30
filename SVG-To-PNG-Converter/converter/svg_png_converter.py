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

    def __get_float(self, svg_object: SvgDeserializedObject, attribute_name: str, default: float = 0):
        try:
            return float(self.__extract_attribute_value(svg_object, attribute_name))
        except ValueError:
            return default

    def __get_string(self, svg_object: SvgDeserializedObject, attribute_name: str, default: str = None):
        value = self.__extract_attribute_value(svg_object, attribute_name)
        if value == '':
            return default
        return value


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
        cx = self.__get_float(circle_object, 'cx', default=0)
        cy = self.__get_float(circle_object, 'cy', default=0)
        r = self.__get_float(circle_object, 'r', default=0)

        stroke = self.__get_string(circle_object, 'stroke', default='black')
        stroke_width = self.__get_float(circle_object, 'stroke-width', default=1)
        stroke_opacity = self.__get_float(circle_object, 'stroke-opacity', default=255)
        fill = self.__get_string(circle_object, 'fill', default='none')
        fill_opacity = self.__get_float(circle_object, 'fill-opacity', default=255)

        try:
            # Convert stroke color to RGBA if necessary
            if stroke_opacity < 255:
                color_rgb = ImageColor.getcolor(stroke, "RGB")
                stroke = color_rgb + (stroke_opacity,)

            # Convert fill color to RGBA if necessary
            if fill_opacity < 255 and fill != 'none':
                fill_rgb = ImageColor.getcolor(fill, "RGB")
                fill = fill_rgb + (fill_opacity,)
            elif fill == 'none':
                fill = None  # No fill

            # Calculate bounding box for circle
            left = cx - r
            top = cy - r
            right = cx + r
            bottom = cy + r

            # Draw the circle
            self.draw.ellipse([left, top, right, bottom], outline=stroke, fill=fill, width=stroke_width)

        except ValueError as ve:
            print(f"Could not process circle attributes: {ve}")
        except Exception as e:
            print(f"Could not draw the circle: {e}")

    def __draw_ellipse(self, ellipse_object: SvgDeserializedObject):
        pass

    def __draw_line(self, line_object: SvgDeserializedObject):
        x1 = self.__get_float(line_object, 'x1', default=0)
        y1 = self.__get_float(line_object, 'y1', default=0)
        x2 = self.__get_float(line_object, 'x2', default=0)
        y2 = self.__get_float(line_object, 'y2', default=0)

        stroke = self.__get_string(line_object, 'stroke', default='black')
        stroke_width = self.__get_float(line_object, 'stroke-width', default=1)
        stroke_opacity = self.__get_float(line_object, 'stroke-opacity', default=255)

        try:
            if stroke_opacity < 255:
                color_rgb = ImageColor.getcolor(stroke, "RGB")
                stroke = color_rgb + (stroke_opacity,)

            self.draw.line((x1, y1, x2, y2), fill=stroke, width=stroke_width)

        except ValueError as ve:
            print(f"Could not process stroke attributes: {ve}")
        except Exception as e:
            print(f"Could not draw the line: {e}")

    def __draw_polyline(self, polyline_object: SvgDeserializedObject):
        pass

    def __draw_path(self, path_object: SvgDeserializedObject):
        pass
