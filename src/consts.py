from enum import Enum
from collections import namedtuple

class DrawCommand(Enum):
    MOVETO = 0
    LINETO = 1
    QUADRATICTO = 2

Edge = namedtuple("Edge", ["type", "data", "S"])
Path = namedtuple("Path", ["edges", "stroke", "fill0", "fill1"])
Shape = namedtuple("Shape", ["palette","transformation_pt", "trans_mat", "paths"])
Point = namedtuple("Point", ["x", "y"])
StrokeStyle = namedtuple("Stroke", ["color", "scaleMode", "caps", "weight", "joints", "miterLimit"])
FillStyle = namedtuple("Fill", ["color", "alpha"])
SYMBOLS = [
    r"\s*\!(-*\d+\.*\d*)\s+(-*\d+\.*\d*)\s*",
    r"\s*[\|\/](-*\d+\.*\d*)\s+(-*\d+\.*\d*)\s*",
    r"\s*[\[\]]((?:\#[0-9A-F]{1,6}\.[0-9A-F]{1,2})|(?:-*\d+\.*\d*))\s+((?:\#[0-9A-F]{1,6}\.[0-9A-F]{1,2})|(?:-*\d+\.*\d*))\s+((?:\#[0-9A-F]{1,6}\.[0-9A-F]{1,2})|(?:-*\d+\.*\d*))\s+((?:\#[0-9A-F]{1,6}\.[0-9A-F]{1,2})|(?:-*\d+\.*\d*))\s*",
    r"S\d{1}"
]