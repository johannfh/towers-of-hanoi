from enum import Enum
import logging
from hanoi.hanoi import towers_of_hanoi
from hanoi.move import Move
from utils import Queue
from typing import Optional, Tuple

import pygame

import components
from components.button import ButtonEvents
from utils import assets, colors, get_center
from utils.event_emitter import EventEmitter

from .constants import (
    AUXILIARY_TOWER,
    BACKGROUND_COLOR,
    BOTTOM_DISK_COLOR,
    DESTINATION_TOWER,
    DISK_SPEED,
    INNER_GAP,
    MAX_DISKS,
    MENU_WIDTH,
    MIN_DISKS,
    OUTER_MARGIN,
    SOURCE_TOWER,
    TOP_DISK_COLOR,
    TOWER_POSITIONS,
)
from .tower import Tower, generate_towers
from .moving_disk import MovingDisk


# load assets
increment_button_image_path = assets.assets("images/increment_button.png")
increment_button_sprite = pygame.image.load(increment_button_image_path)
decrement_button_image_path = assets.assets("images/decrement_button.png")
decrement_button_sprite = pygame.image.load(decrement_button_image_path)


class AppEvents(Enum):
    pass


class App(EventEmitter[AppEvents, None]):

    _logger: logging.Logger
    """Application `Logger` instance"""

    _resolution: Tuple[int, int]
    """`(x, y)` size of the window"""

    _screen: pygame.Surface
    """Reference to the window of this application"""

    _move_queue: Queue[Move]

    _disks: int

    _frame: int
    _data_time: int

    _running: bool
    _solve: bool

    _towers: Tuple[Tower, Tower, Tower]

    _current_move: Optional[Move]
    _moving_disk_data: MovingDisk
    """Contains data related to the current disk being moved"""

    def __init__(
        self,
        resolution: Tuple[int, int],
    ):
        self._listeners = {}

        self._frame = 0
        self._data_time = 0
        self._running = False
        self._solve = False

        self._disk_speed = lambda: DISK_SPEED

        self._logger = logging.getLogger(self.__class__.__name__)

        self._resolution = resolution
        self._screen = pygame.display.set_mode(size=resolution)

        self._clock = pygame.time.Clock()

        self._fps: float = 60
        """Application FPS limit"""

        self._disks = MIN_DISKS

        self._moving_disk_data = MovingDisk(None, None, None)
        self._current_move = None

        self._move_queue = Queue()

        self._move_queue.enqueue(
            *towers_of_hanoi(
                self._disks,
                SOURCE_TOWER,
                DESTINATION_TOWER,
                AUXILIARY_TOWER,
            )
        )

        self._towers = generate_towers(
            self._disks,
            colors.generate_gradient(BOTTOM_DISK_COLOR, TOP_DISK_COLOR, self._disks),
        )

        self._font = pygame.font.SysFont("Arial", 25)

        ##########################
        # Instantiate Components #
        ##########################

        self._increment_button = components.Button(
            (OUTER_MARGIN, OUTER_MARGIN), increment_button_sprite, "IncrementButton"
        )

        self._decrement_button = components.Button(
            (
                OUTER_MARGIN + MENU_WIDTH - decrement_button_sprite.get_width(),
                OUTER_MARGIN,
            ),
            decrement_button_sprite,
            "DecrementButton",
        )

        screen_center = get_center(self._screen)

        solve_text = self._font.render("Solve!", True, colors.BLACK)
        self._solve_button = components.Button(
            (int(screen_center.x) + INNER_GAP // 2, OUTER_MARGIN),
            solve_text,
            "SolveButton",
        )

        self._logger.info("App created")

    def run(self):
        self._logger.info("Starting app")
        self._running = True

        self._increment_button.add_event_listener(
            ButtonEvents.MOUSE_UP, self._increment_disks
        )

        self._decrement_button.add_event_listener(
            ButtonEvents.MOUSE_UP, self._decrement_disks
        )

        self._solve_button.add_event_listener(ButtonEvents.MOUSE_UP, self._solve_towers)

        while self._running:
            self._frame += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # repaint screen all white
            self._screen.fill(BACKGROUND_COLOR)

            if self._solve:
                if not self._current_move and not self._move_queue.empty():
                    self._current_move = self._move_queue.dequeue()
                    self._logger.info(self._current_move)

                # take the next disk from the tower
                if (
                    not self._towers_solved()
                    and not self._moving_disk_data.disk
                    and self._current_move
                ):
                    source_tower = self._towers[self._current_move.source]
                    target_tower = self._towers[self._current_move.destination]

                    # remove disk from source tower
                    disk = source_tower.disks.pop()

                    current_position = pygame.Vector2(
                        TOWER_POSITIONS[self._current_move.source][0] + disk.left,
                        TOWER_POSITIONS[self._current_move.source][1]
                        - source_tower.disk_height * (len(source_tower.disks)),
                    )

                    target_position = pygame.Vector2(
                        TOWER_POSITIONS[self._current_move.destination][0] + disk.left,
                        TOWER_POSITIONS[self._current_move.destination][1]
                        - target_tower.disk_height * (len(target_tower.disks)),
                    )

                    self._moving_disk_data.insert(
                        disk, current_position, target_position
                    )

                # if the moving disk has reached the target position
                if self._moving_disk_data.reached_target():
                    assert self._current_move, "current_move should be defined here"
                    assert self._moving_disk_data.disk, "moving disk should be defined"

                    target_tower = self._towers[self._current_move.destination]
                    moved_disk = self._moving_disk_data.disk
                    target_tower.disks.append(moved_disk)

                    self._collapse_all_towers()

                    self._moving_disk_data.reset()
                    self._current_move = None
                else:
                    next_position = self._moving_disk_data.next_position(
                        self._disk_speed() * self._delta_time
                    )
                    self._moving_disk_data.position = next_position

                self._solve = not self._towers_solved()

            self._draw_menu()
            self._draw_towers()
            self._draw_moving_disk()

            # apply screen updates
            pygame.display.flip()

            # limit fps
            self._delta_time = self._clock.tick(self._fps) / 1000

        pygame.quit()
        self._logger.info("Exiting app")

    def _draw_menu(self):
        screen_center = get_center(self._screen)

        self._decrement_button.draw(self._screen)
        self._increment_button.draw(self._screen)

        disks_text = self._font.render(f"Disks: {self._disks}", True, colors.BLACK)
        self._screen.blit(
            disks_text,
            (screen_center.x - disks_text.get_width() - INNER_GAP // 2, OUTER_MARGIN),
        )

        self._solve_button.draw(self._screen)

    def _draw_towers(self):
        for i, tower in enumerate(self._towers):
            tower_position = TOWER_POSITIONS[i]
            for disk in tower.disks:
                rect = pygame.Rect(0, 0, disk.width, disk.height)
                rect.left = int(tower_position[0] + disk.left)
                rect.bottom = int(tower_position[1] - disk.bottom)
                pygame.draw.rect(self._screen, disk.color, rect)

    def _draw_moving_disk(self):
        if not self._moving_disk_data.disk:
            return

        disk = self._moving_disk_data.disk
        disk_rect = pygame.Rect(0, 0, disk.width, disk.height)
        disk_rect.bottomleft = (
            int(self._moving_disk_data.position[0]),
            int(self._moving_disk_data.position[1]),
        )

        pygame.draw.rect(self._screen, disk.color, disk_rect)

    def _increment_disks(self):
        if self._disks == MAX_DISKS:
            self._logger.info(f"increment_disks Reached MAX_DISKS: {MAX_DISKS}")
            return
        self._disks += 1
        self._logger.info(f"increment_disks Set Disks to: {self._disks}")
        self._rebuild_towers()

    def _decrement_disks(self):
        if self._disks == MIN_DISKS:
            self._logger.info(f"decrement_disks Reached MIN_DISKS: {MIN_DISKS}")
            return
        self._disks -= 1
        self._logger.info(f"decrement_disks Set Disks to: {self._disks}")
        self._rebuild_towers()

    def _solve_towers(self):
        if self._solve:
            self._logger.info("solve Restarting solving process")
        else:
            self._logger.info("solve Starting solving process")
        self._rebuild_towers()
        self._solve = True

    def _towers_solved(self) -> bool:
        return (
            len(self._towers[SOURCE_TOWER].disks) == 0
            and len(self._towers[AUXILIARY_TOWER].disks) == 0
            and len(self._towers[AUXILIARY_TOWER].disks) == self._disks
        )

    def _rebuild_towers(self):
        # stop solving process
        self._solve = False

        # cancel all ongoing moves
        self._current_move = None
        self._moving_disk_data.reset()

        # rebuild towers
        self._towers = generate_towers(
            self._disks,
            colors.generate_gradient(BOTTOM_DISK_COLOR, TOP_DISK_COLOR, self._disks),
        )

        # recalculate move queue
        self._move_queue.clear()

        self._move_queue.enqueue(
            *towers_of_hanoi(
                self._disks,
                SOURCE_TOWER,
                DESTINATION_TOWER,
                AUXILIARY_TOWER,
            )
        )

    def _collapse_all_towers(self):
        for tower in self._towers:
            tower.collapse_disks()
