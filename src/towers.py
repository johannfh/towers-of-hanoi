import pygame
import typing
import constants
import utils


class Disk:
    def __init__(
        self, width: float, height: float, index: float, color: pygame.color.Color
    ):
        self.width = width
        self.height = height

        self.index = index

        self.color = color

        self.left = (constants.DISK_WIDTH_MAX - self.width) / 2
        """distance relative to the towers left"""

        self.bottom = self.height * self.index
        """distance relative to the towers bottom"""


class Tower:
    def __init__(
        self,
        disk_height: float,
        disks: typing.List[Disk] | None,
    ):
        self.disks = disks or []
        self.disk_height = disk_height

    def collapse_disk_heights(self):
        for i in range(len(self.disks)):
            self.disks[i].bottom = self.disk_height * i


def generate_towers(
    disks: int,
    disk_gradient: typing.List[pygame.color.Color],
) -> typing.Tuple[Tower, Tower, Tower]:
    assert (
        len(disk_gradient) == disks
    ), f"Number of colors for the disks did not match the number of disks ({disks})"

    disk_height = min(int(constants.TOWER_HEIGHT / disks), constants.DISK_HEIGHT_MAX)

    initial_disks = []

    for i in range(disks):
        initial_disks.append(
            Disk(
                width=utils.move_linear(
                    constants.DISK_WIDTH_MAX, constants.DISK_WIDTH_MIN, disks, i
                ),
                height=disk_height,
                index=i + 1,
                color=disk_gradient[i],
            )
        )

    towers = (
        Tower(
            disks=initial_disks,
            disk_height=disk_height,
        ),
        Tower(disks=None, disk_height=disk_height),
        Tower(disks=None, disk_height=disk_height),
    )
    return towers
