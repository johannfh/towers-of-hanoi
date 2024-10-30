from enum import Enum
from typing import Optional, Tuple
import uuid

import pygame
from utils.event_emitter import EventEmitter


class ButtonEvents(Enum):
    MOUSE_OVER = "mouse over"
    MOUSE_OUT = "mouse out"

    MOUSE_DOWN = "mouse down"
    MOUSE_UP = "mouse up"


class Button(EventEmitter[ButtonEvents, None]):
    rect: pygame.Rect

    def __init__(
        self,
        topleft: Tuple[int, int],
        sprite: pygame.Surface,
        name: Optional[str],
        scale: float = 1,
    ):
        self._listeners = {}

        self._name = name if name else str(uuid.uuid4())
        width = sprite.get_width()
        height = sprite.get_height()

        self._sprite = pygame.transform.scale(sprite, (width * scale, height * scale))

        self._rect = self._sprite.get_rect()
        self._rect.topleft = topleft

        self._hovering = False
        self._pressed = False

    def draw(self, surface: pygame.Surface):
        mouse_position = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        # handle hovering
        if not self._hovering and self._rect.collidepoint(mouse_position):
            self._hovering = True
            self.emit(ButtonEvents.MOUSE_OVER, None)
        elif self._hovering and not self._rect.collidepoint(mouse_position):
            self._hovering = False
            self.emit(ButtonEvents.MOUSE_OUT, None)

        # handle pressing
        if not self._pressed and left_click and self._hovering:
            self._pressed = True
            self.emit(ButtonEvents.MOUSE_DOWN, None)
        elif self._pressed and not left_click:
            self._pressed = False
            self.emit(ButtonEvents.MOUSE_UP, None)

        surface.blit(self._sprite, self._rect)
