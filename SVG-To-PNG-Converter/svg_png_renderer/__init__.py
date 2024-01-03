"""
This package provides classes for deserializing SVG files and converting them into PNG format.

It includes:
- `SvgDeserializer`: A class for parsing SVG files and turning them into python objects containing relevant information.
- `SvgPngConverter`: A class for converting deserialized SVG objects into PNG images.
"""

from .svg_deserialization import SvgDeserializer
from .svg_png_converter import SvgPngConverter

__all__ = ['SvgDeserializer', 'SvgPngConverter']
