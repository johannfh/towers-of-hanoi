from typing import List
from .move import Move


def towers_of_hanoi(
    n: int, source: int, destination: int, auxiliary: int
) -> List[Move]:
    if n == 1:
        return [Move(source, destination)]
    moves: List[Move] = []

    moves += towers_of_hanoi(n - 1, source, auxiliary, destination)
    moves.append(Move(source, destination))
    moves += towers_of_hanoi(n - 1, auxiliary, destination, source)

    return moves
