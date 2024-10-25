import typing
import pygame


def lerp(source: float, dest: float, weight: float) -> float:
    LOWER = 0
    UPPER = 1

    # prevent weird effects if `source` or `dest` is out of bounds
    if weight < LOWER:
        return source
    if weight > UPPER:
        return dest

    return source + (dest - source) * weight


def get_center(screen: pygame.Surface) -> pygame.Vector2:
    return pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


def get_mouse_position() -> pygame.Vector2:
    return pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


def generate_gradient(
    origin: pygame.color.Color, target: pygame.color.Color, n: int
) -> typing.List[pygame.color.Color]:
    assert n >= 2, "n is too small"

    step = 1 / (n - 1)
    return [origin.lerp(target, step * i) for i in range(0, n)]
