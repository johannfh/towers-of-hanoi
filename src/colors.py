"""Contains constants for different colors. (r, g, b)"""

import typing
from pygame import Color

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)

RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
PURPLE = Color(255, 0, 255)


def generate_gradient(origin: Color, target: Color, n: int) -> typing.List[Color]:
    assert n >= 2, "n is too small"

    step = 1 / (n - 1)
    return [origin.lerp(target, step * i) for i in range(0, n)]


def invert(color: Color) -> Color:
    """Inverts a color, e.g. `#000000` -> `#ffffff`"""

    return Color(
        r=255 - color.r,
        g=255 - color.g,
        b=255 - color.b,
    )
