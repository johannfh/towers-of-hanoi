from enum import Enum
import logging
from hanoi.hanoi import towers_of_hanoi
from hanoi.move import Move
from utils import Queue
from typing import Tuple

import pygame

import components
from components.button import ButtonEvents
from utils import assets, colors, get_center
from utils.event_emitter import EventEmitter
from .tower import Tower

TOWERS = {"source": 0, "auxiliary": 1, "destination": 2}

MIN_DISKS = 3
"""Minimum number of disks"""

MAX_DISKS = 15
"""Maximum number of disks"""

BACKGROUND_COLOR = colors.WHITE

BOTTOM_DISK_COLOR = pygame.Color(50, 0, 200)
TOP_DISK_COLOR = pygame.Color(200, 0, 50)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OUTER_MARGIN = 50
MENU_WIDTH = SCREEN_WIDTH - OUTER_MARGIN * 2
MENU_HEIGHT = 50
INNER_GAP = 25

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

    _movequeue: Queue[Move]

    _disks: int

    _frame: int
    _data_time: int

    _running: bool
    _solve: bool

    _towers: Tuple[Tower, Tower, Tower]

    def __init__(
        self,
        resolution: Tuple[int, int],
    ):
        self._listeners = {}

        self._frame = 0
        self._data_time = 0
        self._running = False
        self._solve = False

        self._logger = logging.getLogger(self.__class__.__name__)

        self._resolution = resolution
        self._screen = pygame.display.set_mode(size=resolution)

        self._clock = pygame.time.Clock()

        self._fps: float = 60
        """Application FPS limit"""

        self._disks = MIN_DISKS

        self._movequeue = Queue()

        self._movequeue.enqueue(
            *towers_of_hanoi(
                self._disks,
                TOWERS["source"],
                TOWERS["destination"],
                TOWERS["auxiliary"],
            )
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

            self._draw_menu()
            self._draw_towers()
            self._draw_moving_disk()

            # apply screen updates
            pygame.display.flip()

            # limit fps
            self._delta_time = self._clock.tick(self._fps)

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
        pass

    def _draw_moving_disk(self):
        pass

    def _increment_disks(self):
        if self._disks == MAX_DISKS:
            self._logger.info(f"increment_disks Reached MAX_DISKS: {MAX_DISKS}")
            return
        self._disks += 1
        self._logger.info(f"increment_disks Set Disks to: {self._disks}")

    def _decrement_disks(self):
        if self._disks == MIN_DISKS:
            self._logger.info(f"decrement_disks Reached MIN_DISKS: {MIN_DISKS}")
            return
        self._disks -= 1
        self._logger.info(f"decrement_disks Set Disks to: {self._disks}")

    def _solve_towers(self):
        if self._solve:
            self._logger.info("solve Restarting solving process")
        else:
            self._logger.info("solve Starting solving process")
        self._solve = True

        self._movequeue.clear()

    def _collapse_towers(self):
        for tower in self._towers:
            print(tower)
