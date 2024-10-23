import typing
import pygame


def lerp(source: float, dest: float, weight: float) -> float:
    assert weight >= 0 and weight <= 1, "weight has to be between 0 and 1"

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
