import logging

import pygame

from button import Button
import colors
import utils

project_name = "Towers of Hanoi"
"""Name of this project"""

# TODO: Maybe make this dependant on a flag
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
"""The logger instance for logging game events."""

LOG_FPS = False

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

TOOLBAR_HEIGHT = 150

pygame.font.init()
default_font = pygame.font.SysFont("Arial", 30)

disk_colors = (
    pygame.color.Color(200, 50, 0),
    pygame.color.Color(50, 0, 200),
)
"""disk_colors: tuple(colorTop, colorBottom)\n
`colorTop` and `colorBottom` are the colors of the smallest and largest disks.
Other colors will be linearly interpolated from them using `utils.generate_gradient`. """

fps: float = 60
"""Frames per second"""

# height - 150px
tower_height = SCREEN_HEIGHT - TOOLBAR_HEIGHT + 50
"""The height of the towers"""

disks = 3
"""Number of disks"""

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
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(project_name)

###############
# load assets #
###############


def from_assets(path: str) -> str:
    return f"assets/{path}"


incr_button_img = pygame.image.load(from_assets("images/increment_button.png"))
decr_button_img = pygame.image.load(from_assets("images/decrement_button.png"))

incr_button = Button(
    x=50,
    y=50,
    image=incr_button_img,
    name="IncrementDisksButton",
)

decr_button = Button(
    x=SCREEN_WIDTH - 50 - incr_button_img.get_width(),
    y=50,
    image=decr_button_img,
    name="DecrementDisksButton",
)


#############
# game loop #
#############

logger.info("Starting game")
fpslog_timespan_passed = utils.create_timepassed(0.5)

while running:
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update screen
    screen.fill(color=colors.WHITE)

    if incr_button.draw(screen):
        disks += 1
        logger.info("set disks to %d", disks)

    if decr_button.draw(screen) and disks > 0:
        disks -= 1
        logger.info("set disks to %d", disks)

    disk_count_text = default_font.render(
        f"Number of disks: {disks}", True, colors.BLACK
    )
    screen.blit(
        disk_count_text,
        (screen.get_width() / 2 - disk_count_text.get_width() / 2, 60),
    )

    # apply screen changes
    pygame.display.flip()

    # calculate deltatime
    delta_time = clock.tick(fps) / 1000

    if LOG_FPS and fpslog_timespan_passed():
        logger.debug("fps: %d", clock.get_fps())

logger.info("Game exited")

pygame.quit()
