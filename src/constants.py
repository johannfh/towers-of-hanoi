import pygame

PROJECT_NAME = "Towers of Hanoi"
"""Name of this project"""

SOURCE_TOWER = 0
AUXILARY_TOWER = 1
DESTINATION_TOWER = 2

LOG_FPS = False

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

TOOLBAR_HEIGHT = 50

MARGIN_VERTICAL = 50
"""Vertical screen margin"""
MARGIN_HORIZONTAL = 50
"""Horizontal screen margin"""

DISK_WIDTH_MAX = 200
DISK_WIDTH_MIN = 50
DISK_HEIGHT_MAX = 30

TOWER_HEIGHT = SCREEN_HEIGHT - (MARGIN_VERTICAL * 2 + TOOLBAR_HEIGHT + MARGIN_VERTICAL)
"""The height of the towers"""

TOWER_POSITIONS = (
    (MARGIN_HORIZONTAL * 1 + DISK_WIDTH_MAX * 0, SCREEN_HEIGHT - MARGIN_VERTICAL),
    (MARGIN_HORIZONTAL * 2 + DISK_WIDTH_MAX * 1, SCREEN_HEIGHT - MARGIN_VERTICAL),
    (MARGIN_HORIZONTAL * 3 + DISK_WIDTH_MAX * 2, SCREEN_HEIGHT - MARGIN_VERTICAL),
)
"""Bottom-left positions `(source, auxiliary, destination)`"""

FONT_FAMILY = "Arial"
FONT_SIZE = 25

DISK_COLORS = (
    pygame.color.Color(50, 0, 200),
    pygame.color.Color(200, 50, 0),
)
"""disk_colors: `tuple(colorTop, colorBottom)`

`colorTop` and `colorBottom` are the colors of the smallest and largest disks.
Other colors will be linearly interpolated from them using `utils.generate_gradient`. """

MIN_DISKS = 1
"""Minimum number of disks"""
MAX_DISKS = 25
"""Maximum number of disks"""

FPS = 60
"""The frames per second for the game"""
