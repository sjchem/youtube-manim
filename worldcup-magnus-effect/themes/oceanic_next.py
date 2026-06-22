"""Small Oceanic Next theme shim used by the project scenes.

The parent repository normally provides this theme, but this project keeps a
local import-compatible copy so renders are reproducible from the folder alone.
"""

from __future__ import annotations

from math import sin

from manim import Circle, VGroup, config

OCEANIC = {
    "background": "#08111A",
    "background_2": "#0D1B2A",
    "cyan": "#5FB3B3",
    "blue": "#6699CC",
    "green": "#99C794",
    "orange": "#F99157",
    "red": "#EC5F67",
    "purple": "#C594C5",
    "white": "#D8DEE9",
    "muted": "#65737E",
    "line": "#1F3443",
}


def apply_oceanic_next_theme() -> None:
    """Apply project-wide Manim defaults."""
    config.background_color = OCEANIC["background"]
    config.frame_width = 16
    config.frame_height = 9
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 30


def oceanic_bubbles(
    count: int = 36,
    width: float = 16.0,
    height: float = 9.0,
    opacity: float = 0.12,
    radius: float = 0.035,
) -> VGroup:
    """Return subtle deterministic bubble dots for Oceanic backgrounds."""
    bubbles = VGroup()
    for index in range(count):
        x = -width / 2 + ((index * 2.817) % width)
        y = -height / 2 + ((index * 1.631 + sin(index) * 0.33) % height)
        r = radius * (0.7 + (index % 5) * 0.22)
        bubble = Circle(
            radius=r,
            stroke_color=OCEANIC["cyan"],
            stroke_width=1.2,
            stroke_opacity=opacity * (0.55 + (index % 4) * 0.12),
            fill_opacity=0,
        )
        bubble.move_to([x, y, 0])
        bubbles.add(bubble)
    return bubbles

