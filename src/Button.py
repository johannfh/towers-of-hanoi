import pygame

class Button:
    rect: pygame.Rect
    """Represents the buttons boundaries"""

    image: pygame.Surface
    """The buttons visible image"""

    pressed: bool = False
    """`True` when button is pressed"""

    def __init__(self, x: int, y: int, image: pygame.Surface, scale: float = 1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def set_position(self, x: int, y: int):
        self.rect.topleft = (x, y)

    def draw(self, surface: pygame.Surface) -> bool:
        action = False

        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == True and self.pressed == False:
                self.pressed = True
                action = True

        if pygame.mouse.get_pressed()[0] == False:
            self.pressed = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
