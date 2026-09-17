"""Procedural 3D props: the padlock, the podium and the flood of card hands.

These are real 3D mobjects (prisms, cylinders, a half-torus), so a tilted
camera gives genuine depth rather than a painted fake. Every prop is built
face-on to the default camera, which keeps its labels readable at the small
camera tilts the film actually uses.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import outlined_text

STEEL = "#9FB6C7"
STEEL_DARK = "#4A6076"
BRASS = "#E8B84B"


def _shaded_prism(
    dimensions: Sequence[float],
    fill: str,
    stroke: str,
    *,
    fill_opacity: float = 1.0,
    stroke_width: float = 2.0,
) -> Prism:
    prism = Prism(dimensions=list(dimensions))
    prism.set_fill(fill, opacity=fill_opacity)
    prism.set_stroke(stroke, width=stroke_width, opacity=0.85)
    return prism


# ----------------------------------------------------------------------------
# Chapter 01: the padlock that is not really a combination lock
# ----------------------------------------------------------------------------


def padlock(accent: str = cfg.CYAN, scale: float = 1.0) -> VGroup:
    """A three-wheel padlock whose digit wheels really do turn about their axis."""
    body = _shaded_prism([3.5, 2.7, 1.1], "#0E2C49", STEEL, stroke_width=2.4)
    bevel = RoundedRectangle(
        width=3.22, height=2.44, corner_radius=0.2,
        stroke_color=accent, stroke_width=3, stroke_opacity=0.45, fill_opacity=0,
    )
    bevel.shift(OUT * 0.57)
    brand = RoundedRectangle(
        width=1.5, height=0.34, corner_radius=0.12,
        stroke_color=accent, stroke_width=2, stroke_opacity=0.35, fill_opacity=0,
    )
    brand.move_to([0, 0.92, 0.57])

    shackle = Torus(major_radius=0.74, minor_radius=0.115, u_range=(0, PI), resolution=(8, 22))
    shackle.set_fill(STEEL, opacity=1).set_stroke(STEEL_DARK, width=0.5, opacity=0.5)
    shackle.rotate(PI / 2, axis=RIGHT)
    shackle.move_to([0, 2.05, 0])

    legs = VGroup()
    for side in (-1, 1):
        leg = Cylinder(radius=0.105, height=0.78, direction=UP, resolution=(6, 14))
        leg.set_fill(STEEL, opacity=1).set_stroke(STEEL_DARK, width=0.5, opacity=0.5)
        leg.move_to([side * 0.74, 1.7, 0])
        legs.add(leg)

    # A flat VMobject is never depth-sorted in Manim's 3D camera: it is always
    # drawn last. So the window frame may be flat, but nothing flat and filled
    # can sit between the camera and a wheel, or it would hide the wheel.
    wheels = VGroup()
    windows = VGroup()
    for x in (-0.92, 0.0, 0.92):
        wheel = Cylinder(radius=0.42, height=0.62, direction=RIGHT, resolution=(8, 20))
        wheel.set_fill("#1E5C86", opacity=1).set_stroke(width=0, opacity=0)
        wheel.move_to([x, -0.28, 0.62])
        window = RoundedRectangle(
            width=0.84, height=1.08, corner_radius=0.1,
            stroke_color=accent, stroke_width=3, stroke_opacity=0.8, fill_opacity=0,
        ).move_to([x, -0.28, 0.74])
        wheels.add(wheel)
        windows.add(window)

    group = VGroup(body, bevel, brand, legs, shackle, wheels, windows)
    group.body = body
    group.shackle = shackle
    group.legs = legs
    group.wheels = wheels
    group.windows = windows
    return group.scale(scale)


def wheel_digit(value: str, color: str = cfg.WHITE, font_size: int = 54) -> Text:
    """One digit sitting on the front of a padlock wheel."""
    return outlined_text(value, font_size, color)


# ----------------------------------------------------------------------------
# Chapter 04: the podium, where a position is a different thing from a person
# ----------------------------------------------------------------------------


def podium(scale: float = 1.0) -> VGroup:
    """Silver, gold, bronze blocks in real 3D, with their ranks on the front."""
    specs = (
        ("2", 1.55, -2.0, cfg.MUTED),
        ("1", 2.25, 0.0, cfg.GOLD),
        ("3", 1.15, 2.0, cfg.ORANGE),
    )
    blocks = VGroup()
    ranks = VGroup()
    for label, height, x, color in specs:
        block = _shaded_prism([1.95, height, 1.5], "#0C2B47", color, stroke_width=2.6)
        block.move_to([x, -2.3 + height / 2, 0])
        number = outlined_text(label, 66, color)
        number.move_to(block.get_center() + OUT * 0.78)
        edge = RoundedRectangle(
            width=1.72, height=height - 0.22, corner_radius=0.1,
            stroke_color=color, stroke_width=2.4, stroke_opacity=0.45, fill_opacity=0,
        ).move_to(block.get_center() + OUT * 0.76)
        blocks.add(block)
        ranks.add(VGroup(edge, number))
    floor = Prism(dimensions=[7.2, 0.22, 2.4])
    floor.set_fill("#07203A", opacity=1).set_stroke(cfg.MUTED, width=1.6, opacity=0.4)
    floor.move_to([0, -2.41, 0])
    group = VGroup(floor, blocks, ranks)
    group.blocks = blocks
    group.ranks = ranks
    group.scale(scale)
    # Seats are read back after scaling, so a scaled podium still reports real points.
    group.tops = [block.get_top() + OUT * 0.12 for block in blocks]
    return group


def podium_order() -> tuple[int, int, int]:
    """Index of the gold, silver and bronze block inside ``podium().blocks``."""
    return (1, 0, 2)


# ----------------------------------------------------------------------------
# Chapter 09: two and a half million hands, seen as volume rather than a list
# ----------------------------------------------------------------------------


def mini_hand(width: float = 0.3, height: float = 0.42, color: str = cfg.CYAN) -> VGroup:
    """A five-card hand shrunk to a single glyph, for the closing flood."""
    cards = VGroup()
    for index in range(5):
        card = RoundedRectangle(
            width=width, height=height, corner_radius=0.03,
            stroke_color=color, stroke_width=0.9, stroke_opacity=0.8,
            fill_color="#0E3457", fill_opacity=0.9,
        )
        card.shift(RIGHT * index * width * 0.34 + UP * index * 0.016)
        # Fan about the bottom edge, the way a hand is actually held.
        card.rotate((index - 2) * 0.1, about_point=card.get_bottom())
        cards.add(card)
    return cards.center()


def hand_cloud(count: int = 150, depth: float = 5.0, seed: int = cfg.SEED) -> VGroup:
    """A drifting cloud of tiny hands, spread through real depth."""
    rng = np.random.default_rng(seed)
    cloud = VGroup()
    for _ in range(count):
        z = rng.uniform(-depth, -0.6)
        scale = np.interp(z, [-depth, -0.6], [0.55, 1.15])
        tint = rng.choice([cfg.CYAN, cfg.BLUE, cfg.PURPLE, cfg.GOLD], p=[0.45, 0.3, 0.15, 0.1])
        hand = mini_hand(color=str(tint)).scale(scale)
        hand.move_to([rng.uniform(-7.4, 7.4), rng.uniform(-4.0, 4.0), z])
        hand.set_opacity(float(np.interp(z, [-depth, -0.6], [0.28, 0.85])))
        cloud.add(hand)
    # Flat mobjects are drawn in list order, so sort far-to-near by hand.
    cloud.submobjects.sort(key=lambda mob: float(mob.get_center()[2]))
    return cloud


def card_fan(count: int = 5, spread: float = 0.42, radius: float = 4.2) -> VGroup:
    """Face-down cards fanned out along an arc, used as a transition flourish."""
    from manim_scenes.common import card_back

    fan = VGroup()
    for index in range(count):
        angle = (index - (count - 1) / 2) * spread * 0.32
        card = card_back(width=1.1, height=1.6)
        card.rotate(-angle)
        card.shift(np.array([np.sin(angle) * radius, np.cos(angle) * radius - radius, 0.04 * index]))
        fan.add(card)
    return fan.center()
