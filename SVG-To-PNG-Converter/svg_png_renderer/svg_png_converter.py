from .converter import Converter
from .svg_deserialization import SvgDeserializedObject
from .svg_utilitary import SvgUtility
from PIL import Image, ImageDraw, ImageColor


class SvgPngConverter(Converter):
    def __init__(self, svg_deserialized_objects: list[SvgDeserializedObject], output_dim: tuple[int, int] = (500, 500),
                 output_file_path: str = 'output.png'):
        super().__init__(svg_deserialized_objects, output_file_path)
        self.deserialized_objects: list[SvgDeserializedObject] = svg_deserialized_objects
        self.output_dim = output_dim
        self.image = Image.new("RGBA", self.output_dim, "WHITE")
        self.draw = ImageDraw.Draw(self.image)

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
            print('Image saved successfully')
        except Exception as e:
            print(f'Could not save the image: {e}')

    def __draw_rect(self, rect_object: SvgDeserializedObject):
        x = SvgUtility.get_float(rect_object, 'x', default=0)
        y = SvgUtility.get_float(rect_object, 'y', default=0)
        width = SvgUtility.get_float(rect_object, 'width', default=0)
        height = SvgUtility.get_float(rect_object, 'height', default=0)
        stroke_width = SvgUtility.get_int(rect_object, 'stroke-width', default=1)

        stroke = SvgUtility.process_color_and_opacity(rect_object, 'stroke')
        fill = SvgUtility.process_color_and_opacity(rect_object, 'fill', default_color='none')

        bottom_right_x = x + width
        bottom_right_y = y + height

        try:
            self.draw.rectangle((x, y, bottom_right_x, bottom_right_y), outline=stroke, fill=fill, width=stroke_width)
        except Exception as e:
            print(f"Could not draw the rectangle: {e}")

    def __draw_circle(self, circle_object: SvgDeserializedObject):
        cx = SvgUtility.get_float(circle_object, 'cx', default=0)
        cy = SvgUtility.get_float(circle_object, 'cy', default=0)
        r = SvgUtility.get_float(circle_object, 'r', default=0)
        stroke_width = SvgUtility.get_int(circle_object, 'stroke-width', default=1)

        stroke = SvgUtility.process_color_and_opacity(circle_object, 'stroke')
        fill = SvgUtility.process_color_and_opacity(circle_object, 'fill', default_color='none')

        left = cx - r
        top = cy - r
        right = cx + r
        bottom = cy + r

        try:
            self.draw.ellipse([left, top, right, bottom], outline=stroke, fill=fill, width=stroke_width)
        except Exception as e:
            print(f"Could not draw the circle: {e}")

    def __draw_ellipse(self, ellipse_object: SvgDeserializedObject):
        cx = SvgUtility.get_float(ellipse_object, 'cx', default=0)
        cy = SvgUtility.get_float(ellipse_object, 'cy', default=0)
        rx = SvgUtility.get_float(ellipse_object, 'rx', default=0)
        ry = SvgUtility.get_float(ellipse_object, 'ry', default=0)
        stroke_width = SvgUtility.get_int(ellipse_object, 'stroke-width', default=1)

        stroke = SvgUtility.process_color_and_opacity(ellipse_object, 'stroke')
        fill = SvgUtility.process_color_and_opacity(ellipse_object, 'fill', default_color='none')

        left = cx - rx
        top = cy - ry
        right = cx + rx
        bottom = cy + ry

        try:
            self.draw.ellipse([left, top, right, bottom], outline=stroke, fill=fill, width=stroke_width)
        except Exception as e:
            print(f"Could not draw the ellipse: {e}")

    def __draw_line(self, line_object: SvgDeserializedObject):
        x1 = SvgUtility.get_float(line_object, 'x1', default=0)
        y1 = SvgUtility.get_float(line_object, 'y1', default=0)
        x2 = SvgUtility.get_float(line_object, 'x2', default=0)
        y2 = SvgUtility.get_float(line_object, 'y2', default=0)
        stroke_width = SvgUtility.get_int(line_object, 'stroke-width', default=1)
        stroke = SvgUtility.process_color_and_opacity(line_object, 'stroke')

        try:
            self.draw.line([x1, y1, x2, y2], fill=stroke, width=stroke_width)
        except Exception as e:
            print(f"Could not draw the line: {e}")

    def __draw_polyline(self, polyline_object: SvgDeserializedObject):
        points = SvgUtility.get_string(polyline_object, 'points', default='')
        stroke_width = SvgUtility.get_int(polyline_object, 'stroke-width', default=1)
        stroke = SvgUtility.process_color_and_opacity(polyline_object, 'stroke')

        try:
            polyline_points = []
            for point in points.split():
                x, y = map(float, point.split(','))
                polyline_points.append((x, y))

            if polyline_points:
                self.draw.line(polyline_points, fill=stroke, width=stroke_width, joint='curve')
        except Exception as e:
            print(f"Could not draw the polyline: {e}")

    def __draw_path(self, path_object: SvgDeserializedObject):
        path_data = SvgUtility.get_string(path_object, 'd', default='')
        stroke_width = SvgUtility.get_int(path_object, 'stroke-width', default=1)
        stroke = SvgUtility.process_color_and_opacity(path_object, 'stroke')

        current_x, current_y = 0, 0

        split_data = path_data.split()
        command_segments = []
        for i in range(len(split_data)):
            if split_data[i] == 'M':
                command_segments.append(('M', split_data[i + 1], split_data[i + 2]))
            elif split_data[i] == 'L':
                command_segments.append(('L', split_data[i + 1], split_data[i + 2]))
        try:
            for segment in command_segments:
                if segment[0] == 'M':
                    current_x = float(segment[1])
                    current_y = float(segment[2])
                elif segment[0] == 'L':
                    end_x = float(segment[1])
                    end_y = float(segment[2])
                    self.draw.line((current_x, current_y, end_x, end_y), fill=stroke, width=stroke_width)
                    current_x, current_y = end_x, end_y
        except ValueError as ve:
            print(f"Could not process path attributes: {ve}")
        except Exception as e:
            print(f"Could not draw the path: {e}")
