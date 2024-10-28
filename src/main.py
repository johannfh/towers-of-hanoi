import logging
import time
import typing

import pygame

import button
import colors
from constants import (
    AUXILARY_TOWER,
    DESTINATION_TOWER,
    DISK_COLORS,
    DISK_SPEED,
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
    SOURCE_TOWER,
    TOWER_POSITIONS,
    FPS,
)
import towers
from towers import MovingDisk
import towers_of_hanoi
import utils

# TODO: Maybe make this dependant on a flag
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
"""The logger instance for logging game events."""

disks = 3
"""Number of disks"""

move_queue: utils.Queue[towers_of_hanoi.Move] = utils.Queue()
"""Remaining disk moves"""


move_queue.enqueue(
    *towers_of_hanoi.towers_of_hanoi(
        disks,
        SOURCE_TOWER,
        DESTINATION_TOWER,
        AUXILARY_TOWER,
    )
)


# TODO: Calculate disk_speed from animation_duration
# so animation speed increases when there are more disks

# animation_duration = 5
# """Time to complete the animation in (in `Seconds`)"""

disk_speed: typing.Callable[[], float] = lambda: DISK_SPEED
"""Should generally be multiplied by `delta_time` when used"""

moving_disk_data: MovingDisk = MovingDisk(
    position=pygame.Vector2(0, 0),
    target_position=pygame.Vector2(0, 0),
    disk=None,
)
"""Contains data related to the current disk being moved"""

current_move: towers_of_hanoi.Move | None = None
"""Current move being processed"""

solve_towers = False
"""`True` if solving is in progress"""

hanoi_towers = towers.generate_towers(
    disks, colors.generate_gradient(DISK_COLORS[0], DISK_COLORS[1], disks)
)
"""(`source`, `target`, `destination`)"""


def update_disks(transform: typing.Callable[[int], int]):

    # stop solving progress
    global solve_towers
    solve_towers = False

    # delete current moves being processed
    global current_move
    current_move = None

    global moving_disk_data
    moving_disk_data.reset()

    # update number of disks and rebuild towers
    global disks
    disks = transform(disks)

    global hanoi_towers
    hanoi_towers = towers.generate_towers(
        disks,
        colors.generate_gradient(DISK_COLORS[0], DISK_COLORS[1], disks),
    )

    # clear old moves and generate new ones
    global move_queue
    move_queue.clear()

    move_queue.enqueue(
        *towers_of_hanoi.towers_of_hanoi(
            disks,
            SOURCE_TOWER,
            DESTINATION_TOWER,
            AUXILARY_TOWER,
        )
    )


def set_disks(n: int):
    update_disks(lambda _: n)


def towers_solved() -> bool:
    """Checks if the problem is solved"""
    return (
        len(hanoi_towers[0].disks) == 0
        and len(hanoi_towers[1].disks) == 0
        and len(hanoi_towers[2].disks) == disks
    )


##################
# pre game setup #
##################

delta_time = 0
"""The time that passed between each frame"""

running = True
"""Game loop state"""

clock = pygame.time.Clock()
"""Clock for game sync"""

#####################
# initialize pygame #
#####################

pygame.init()
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(PROJECT_NAME)

pygame.font.init()
font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

###############
# load assets #
###############


def from_assets(path: str) -> str:
    return f"assets/{path}"


incr_button_img = pygame.image.load(from_assets("images/increment_button.png"))
decr_button_img = pygame.image.load(from_assets("images/decrement_button.png"))


#############
# game loop #
#############


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


def draw_moving_disk():
    if not moving_disk_data.disk:
        return
    disk_rect = pygame.rect.Rect(0, 0, disk.width, disk.height)
    disk_rect.bottomleft = (
        int(moving_disk_data.position[0]),
        int(moving_disk_data.position[1]),
    )
    pygame.draw.rect(screen, disk.color, disk_rect)


logger.info("Game starting")
GAME_START = time.time()
fpslog_timespan_passed = utils.create_timepassed(0.5)

for i in range(len(TOWER_POSITIONS)):
    pos = TOWER_POSITIONS[i]
    logger.info(f"Tower {i} bottomleft=({pos[0]}, {pos[1]})")

for disk in hanoi_towers[0].disks:
    logger.info(f"Disk {disk.index} margin-left={disk.left} margin-right={disk.bottom}")

solve_text = font.render("Solve!", True, colors.BLACK)

solve_button = button.Button(
    x=int(screen.get_width() / 2 - solve_text.get_width() / 2),
    y=MARGIN_VERTICAL + FONT_SIZE,
    image=solve_text,
    name="SolveHanoiButton",
)

incr_button = button.Button(
    x=MARGIN_HORIZONTAL,
    y=MARGIN_VERTICAL,
    image=incr_button_img,
    name="IncrementDisksButton",
)

decr_button = button.Button(
    x=SCREEN_WIDTH - MARGIN_HORIZONTAL - incr_button_img.get_width(),
    y=MARGIN_VERTICAL,
    image=decr_button_img,
    name="DecrementDisksButton",
)

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

    if solve_button.draw(screen):
        set_disks(disks)  # regenerate towers
        logger.info("solving towers")
        solve_towers = True

    draw_towers()
    draw_moving_disk()

    if solve_towers:
        # Go to next move if done with previous move
        if not current_move and not move_queue.empty():
            current_move = move_queue.dequeue()
            logger.info(current_move)

        # Take next disk from source tower
        if not towers_solved() and not moving_disk_data.disk and current_move:
            source_tower = hanoi_towers[current_move.source]
            target_tower = hanoi_towers[current_move.destination]

            # remove disk from source tower
            disk = source_tower.disks.pop()

            # save current disk position
            disk_position = pygame.Vector2(
                TOWER_POSITIONS[current_move.source][0] + disk.left,
                TOWER_POSITIONS[current_move.source][1]
                - (len(source_tower.disks)) * source_tower.disk_height,
            )

            target_position = pygame.Vector2(
                TOWER_POSITIONS[current_move.destination][0] + disk.left,
                TOWER_POSITIONS[current_move.destination][1]
                - (len(target_tower.disks)) * target_tower.disk_height,
            )

            moving_disk_data.insert(disk, disk_position, target_position)

        # move disk until it reached the target position
        if moving_disk_data.reached_target():
            assert current_move, "current_move should be defined here"
            assert moving_disk_data.disk, "moving disk should be defined"

            target_tower = hanoi_towers[current_move.destination]
            moved_disk = moving_disk_data.disk
            target_tower.disks.append(moved_disk)

            # Update the heights of each towers disks so they are correctly stacked
            for tower in hanoi_towers:
                tower.collapse_disk_heights()

            moving_disk_data.reset()
            current_move = None
        else:
            # calculate next position for moving disk
            next_position = moving_disk_data.next_position(disk_speed() * delta_time)

            moving_disk_data.position = next_position

        solve_towers = not towers_solved()


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
