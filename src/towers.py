import pygame
import typing
import constants
import towers
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


# disk_speed = lambda: 2 ^ disks - 1
# """Speed in which the disk should move"""


class MovingDisk:
    def __init__(
        self,
        position: pygame.Vector2 | None,
        target_position: pygame.Vector2 | None,
        disk: towers.Disk | None,
    ):
        self.position: pygame.Vector2 = position or pygame.Vector2(0, 0)
        """Current position of the disk on screen (bottom left)"""
        self.target_position: pygame.Vector2 = target_position or pygame.Vector2(0, 0)
        """Position the disk is moving towards (bottom left)"""
        self.disk: towers.Disk | None = disk
        """Disk which is currently being moved"""

    def reset(self):
        self.disk = None
        self.position = pygame.Vector2(0, 0)
        self.target_position = pygame.Vector2(0, 0)

    def reached_target(self) -> bool:
        return self.position == self.target_position

    def insert(
        self,
        disk: towers.Disk,
        position: pygame.Vector2,
        target: pygame.Vector2,
    ):
        self.disk = disk
        self.position = position
        self.target_position = target

    def next_position(self, speed: float) -> pygame.Vector2:
        return self.position.move_towards(self.target_position, speed)
