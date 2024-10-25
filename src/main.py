import logging
import typing

import pygame

import towers
import colors
import utils


# TODO: Maybe make this dependant on a flag
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
"""The logger instance for logging game events."""

resolution: typing.Tuple[float, float] = (1080, 720)
"""The `(width, height)` resolution for the game."""

disk_colors = (
    pygame.color.Color(200, 50, 0),
    pygame.color.Color(50, 0, 200),
)
"""disk_colors: tuple(colorTop, colorBottom)\n
`colorTop` and `colorBottom` are the colors of the smallest and largest disks.
Other colors will be linearly interpolated from them using `utils.generate_gradient`. """

fps: float = 60

logger.info("Starting game")

resolution = resolution
"""The resolution of the game window. `(X, Y)`"""

# height - 150px
tower_height = resolution[1] - 150
"""The height of the towers"""

fps = fps
"""The frames per second for the game loop. """

delta_time = 0
"""The time that passed between each frame"""

running = True
"""Game loop state"""

clock = pygame.time.Clock()
"""Clock for game sync"""

##################
# pre game setup #
##################

pygame.init()
window = pygame.display.set_mode(size=resolution)

circle_position = utils.get_center(window)


#############
# game loop #
#############

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
