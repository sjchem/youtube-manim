"""Project-wide visual configuration for the Manim animation."""

from manim import (
    BLUE_B,
    BLUE_D,
    BLUE_E,
    GREEN_C,
    ORANGE,
    PURPLE_B,
    RED_C,
    WHITE,
    config,
)

OCEANIC_BG = "#07131f"
OCEANIC_PANEL = "#0b2033"
OCEANIC_GRID = "#22445f"
CYAN = "#7FDBFF"
CYAN_BRIGHT = "#B9F7FF"
SOFT_BLUE = BLUE_B
DEEP_BLUE = BLUE_E
VALID_GREEN = GREEN_C
WARNING_ORANGE = ORANGE
ERROR_RED = RED_C
LIMIT_PURPLE = PURPLE_B
MAIN_WHITE = WHITE

COLOR_MAP = {
    "normal": CYAN,
    "main": MAIN_WHITE,
    "valid": VALID_GREEN,
    "warning": WARNING_ORANGE,
    "error": ERROR_RED,
    "limit": LIMIT_PURPLE,
    "grid": OCEANIC_GRID,
    "panel": OCEANIC_PANEL,
    "background": OCEANIC_BG,
}


def apply_oceanic_next_theme() -> None:
    """Apply a dark, readable oceanic look for every scene."""

    config.background_color = OCEANIC_BG
    config.frame_rate = 30
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_width = 16
    config.frame_height = 9


apply_oceanic_next_theme()
