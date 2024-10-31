from typing import List, Optional, Tuple

import pygame

import utils
from .constants import DISK_HEIGHT_MAX, DISK_WIDTH_MAX, DISK_WIDTH_MIN
from .disk import Disk
from .constants import TOWER_HEIGHT


class Tower:
    disks: List[Disk]
    """Disks of this tower"""

    disk_height: float
    """Height of the disks"""

    def __init__(self, disk_height: float, initial_disks: Optional[List[Disk]]):
        self.disks = initial_disks or []
        self.disk_height = disk_height

    def collapse_disks(self):
        for i, disk in enumerate(self.disks):
            disk.bottom = self.disk_height * i


def generate_towers(
    disks: int,
    disk_gradient: List[pygame.Color],
) -> Tuple[Tower, Tower, Tower]:
    assert (
        len(disk_gradient) == disks
    ), f"Number of colors for the disks did not match the number of disks ({disks})"

    disk_height = min(int(TOWER_HEIGHT / disks), DISK_HEIGHT_MAX)

    initial_disks = []

    for i in range(disks):
        initial_disks.append(
            Disk(
                width=utils.move_linear(
                    DISK_WIDTH_MAX, DISK_WIDTH_MIN, disks, i
                ),
                height=disk_height,
                index=i + 1,
                color=disk_gradient[i],
            )
        )

    towers = (
        Tower(
            initial_disks=initial_disks,
            disk_height=disk_height,
        ),
        Tower(initial_disks=None, disk_height=disk_height),
        Tower(initial_disks=None, disk_height=disk_height),
    )
    return towers
