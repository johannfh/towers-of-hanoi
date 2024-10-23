import logging
import typing

# from towers_of_hanoi import towers_of_hanoi

import pygame

import utils


class Tower:
    def __init__(self, disks: typing.List = []):
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

        Args:
            resolution (tuple[float, float]): The resolution of the game window. `(X, Y)`
            logger (logging.Logger): The logger instance for logging game events.
            fps (float): The frames per second for the game loop.
        """

        self.logger = logger
        self.logger.info("Starting game")

        self.resolution = resolution

        self.fps = fps
        self.delta_time = self.fps / 1000

        self.clock = pygame.time.Clock()
        self.running = True
        self.colorTop = colorTop
        self.colorBottom = colorBottom

        self.set_disks(3)

    def set_disks(self, n: int) -> None:
        self.towers = (Tower([x + 1 for x in range(n)]), Tower(), Tower())

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
    # TODO: Make this work
    logger = logging.getLogger(__name__)

    # TODO: Maybe make this dependant on a flag
    logger.setLevel(logging.DEBUG)

    game = Game(
        logger=logger,
    )

    game.start()
