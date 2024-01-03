import sys
import svg_png_renderer as svg


def main():
    if len(sys.argv) != 2:
        print("Usage: python svg.py <filename>.svg")
        sys.exit(1)

    filename = sys.argv[1]

    deserializer = svg.SvgDeserializer(filename)
    deserialized_elements = deserializer.deserialize()
    path = 'image.png'
    converter = svg.SvgPngConverter(deserialized_elements, (500, 500), path)
    converter.convert()


if __name__ == "__main__":
    main()
