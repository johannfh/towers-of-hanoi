import logging
import time
import typing

import pygame

from button import Button
import colors
from constants import (
    DISK_COLORS,
    FONT_FAMILY,
    FONT_SIZE,
    LOG_FPS,
    MARGIN_HORIZONTAL,
    MARGIN_VERTICAL,
    MAX_DISKS,
    MIN_DISKS,
    PROJECT_NAME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TOWER_POSITIONS,
    FPS,
    TOWER_HEIGHT,
)
import constants
import towers
from towers_of_hanoi import towers_of_hanoi, Move
import utils

# TODO: Maybe make this dependant on a flag
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
"""The logger instance for logging game events."""

move_queue: utils.Queue[Move] = utils.Queue()
"""Remaining disk moves"""

disks = 3
"""Number of disks"""

hanoi_towers = towers.generate_towers(
    disks, TOWER_HEIGHT, colors.generate_gradient(DISK_COLORS[0], DISK_COLORS[1], disks)
)


def update_disks(transform: typing.Callable[[int], int]):
    # global references
    global disks
    global hanoi_towers
    global move_queue

    # update number of disks
    disks = transform(disks)

    # regenerate hanoi towers
    hanoi_towers = towers.generate_towers(
        disks,
        TOWER_HEIGHT,
        colors.generate_gradient(DISK_COLORS[0], DISK_COLORS[1], disks),
    )

    # clear old moves
    move_queue.clear()

    # generate new moves
    move_queue.enqueue(*towers_of_hanoi(disks, 0, 2, 1))


def set_disks(n: int):
    update_disks(lambda _: n)


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
pygame.display.set_caption(PROJECT_NAME)

###############
# load assets #
###############


def from_assets(path: str) -> str:
    return f"assets/{path}"


incr_button_img = pygame.image.load(from_assets("images/increment_button.png"))
decr_button_img = pygame.image.load(from_assets("images/decrement_button.png"))

incr_button = Button(
    x=MARGIN_HORIZONTAL,
    y=MARGIN_VERTICAL,
    image=incr_button_img,
    name="IncrementDisksButton",
)

decr_button = Button(
    x=SCREEN_WIDTH - MARGIN_HORIZONTAL - incr_button_img.get_width(),
    y=MARGIN_VERTICAL,
    image=decr_button_img,
    name="DecrementDisksButton",
)

pygame.font.init()

font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

solve_text = font.render("Solve!", True, colors.BLACK)
solve_button = Button(
    x=int(screen.get_width() / 2 - solve_text.get_width() / 2),
    y=MARGIN_VERTICAL + FONT_SIZE,
    image=solve_text,
    name="SolveHanoiButton",
)

#############
# game loop #
#############

logger.info("Game starting")
GAME_START = time.time()
fpslog_timespan_passed = utils.create_timepassed(0.5)


def draw_towers():
    for i in range(len(hanoi_towers)):
        tower = hanoi_towers[i]
        tower_position = TOWER_POSITIONS[i]

        for j in range(len(hanoi_towers[i].disks)):
            disk = tower.disks[j]
            disk.width
            disk_rect = pygame.rect.Rect(0, 0, disk.width, disk.height)
            disk_rect.bottomleft = (
                int(tower_position[0] + disk.left),
                int(tower_position[1] - disk.bottom),
            )
            pygame.draw.rect(screen, disk.color, disk_rect)

for pos in constants.TOWER_POSITIONS:
    print(f"({pos[0]}, {pos[1]})")

for disk in hanoi_towers[0].disks:
    print(disk.index, disk.left, disk.bottom)


while running:
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update screen
    screen.fill(color=colors.WHITE)

    if incr_button.draw(screen) and disks < MAX_DISKS:
        update_disks(lambda disks: disks + 1)
        logger.info("set disks to %d", disks)

    if decr_button.draw(screen) and disks > MIN_DISKS:
        update_disks(lambda disks: disks - 1)
        logger.info("set disks to %d", disks)

    solve_button.draw(screen)

    draw_towers()

    disk_count_text = pygame.font.SysFont(FONT_FAMILY, 25).render(
        f"Number of disks: {disks}", True, colors.BLACK
    )
    screen.blit(
        disk_count_text,
        (screen.get_width() / 2 - disk_count_text.get_width() / 2, MARGIN_VERTICAL),
    )

    # apply screen changes
    pygame.display.flip()

    # calculate deltatime
    delta_time = clock.tick(FPS) / 1000

    if LOG_FPS and fpslog_timespan_passed():
        logger.debug("fps: %d", clock.get_fps())

logger.info("Game exiting")
logger.info("Game duration: %.3f seconds", time.time() - GAME_START)

pygame.quit()
