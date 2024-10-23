import logging
# import towers_of_hanoi as toh

import pygame

class Game():
    def start(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.logger.info("Starting game")
        pygame.init()

        self.screen = pygame.display.set_mode(size=(1080, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        self.delta_time = self.fps / 1000

        while self.running:
            self.mainloop()

        self.logger.info("Game exited successfully")
   
    def mainloop(self) -> None:
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # update screen
        self.screen.fill(color="purple")

        # apply screen changes
        pygame.display.flip()

        # calculate deltatime
        self.delta_time = self.clock.tick(self.fps) / 1000

if __name__ == "__main__":

    logger = logging.getLogger(__name__)

    # TODO: Maybe make this dependant on a flag
    logger.setLevel(logging.DEBUG)

    game = Game()
    game.start(logger)
