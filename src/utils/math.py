import typing


class Comparable(typing.Protocol):
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...

    def __le__(self, other: object) -> bool:
        return self < other or self == other

    def __ge__(self, other: object) -> bool:
        return self > other or self == other


C = typing.TypeVar("C", bound=Comparable)


def clamp(n: C, min: C, max: C):
    if n < min:
        return min
    if n > max:
        return max
    return n


def lerp(source: float, dest: float, weight: float) -> float:
    LOWER = 0
    UPPER = 1

    # prevent weird effects if `source` or `dest` is out of bounds
    if weight < LOWER:
        return source
    if weight > UPPER:
        return dest

    return source + (dest - source) * weight


def move_linear(from_val: float, to_val: float, n: int, i: int) -> float:
    """`n` should be `1` greater than `i` at the end"""

    step_size = (to_val - from_val) / n
    return from_val + step_size * i
