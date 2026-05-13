"""Color helpers shared by the tennis probability scenes."""

from __future__ import annotations

from config import BALL_YELLOW, BLUE, COURT_DARK, COURT_GREEN, LINE_WHITE, RECEIVER_RED, SERVER_GREEN, TENNIS_GOLD

MANIM_COLORS = {
    "background": "#07110C",
    "court": COURT_GREEN,
    "court_dark": COURT_DARK,
    "line": LINE_WHITE,
    "ball": BALL_YELLOW,
    "gold": TENNIS_GOLD,
    "server": SERVER_GREEN,
    "receiver": RECEIVER_RED,
    "blue": BLUE,
}


def hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    """Convert #RRGGBB to an RGB tuple in [0, 1]."""

    clean = hex_color.lstrip("#")
    return tuple(int(clean[index : index + 2], 16) / 255 for index in (0, 2, 4))
