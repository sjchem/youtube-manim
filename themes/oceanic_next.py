from __future__ import annotations

import random

import manim as m

from .base import THEMES, apply_dark_theme

OCEANIC_DEEP_BACKGROUND = "#041A2F"
OCEANIC_BUBBLE_COLOR = "#8ED4FF"
OCEANIC_BUBBLE_HIGHLIGHT = "#E8FAFF"
OCEANIC_BUBBLE_SEED = 42
OCEANIC_RANDOM_BUBBLE_COUNT = 12
OCEANIC_FEATURE_BUBBLE_SPECS = [
    ((-5.7, 2.7, 0), 0.42, 0.021),
    ((-3.9, -2.2, 0), 0.28, 0.018),
    ((-1.2, 2.9, 0), 0.18, 0.016),
    ((2.5, -2.7, 0), 0.34, 0.018),
    ((4.8, 1.9, 0), 0.52, 0.019),
    ((5.9, -0.8, 0), 0.22, 0.015),
]


def _random_bubble_specs() -> list[tuple[tuple[float, float, float], float, float]]:
    """Create stable random bubbles for a calm Oceanic background."""

    rng = random.Random(OCEANIC_BUBBLE_SEED)
    specs = []
    for _ in range(OCEANIC_RANDOM_BUBBLE_COUNT):
        radius = rng.uniform(0.035, 0.13)
        x = rng.uniform(-6.7, 6.7)
        y = rng.uniform(-3.5, 3.5)
        opacity = rng.uniform(0.01, 0.026)
        specs.append(((x, y, 0), radius, opacity))
    return specs


def _oceanic_bubble(
    point: tuple[float, float, float],
    radius: float,
    opacity: float,
) -> m.VGroup:
    """Create one transparent bubble with subtle 3D highlights."""

    body = m.Circle(
        radius=radius,
        color=OCEANIC_BUBBLE_COLOR,
        stroke_width=max(0.7, radius * 5.0),
        stroke_opacity=min(opacity * 2.4, 0.12),
        fill_color=OCEANIC_BUBBLE_COLOR,
        fill_opacity=opacity,
    )
    rim = m.Circle(
        radius=radius * 0.9,
        color=OCEANIC_BUBBLE_HIGHLIGHT,
        stroke_width=max(0.5, radius * 2.8),
        stroke_opacity=min(opacity * 1.45, 0.075),
        fill_opacity=0,
    )
    shine = m.Circle(
        radius=radius * 0.18,
        color=OCEANIC_BUBBLE_HIGHLIGHT,
        stroke_width=0,
        fill_opacity=min(opacity * 2.1, 0.085),
    ).shift(m.LEFT * radius * 0.34 + m.UP * radius * 0.34)
    glint = m.Circle(
        radius=radius * 0.08,
        color=OCEANIC_BUBBLE_HIGHLIGHT,
        stroke_width=0,
        fill_opacity=min(opacity * 1.8, 0.065),
    ).shift(m.LEFT * radius * 0.1 + m.UP * radius * 0.12)

    return m.VGroup(body, rim, shine, glint).move_to(point)


def apply_oceanic_next_theme(scene: m.Scene) -> None:
    """Apply the Oceanic Next dark theme with the custom deep background."""

    apply_dark_theme(scene, THEMES["oceanic_next"])
    scene.camera.background_color = OCEANIC_DEEP_BACKGROUND


def oceanic_bubbles() -> m.VGroup:
    """Create the subtle Oceanic Next bubble layer."""

    bubbles = m.VGroup()
    for point, radius, opacity in OCEANIC_FEATURE_BUBBLE_SPECS + _random_bubble_specs():
        bubbles.add(_oceanic_bubble(point, radius, opacity))
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
