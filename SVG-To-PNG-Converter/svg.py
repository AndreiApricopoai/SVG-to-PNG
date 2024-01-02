import svg_png_renderer as svg

deserializer = svg.SvgDeserializer('file.svg')
deserialized_elements = deserializer.deserialize()
path = 'C:\\Users\\Andrei\\Desktop\\SVG-to-PNG\\SVG-To-PNG-Converter\\image.png'
converter = svg.SvgPngConverter(deserialized_elements, (500, 500), path)
converter.convert()

