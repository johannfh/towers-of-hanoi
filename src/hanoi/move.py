from typing import TypedDict


class Move:
    source: int
    destination: int

    def __init__(self, source: int, destination: int):
        self.source = source
        self.destination = destination

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination}"
