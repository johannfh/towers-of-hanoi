from typing import List
from .move import Move


def towers_of_hanoi(
    n: int, source: int, destination: int, auxiliary: int
) -> List[Move]:
    if n == 1:
        return [{"source": source, "destination": destination}]
    moves: List[Move] = []

    moves += towers_of_hanoi(n - 1, source, auxiliary, destination)
    moves.append({"source": source, "destination": destination})
    moves += towers_of_hanoi(n - 1, auxiliary, destination, source)

    return moves
