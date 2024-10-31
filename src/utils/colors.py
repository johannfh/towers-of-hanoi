from typing import List
import pygame

def generate_gradient(
    origin: pygame.Color, target: pygame.Color, n: int
) -> List[pygame.Color]:
    assert n >= 0, "n must not be negative"
    if n == 0:
        return []
    if n == 1:
        return [origin]

    step = 1 / (n - 1)
    return [origin.lerp(target, step * i) for i in range(0, n)]

def invert(color: pygame.Color) -> pygame.Color:
    """Inverts a color, e.g. `#000000` -> `#ffffff`"""

    return pygame.Color(
        r=255 - color.r,
        g=255 - color.g,
        b=255 - color.b,
    )

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
