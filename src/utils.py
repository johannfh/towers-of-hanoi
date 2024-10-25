import time
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


def create_timepassed(seconds: float):
    """ Creates a function that returns `True` if
    the time since the last call returning `True` is
    longer than `seconds`. Returns `False` otherwise."""

    last_has_passed = time.time()

    def has_passed() -> bool:
        """Returns `True` if the specified time
        since the last call returning `True`
        has passed. Returns `False` otherwise."""

        nonlocal last_has_passed
        current_time = time.time()
        if current_time - last_has_passed >= seconds:
            last_has_passed = time.time()
            return True
        return False

    return has_passed
