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
    disks: int,
    tower_height: int,
    disk_gradient: typing.List[pygame.color.Color],
) -> typing.Tuple[Tower, Tower, Tower]:
    assert (
        len(disk_gradient) == disks
    ), f"Number of colors for the disks did not match the number of disks ({disks})"

    disk_height = int(tower_height / disks)
    DISK_WIDTH_MAX = 200
    DISK_WIDTH_MIN = 100

    initial_disks = [
        Disk(
            width=utils.lerp(DISK_WIDTH_MAX, DISK_WIDTH_MIN, 1 / (disks - i)),
            height=disk_height,
            index=disks - i,
            color=disk_gradient[i],
        )
        for i in range(disks)
    ]

    towers = (
        Tower(initial_disks),
        Tower(),
        Tower(),
    )
    return towers
