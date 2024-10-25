"""Contains constants for different colors. (r, g, b)"""

import typing
from pygame import Color

BLACK = Color(0, 0, 0)
"""`#000000`"""
WHITE = Color(255, 255, 255)
"""`#ffffff`"""

RED = Color(255, 0, 0)
"""`#ff0000`"""
GREEN = Color(0, 255, 0)
"""`#00ff00`"""
BLUE = Color(0, 0, 255)
"""`#0000ff`"""

YELLOW = Color(255, 255, 0)
"""`#ffff00`"""
CYAN = Color(0, 255, 255)
"""`#00ffff`"""
PURPLE = Color(255, 0, 255)
"""`#ff00ff`"""


def generate_gradient(origin: Color, target: Color, n: int) -> typing.List[Color]:
    assert n >= 0, "n must not be negative"
    if n == 0:
        return []
    if n == 1:
        return [origin]

    step = 1 / (n - 1)
    return [origin.lerp(target, step * i) for i in range(0, n)]


def invert(color: Color) -> Color:
    """Inverts a color, e.g. `#000000` -> `#ffffff`"""

    return Color(
        r=255 - color.r,
        g=255 - color.g,
        b=255 - color.b,
    )
