import pygame
import typing
import utils


class Disk:
    def __init__(
        self, width: float, height: float, index: float, color: pygame.color.Color
    ):
        self.width = width
        self.height = height
        self.index = index
        self.color = color


class Tower:
    def __init__(self, disks: typing.List[Disk] = []):
        self.disks = disks

    def pop(self, n: int = -1):
        """
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """
        return self.disks.pop(n)

def generate_towers(
    tower_height: int,
    disk_gradient: typing.List[pygame.color.Color],
) -> typing.Tuple[Tower, Tower, Tower]:
    assert (
        len(disk_gradient) == tower_height
    ), f"Number of colors for the disks did not match the number of disks ({tower_height})"

    disk_height = tower_height / tower_height
    disk_width_max = 200.0
    disk_width_min = 50.0
    initial_disks = [
        Disk(
            width=utils.lerp(disk_width_max, disk_width_min, 1 / (tower_height - i)),
            height=disk_height,
            index=tower_height - i,
            color=disk_gradient[i],
        )
        for i in range(tower_height)
    ]

    towers = (
        Tower(initial_disks),
        Tower(),
        Tower(),
    )
    return towers
