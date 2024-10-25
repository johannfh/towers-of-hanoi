import logging
import typing

# from towers_of_hanoi import towers_of_hanoi

import pygame

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
    tower_height: int, disk_gradient: typing.List[pygame.color.Color]
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
            color=disk_colors[i],
        )
        for i in range(tower_height)
    ]

    towers = (
        Tower(initial_disks),
        Tower(),
        Tower(),
    )
    return towers


# TODO: Maybe make this dependant on a flag
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
"""
The logger instance for logging game events.
"""

resolution: typing.Tuple[float, float] = (1080, 720)
"""
The `(width, height)` resolution for the game.
"""

disk_colors = (
    pygame.color.Color(200, 50, 0),
    pygame.color.Color(50, 0, 200),
)
"""
disk_colors: tuple(colorTop, colorBottom)

`colorTop` and `colorBottom` are the colors of the smallest and largest disks.
Other colors will be linearly interpolated from them using `utils.generate_gradient`.
"""

fps: float = 60

logger.info("Starting game")

resolution = resolution
"""
The resolution of the game window. `(X, Y)`
"""

# height - 150px
tower_height = resolution[1] - 150

fps = fps
"""
The frames per second for the game loop.
"""

delta_time = 0
"""
The time that passed between each frame
"""

running = True
"""
Game loop state
"""

pygame.init()
window = pygame.display.set_mode(size=resolution)

circle_position = utils.get_center(window)

clock = pygame.time.Clock()

while running:
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update screen
    window.fill(color="#000000")

    pygame.draw.circle(
        surface=window,
        color="red",
        center=circle_position,
        radius=40,
    )

    mouse_pos = utils.get_mouse_position()

    # circle_position = circle_position.lerp(pygame.Vector2(mouse_pos[0], mouse_pos[1]), 0.1)
    # print(circle_position.distance_to(mouse_pos))

    circle_position.move_towards_ip(mouse_pos, 10)

    # apply screen changes
    pygame.display.flip()

    # calculate deltatime
    delta_time = clock.tick(fps) / 1000

logger.info("Game exited")
pygame.quit()
