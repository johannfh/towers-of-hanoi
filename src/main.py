import logging

# from towers_of_hanoi import towers_of_hanoi

import pygame


class Game:
    def __init__(
        self, resolution: tuple[float, float], logger: logging.Logger, fps: float = 60
    ) -> None:
        """
        Initialize the game state with the given `resolution`, `logger`, and `fps` (frames per second).
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


    def start(self) -> None:
        """
        Sets up the display, and starts the main game loop.

        Blocks until the game has finished.
        """

        pygame.init()
        self.screen = pygame.display.set_mode(size=self.resolution)
        self.circle_position = get_center(self.screen)

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
        mouse_pos = pygame.mouse.get_pos()

        self.circle_position = self.circle_position.lerp(pygame.Vector2(mouse_pos[0], mouse_pos[1]), 0.1)

        # apply screen changes
        pygame.display.flip()

        # calculate deltatime
        self.delta_time = self.clock.tick(self.fps) / 1000


def get_center(screen: pygame.Surface):
    return pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


if __name__ == "__main__":
    # TODO: Make this work
    logger = logging.getLogger(__name__)

    # TODO: Maybe make this dependant on a flag
    logger.setLevel(logging.DEBUG)

    game = Game(logger=logger, resolution=(1080, 720))

    game.start()
