import logging
import time
import typing

import pygame

import components
import colors


from constants import (
    AUXILIARY_TOWER,
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

###############
# load assets #
###############


def from_assets(path: str) -> str:
    return f"assets/{path}"


incr_button_img = pygame.image.load(from_assets("images/increment_button.png"))
decr_button_img = pygame.image.load(from_assets("images/decrement_button.png"))


class App:
    logger = logging.getLogger(__name__)
    """The `Logger` instance for the App"""

    __movequeue__: utils.Queue[towers_of_hanoi.Move]
    """Remaining disk moves"""

    __disks__: int
    """Number of disks"""

    moving_disk_data: MovingDisk
    """Contains data related to the current disk being moved"""

    def __init__(self):

        self.__frame__ = 0
        self.__disks__ = 3
        self.__movequeue__ = utils.Queue()

        self.__movequeue__.enqueue(
            *towers_of_hanoi.towers_of_hanoi(
                self.__disks__,
                SOURCE_TOWER,
                DESTINATION_TOWER,
                AUXILIARY_TOWER,
            )
        )
        # TODO: Calculate disk_speed from animation_duration
        # so animation speed increases when there are more disks

        # animation_duration = 5
        # """Time to complete the animation in (in `Seconds`)"""

        self.disk_speed: typing.Callable[[], float] = lambda: DISK_SPEED
        """Should generally be multiplied by `delta_time` when used"""

        self.moving_disk_data = MovingDisk(
            position=pygame.Vector2(0, 0),
            target_position=pygame.Vector2(0, 0),
            disk=None,
        )
        self.current_move: typing.Optional[towers_of_hanoi.Move] = None
        """Current move being processed"""

        self.solve_towers = False
        """`True` if solving is in progress"""

        self.hanoi_towers = towers.generate_towers(
            self.__disks__,
            colors.generate_gradient(DISK_COLORS[0], DISK_COLORS[1], self.__disks__),
        )
        """(`source`, `target`, `destination`)"""

        ##################
        # pre game setup #
        ##################

        self.delta_time = 0
        """The time that passed between each frame"""

        self.running = True
        """Game loop state"""

        self.clock = pygame.time.Clock()
        """Clock for game sync"""

    def run(self, fps: int):
        self.__fps__ = fps

        #####################
        # initialize pygame #
        #####################
        pygame.init()
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(PROJECT_NAME)

        # initialize font
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

        self.logger.info("Game starting")

        self.GAME_START = time.time()
        fpslog_timespan_passed = utils.create_timepassed(0.5)

        for i in range(len(TOWER_POSITIONS)):
            pos = TOWER_POSITIONS[i]
            self.logger.info(f"Tower {i} bottomleft=({pos[0]}, {pos[1]})")

        for disk in self.hanoi_towers[0].disks:
            self.logger.info(
                f"Disk {disk.index} margin-left={disk.left} margin-right={disk.bottom}"
            )

        solve_text = self.font.render("Solve!", True, colors.BLACK)

        solve_button = components.Button(
            x=int(self.screen.get_width() / 2 - solve_text.get_width() / 2),
            y=MARGIN_VERTICAL + FONT_SIZE,
            image=solve_text,
            name="SolveHanoiButton",
        )

        incr_button = components.Button(
            x=MARGIN_HORIZONTAL,
            y=MARGIN_VERTICAL,
            image=incr_button_img,
            name="IncrementDisksButton",
        )

        decr_button = components.Button(
            x=SCREEN_WIDTH - MARGIN_HORIZONTAL - incr_button_img.get_width(),
            y=MARGIN_VERTICAL,
            image=decr_button_img,
            name="DecrementDisksButton",
        )

        while self.running:
            # process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update screen
            self.screen.fill(color=colors.WHITE)

            if incr_button.draw(self.screen) and self.__disks__ < MAX_DISKS:
                self.update_disks(lambda disks: disks + 1)
                self.logger.info("set disks to %d", self.__disks__)

            if decr_button.draw(self.screen) and self.__disks__ > MIN_DISKS:
                self.update_disks(lambda disks: disks - 1)
                self.logger.info("set disks to %d", self.__disks__)

            if solve_button.draw(self.screen):
                self.set_disks(self.__disks__)  # regenerate towers
                self.logger.info("solving towers")
                self.solve_towers = True

            self.draw_towers()
            self.draw_moving_disk()

            if self.solve_towers:
                # Go to next move if done with previous move
                if not self.current_move and not self.__movequeue__.empty():
                    self.current_move = self.__movequeue__.dequeue()
                    self.logger.info(self.current_move)

                # Take next disk from source tower
                if (
                    not self.towers_solved()
                    and not self.moving_disk_data.disk
                    and self.current_move
                ):
                    source_tower = self.hanoi_towers[self.current_move.source]
                    target_tower = self.hanoi_towers[self.current_move.destination]

                    # remove disk from source tower
                    disk = source_tower.disks.pop()

                    # save current disk position
                    disk_position = pygame.Vector2(
                        TOWER_POSITIONS[self.current_move.source][0] + disk.left,
                        TOWER_POSITIONS[self.current_move.source][1]
                        - (len(source_tower.disks)) * source_tower.disk_height,
                    )

                    target_position = pygame.Vector2(
                        TOWER_POSITIONS[self.current_move.destination][0] + disk.left,
                        TOWER_POSITIONS[self.current_move.destination][1]
                        - (len(target_tower.disks)) * target_tower.disk_height,
                    )

                    self.moving_disk_data.insert(disk, disk_position, target_position)

                # move disk until it reached the target position
                if self.moving_disk_data.reached_target():
                    assert self.current_move, "current_move should be defined here"
                    assert self.moving_disk_data.disk, "moving disk should be defined"

                    target_tower = self.hanoi_towers[self.current_move.destination]
                    moved_disk = self.moving_disk_data.disk
                    target_tower.disks.append(moved_disk)

                    # Update the heights of each towers disks so they are correctly stacked
                    for tower in self.hanoi_towers:
                        tower.collapse_disk_heights()

                    self.moving_disk_data.reset()
                    self.current_move = None
                else:
                    # calculate next position for moving disk
                    next_position = self.moving_disk_data.next_position(
                        self.disk_speed() * self.delta_time
                    )

                    self.moving_disk_data.position = next_position

                self.solve_towers = not self.towers_solved()

            disk_count_text = pygame.font.SysFont(FONT_FAMILY, 25).render(
                f"Number of disks: {self.__disks__}", True, colors.BLACK
            )

            self.screen.blit(
                disk_count_text,
                (
                    self.screen.get_width() / 2 - disk_count_text.get_width() / 2,
                    MARGIN_VERTICAL,
                ),
            )

            # apply screen changes
            pygame.display.flip()

            # calculate deltatime
            self.delta_time = self.clock.tick(self.__fps__) / 1000

            if LOG_FPS and fpslog_timespan_passed():
                self.logger.debug("fps: %d", self.clock.get_fps())

        self.logger.info("Game exiting")
        self.logger.info("Game duration: %.3f seconds", time.time() - self.GAME_START)

        pygame.quit()

    def increment_frame(self):
        """Call this once per frame to increment the frame counter"""
        self.__frame__ += 1

    def get_frame(self) -> int:
        return self.__frame__

    def update_disks(self, transform: typing.Callable[[int], int]):

        # stop solving progress
        self.solve_towers = False

        # delete current moves being processed
        self.current_move = None

        self.moving_disk_data.reset()

        # update number of disks and rebuild towers
        self.__disks__ = transform(self.__disks__)

        self.hanoi_towers = towers.generate_towers(
            self.__disks__,
            colors.generate_gradient(DISK_COLORS[0], DISK_COLORS[1], self.__disks__),
        )

        # clear old moves and generate new ones
        self.__movequeue__.clear()

        self.__movequeue__.enqueue(
            *towers_of_hanoi.towers_of_hanoi(
                self.__disks__,
                SOURCE_TOWER,
                DESTINATION_TOWER,
                AUXILIARY_TOWER,
            )
        )

    def set_disks(self, n: int):
        self.update_disks(lambda _: n)

    def towers_solved(self) -> bool:
        """Checks if the problem is solved"""
        return (
            len(self.hanoi_towers[0].disks) == 0
            and len(self.hanoi_towers[1].disks) == 0
            and len(self.hanoi_towers[2].disks) == self.__disks__
        )

    #############
    # game loop #
    #############

    def draw_towers(self):
        for i in range(len(self.hanoi_towers)):
            tower = self.hanoi_towers[i]
            tower_position = TOWER_POSITIONS[i]

            for j in range(len(self.hanoi_towers[i].disks)):
                disk = tower.disks[j]
                disk.width
                disk_rect = pygame.rect.Rect(0, 0, disk.width, disk.height)
                disk_rect.bottomleft = (
                    int(tower_position[0] + disk.left),
                    int(tower_position[1] - disk.bottom),
                )
                pygame.draw.rect(self.screen, disk.color, disk_rect)

    def draw_moving_disk(self):
        if not self.moving_disk_data.disk:
            return
        disk_rect = pygame.rect.Rect(
            0, 0, self.moving_disk_data.disk.width, self.moving_disk_data.disk.height
        )
        disk_rect.bottomleft = (
            int(self.moving_disk_data.position[0]),
            int(self.moving_disk_data.position[1]),
        )
        pygame.draw.rect(self.screen, self.moving_disk_data.disk.color, disk_rect)
