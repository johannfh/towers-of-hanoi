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

    hover: bool = False
    """`True` when mouse is over button"""

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
        logger.debug(
            '%s "%s" position set to %s',
            self.__class__.__name__,
            self.name,
            self.rect.topleft,
        )

    def get_position(self) -> typing.Tuple[int, int]:
        return self.rect.topleft

    def draw(self, surface: pygame.Surface) -> bool:
        action = False

        mouse_position = pygame.mouse.get_pos()

        if not self.hover and self.rect.collidepoint(mouse_position):
            logger.debug(
                '%s "%s" mouse over at %s',
                self.__class__.__name__,
                self.name,
                pygame.mouse.get_pos(),
            )
            self.hover = True

        if self.hover and not self.rect.collidepoint(mouse_position):
            logger.debug(
                '%s "%s" mouse out at %s',
                self.__class__.__name__,
                self.name,
                pygame.mouse.get_pos(),
            )
            self.hover = False

        left_click = pygame.mouse.get_pressed()[0]

        if not self.pressed and left_click and self.hover:
            logger.debug(
                '%s "%s" pressed mouse at %s',
                self.__class__.__name__,
                self.name,
                pygame.mouse.get_pos(),
            )

            self.pressed = True
            action = True

        if self.pressed and not left_click:
            logger.debug(
                '%s "%s" released mouse at %s',
                self.__class__.__name__,
                self.name,
                pygame.mouse.get_pos(),
            )
            self.pressed = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
