import logging
import typing

# from towers_of_hanoi import towers_of_hanoi

import pygame

import utils


class Disk:
    def __init__(self, width: float, height: float, index: float):
        self.width = width
        self.height = height
        self.index = index


class Tower:
    def __init__(self, disks: typing.List[Disk] = []):
        self.disks = disks

    def pop(self, n: int = -1):
        """
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """
        return self.disks.pop(n)


class Game:
    def __init__(
        self,
        logger: logging.Logger,
        resolution: typing.Tuple[float, float] = (1080, 720),
        colorTop: pygame.color.Color = pygame.color.Color(200, 50, 0),
        colorBottom: pygame.color.Color = pygame.color.Color(50, 0, 200),
        fps: float = 60,
    ) -> None:
        """
        Initialize the game state with the given `resolution`, `logger`, and `fps` (frames per second).

        The `colorTop` and `colorBottom` parameters are the colors of the smallest and largest disks.
        Other colors will be linearly interpolated from them using `utils.generate_gradient`.
        """

        self.logger = logger
        """
        The logger instance for logging game events.
        """

        self.logger.info("Starting game")

        self.resolution = resolution
        """
        The resolution of the game window. `(X, Y)`
        """

        # height - 150px
        self.tower_height = resolution[1] - 150

        self.fps = fps
        """
        The frames per second for the game loop.
        """
        self.delta_time = self.fps / 1000

        self.clock = pygame.time.Clock()
        self.running = True
        self.colorTop = colorTop
        self.colorBottom = colorBottom

        self.set_disks(3)

    def set_disks(self, n: int) -> None:
        diskHeight = self.tower_height / n
        diskWidthMax = 200.0
        diskWidthMin = 50.0
        initial_disks = [
            Disk(
                width=utils.lerp(diskWidthMax, diskWidthMin, 1 / (n - i)),
                height=diskHeight,
                index=n - i,
            )
            for i in range(n)
        ]
        self.towers = (
            Tower(),
            Tower(),
            Tower(),
        )

    def start(self) -> None:
        """
        Sets up the display, and starts the main game loop.

        Blocks until the game has finished.
        """

        pygame.init()
        self.screen = pygame.display.set_mode(size=self.resolution)
        self.circle_position = utils.get_center(self.screen)

        while self.running:
            self.mainloop()

        pygame.quit()

        self.logger.info("Game exited")

    def mainloop(self) -> None:
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # update screen
        screen = self.screen
        screen.fill(color="#000000")

        pygame.draw.circle(
            surface=screen,
            color="red",
            center=self.circle_position,
            radius=40,
        )

        mouse_pos = utils.get_mouse_position()

        # self.circle_position = self.circle_position.lerp(pygame.Vector2(mouse_pos[0], mouse_pos[1]), 0.1)
        # print(self.circle_position.distance_to(mouse_pos))

        self.circle_position.move_towards_ip(mouse_pos, 10)

        # apply screen changes
        pygame.display.flip()

        # calculate deltatime
        self.delta_time = self.clock.tick(self.fps) / 1000


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # TODO: Maybe make this dependant on a flag
    logging.basicConfig(level=logging.DEBUG)

    game = Game(
        logger=logger,
    )

    game.start()
