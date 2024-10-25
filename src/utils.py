import time
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


def create_timepassed(seconds: float):
    """Creates a function that returns `True` if
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


class Comparable(typing.Protocol):
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...

    def __le__(self, other: object) -> bool:
        return self < other or self == other

    def __ge__(self, other: object) -> bool:
        return self > other or self == other


T = typing.TypeVar("T", bound=Comparable)


def clamp(n: T, min: T, max: T):
    if n < min:
        return min
    if n > max:
        return max
    return n


class Queue[T]:
    """A really simple generic `Queue` implementation"""

    __items: typing.List[T] = []
    """The items in the `Queue`. """

    def __init__(self):
        pass

    def enqueue(self, *items: T) -> None:
        """Add new items to the `Queue`"""
        for item in items:
            self.__items.append(item)

    def dequeue(self) -> T:
        """Remove and return the next element in `Queue`.
        Raises `IndexError` if the `Queue` is empty."""
        return self.__items.pop(0)

    def peek(self) -> T:
        """Return the next element in `Queue` without removing it.
        Raises `IndexError` if the `Queue` is empty."""
        return self.__items[0]

    def empty(self) -> bool:
        """Check if the `Queue` is empty."""
        return len(self.__items) == 0

    def clear(self) -> typing.List[T]:
        """Remove and return **ALL** items from the `Queue`."""
        items = self.__items
        self.__items = []
        return items
