import pygame


def get_center(screen: pygame.Surface) -> pygame.Vector2:
    return pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


def get_mouse_position() -> pygame.Vector2:
    return pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
