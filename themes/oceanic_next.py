from __future__ import annotations

import manim as m

from .base import THEMES, apply_dark_theme

OCEANIC_DEEP_BACKGROUND = "#061018"
OCEANIC_BUBBLE_SPECS = [
    ((-5.7, 2.7, 0), 0.42, 0.035),
    ((-3.9, -2.2, 0), 0.28, 0.028),
    ((-1.2, 2.9, 0), 0.18, 0.025),
    ((2.5, -2.7, 0), 0.34, 0.028),
    ((4.8, 1.9, 0), 0.52, 0.032),
    ((5.9, -0.8, 0), 0.22, 0.024),
]


def apply_oceanic_next_theme(scene: m.Scene) -> None:
    """Apply the Oceanic Next dark theme with the custom deep background."""

    apply_dark_theme(scene, THEMES["oceanic_next"])
    scene.camera.background_color = OCEANIC_DEEP_BACKGROUND


def oceanic_bubbles() -> m.VGroup:
    """Create the subtle Oceanic Next bubble layer."""

    bubbles = m.VGroup()
    for point, radius, opacity in OCEANIC_BUBBLE_SPECS:
        bubble = m.Circle(
            radius=radius,
            color=m.LIGHT_GREY,
            stroke_width=0,
            stroke_opacity=0,
            fill_opacity=opacity,
        ).move_to(point)
        bubbles.add(bubble)
    return bubbles


def add_oceanic_bubbles(scene: m.Scene) -> m.VGroup:
    """Add the Oceanic Next bubble layer to a scene and return it."""

    bubbles = oceanic_bubbles()
    scene.add(bubbles)
    return bubbles


def apply_oceanic_next_scene(
    scene: m.Scene,
    include_bubbles: bool = True,
) -> m.VGroup | None:
    """Apply the Oceanic Next theme and optionally add the bubble layer."""

    apply_oceanic_next_theme(scene)
    if not include_bubbles:
        return None
    return add_oceanic_bubbles(scene)
