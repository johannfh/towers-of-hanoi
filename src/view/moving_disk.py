from typing import Optional
import pygame

from .tower import Disk


class MovingDisk:
    def __init__(
        self,
        position: pygame.Vector2 | None,
        target_position: pygame.Vector2 | None,
        disk: Optional[Disk],
    ):
        self.position: pygame.Vector2 = position or pygame.Vector2(0, 0)
        """Current position of the disk on screen (bottom left)"""
        self.target_position: pygame.Vector2 = target_position or pygame.Vector2(0, 0)
        """Position the disk is moving towards (bottom left)"""
        self.disk: Disk | None = disk
        """Disk which is currently being moved"""

    def reset(self):
        self.disk = None
        self.position = pygame.Vector2(0, 0)
        self.target_position = pygame.Vector2(0, 0)

    def reached_target(self) -> bool:
        return self.position == self.target_position

    def insert(
        self,
        disk: Disk,
        position: pygame.Vector2,
        target: pygame.Vector2,
    ):
        self.disk = disk
        self.position = position
        self.target_position = target

    def next_position(self, speed: float) -> pygame.Vector2:
        return self.position.move_towards(self.target_position, speed)
