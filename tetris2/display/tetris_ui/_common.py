from os import PathLike
from typing import IO, Sequence, Tuple, Union

from pygame.color import Color
from pygame.math import Vector2

AnyPath = Union[str, bytes, PathLike[str], PathLike[bytes]]

FileArg = Union[AnyPath, IO[bytes], IO[str]]

Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]
Size = Union[Tuple[float, float], Sequence[float], Vector2]

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]