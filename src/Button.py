import logging
import typing
import pygame
import uuid

logger = logging.getLogger(__name__)


class Button:
    rect: pygame.Rect
    """Represents the buttons boundaries"""

    image: pygame.Surface
    """The buttons visible image"""

    pressed: bool = False
    """`True` when button is pressed"""

    name: str = uuid.uuid4().__str__()
    """Name of this button, usually used for debugging"""

    def __init__(
        self, x: int, y: int, image: pygame.Surface, name: str | None, scale: float = 1
    ):
        self.name = name if name else self.name

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        logger.info("%s created at %s", self.__class__.__name__, self.rect.topleft)

    def set_position(self, x: int | None, y: int | None):
        """Updates coordinates if not `None`"""
        self.rect.topleft = (x or self.rect.x, y or self.rect.y)
        logger.info(
            "%s position set to x=%d y=%d", self.__class__, self.rect.x, self.rect.y
        )

    def get_position(self) -> typing.Tuple[int, int]:
        return self.rect.topleft

    def draw(self, surface: pygame.Surface) -> bool:
        action = False

        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            logger.debug(
                '%s hovering over "%s" mouse at (%d, %d)',
                self.__class__.__name__,
                self.name,
                pygame.mouse.get_pos()[0],
                pygame.mouse.get_pos()[1],
            )
            if pygame.mouse.get_pressed()[0] == True and self.pressed == False:
                self.pressed = True
                action = True

        if pygame.mouse.get_pressed()[0] == False:
            self.pressed = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
