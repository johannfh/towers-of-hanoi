import functools
import typing


class Move:
    source: int
    destination: int

    def __init__(self, source: int, destination: int) -> None:
        self.source = source
        self.destination = destination

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination}"


def print_moves(moves: typing.List[Move]) -> None:
    for move in moves:
        print(move)


@functools.cache
def towers_of_hanoi(
    n: int, source: int, destination: int, auxiliary: int
) -> typing.List[Move]:
    """
    Generate moves to move `n` Disks from tower `source` to `destination` over `auxiliary`.
    """

    assert n > 0, "n has to be greater than 0"

    collision_error_msg = "Identifier collision between towers:"

    assert source != destination, f"{collision_error_msg} source == destination"
    assert source != auxiliary, f"{collision_error_msg} source == auxiliary"
    assert destination != auxiliary, f"{collision_error_msg} destination == auxiliary"

    if n <= 1:
        return [Move(source, destination)]

    moves: typing.List[Move] = []

    moves += [move for move in towers_of_hanoi(n - 1, source, auxiliary, destination)]
    moves.append(Move(source, destination))
    moves += [move for move in towers_of_hanoi(n - 1, auxiliary, destination, source)]

    return moves
