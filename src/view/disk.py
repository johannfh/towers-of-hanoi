from typing import Tuple

import pygame

from .constants import DISK_WIDTH_MAX


class Disk:
    width: float
    """Width of this `Disk`"""
    height: float
    """Height of this `Disk`"""

    bottom: float
    """Distance relative to the bottom of this disks current tower"""
    left: float
    """Distance relative to the left of this disks current tower"""

    index: int
    """Index of this Disk (`unique`) (`in-order`, starting at 0 from the bottom)"""

    color: pygame.Color
    """The color of this disk"""

    def __init__(self, width: float, height: float, index: int, color: pygame.Color):
        self.width = width
        self.height = height

        self.index = index
        self.color = color

        self.left = (DISK_WIDTH_MAX - self.width) / 2

        self.bottom = self.height * self.index
