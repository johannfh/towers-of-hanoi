import typing

type Source = int
type Auxilary = int
type Destination = int

type Move = tuple[Source, Destination]
"""
Moves are always from `Source` to `Destination`.
"""

def print_moves(moves: typing.List[Move]):
    for move in moves:
        print(f"{move[0]}->{move[1]}")

type Disks = int

def towers_of_hanoi(n: Disks, source: Source, destination: Destination, auxilary: Auxilary) -> typing.List[Move]:
    """
    Generate moves to move `n` Disks from tower `source` to `destination` over `auxilary`.
    """
    moves: typing.List[Move] = []
    if n <= 1:
        moves.append((source, destination))
    else:
        for i in towers_of_hanoi(n-1, source, auxilary, destination):
            moves.append(i)

        moves.append((source, destination))

        for i in towers_of_hanoi(n-1, auxilary, destination, source):
            moves.append(i)

    return moves

if __name__ == "__main__":
    print_moves(towers_of_hanoi(4, 0, 1, 2))