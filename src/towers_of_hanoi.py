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
    n: int, source: int, destination: int, auxilary: int
) -> typing.List[Move]:
    """
    Generate moves to move `n` Disks from tower `source` to `destination` over `auxilary`.
    """

    assert n > 0, "n has to be greater than 0"

    collision_error_msg = "Identifier collision between towers:"

    assert source != destination, f"{collision_error_msg} source == destination"
    assert source != auxilary, f"{collision_error_msg} source == auxilary"
    assert destination != auxilary, f"{collision_error_msg} destination == auxilary"

    moves: typing.List[Move] = []
    if n <= 1:
        moves.append(Move(source, destination))
    else:
        for i in towers_of_hanoi(n - 1, source, auxilary, destination):
            moves.append(i)

        moves.append(Move(source, destination))

        for i in towers_of_hanoi(n - 1, auxilary, destination, source):
            moves.append(i)

    return moves
