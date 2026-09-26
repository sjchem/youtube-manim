"""Procedurally drawn objects: the things the film sorts.

Set theory only becomes concrete when the elements are *things*, not letters,
so every card carries a drawing. Each icon here is built from plain Manim
geometry around the origin at roughly one unit tall, which keeps the film free
of image assets and keeps every card crisp at 1440p.

The lookup at the bottom is the single source of truth: a scene names an
element (``"platypus"``) and gets its drawing, so the names in
``utils.set_models`` and the pictures on screen can never drift apart.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from manim import *

import config as cfg

# Ink colours for the drawings. These are illustration colours, not the
# semantic palette: a carrot is orange because carrots are orange, and that
# carries no meaning about regions.
LEAF = "#73EA83"
APPLE_RED = "#FF5E77"
BANANA_YELLOW = "#FFE265"
BERRY = "#FF7A85"
GRAPE = "#B69CFF"
CARROT = "#FF9F43"
CRUST = "#E7B25C"
CHEESE = "#FFF0C2"
TOMATO = "#FF5E77"
FUR = "#F2B37A"
TIGER_FUR = "#FFA94D"
DOG_FUR = "#C9A227"
WHALE_BLUE = "#65CFFF"
FEATHER = "#F4FAFF"
DUCK_BROWN = "#D9B27C"
BILL = "#FF9F43"
PLATY_BROWN = "#E0A76D"
SNAKE_GREEN = "#78D98B"
SHELL = "#FFE9B0"
MEAT_PINK = "#F08585"
MUSHROOM = "#D8C3A5"
OLIVE_GREEN = "#B0D95B"
ONION = "#E7C6E8"
PEPPER = "#6FD18A"

STROKE = 3.6


# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------


def _filled(mob: VMobject, color: str, opacity: float = 0.34, width: float = STROKE) -> VMobject:
    return mob.set_stroke(color, width=width).set_fill(color, opacity=max(opacity, 0.82))


def _crescent(
    start: Sequence[float],
    end: Sequence[float],
    outer_angle: float,
    inner_angle: float,
    color: str,
    opacity: float = 0.34,
) -> VMobject:
    """A closed sliver between two arcs — bananas, whale flukes, bacon."""
    outer = ArcBetweenPoints(np.array(start), np.array(end), angle=outer_angle)
    inner = ArcBetweenPoints(np.array(end), np.array(start), angle=inner_angle)
    shape = VMobject()
    shape.set_points(np.vstack([outer.points, inner.points]))
    return _filled(shape, color, opacity)


def _dot_cluster(points: Sequence[Sequence[float]], radius: float, color: str) -> VGroup:
    return VGroup(*[
        Dot(np.array(point), radius=radius, color=color, fill_opacity=0.9)
        for point in points
    ])


def _leaf_blade(color: str = LEAF, scale: float = 1.0, angle: float = 0.0) -> VMobject:
    blade = _crescent([-0.22, 0.0, 0], [0.22, 0.0, 0], -0.9, -0.9, color, 0.45)
    return blade.scale(scale).rotate(angle)


def _stem(height: float = 0.2, color: str = "#8A6B3F") -> Line:
    return Line(ORIGIN, UP * height, color=color, stroke_width=4.5)


def _eye(color: str = "#0B1F33", radius: float = 0.038) -> Dot:
    return Dot(radius=radius, color=color, fill_opacity=1)


# ---------------------------------------------------------------------------
# Fruit and food
# ---------------------------------------------------------------------------


def apple() -> VGroup:
    left = Circle(radius=0.32).shift(LEFT * 0.11 + DOWN * 0.05)
    right = Circle(radius=0.32).shift(RIGHT * 0.11 + DOWN * 0.05)
    body = VGroup(_filled(left, APPLE_RED), _filled(right, APPLE_RED))
    notch = Arc(radius=0.14, start_angle=0, angle=PI, color=APPLE_RED, stroke_width=3)
    notch.move_to([0, 0.24, 0])
    stem = _stem(0.22).move_to([0, 0.34, 0])
    leaf = _leaf_blade(LEAF, 0.85, 0.5).move_to([0.17, 0.4, 0])
    return VGroup(body, notch, stem, leaf)


def banana() -> VGroup:
    body = _crescent([-0.3, 0.3, 0], [0.34, -0.22, 0], -1.55, 0.72, BANANA_YELLOW, 0.4)
    stub = Line([-0.3, 0.3, 0], [-0.36, 0.44, 0], color="#8A6B3F", stroke_width=4.5)
    tip = Line([0.34, -0.22, 0], [0.42, -0.34, 0], color="#8A6B3F", stroke_width=4.5)
    return VGroup(body, stub, tip)


def strawberry() -> VGroup:
    body = VMobject()
    outer = ArcBetweenPoints([-0.36, 0.16, 0], [0.36, 0.16, 0], angle=-3.3)
    close = ArcBetweenPoints([0.36, 0.16, 0], [0.0, -0.38, 0], angle=1.0)
    back = ArcBetweenPoints([0.0, -0.38, 0], [-0.36, 0.16, 0], angle=1.0)
    body.set_points(np.vstack([outer.points, close.points, back.points]))
    _filled(body, BERRY, 0.4)
    calyx = VGroup(*[
        _leaf_blade(LEAF, 0.75, angle).move_to([0.2 * np.cos(angle), 0.26 + 0.07 * np.sin(angle), 0])
        for angle in (-0.5, 0.0, 0.5)
    ])
    seeds = _dot_cluster(
        [[-0.16, 0.0, 0], [0.16, 0.02, 0], [0.0, -0.1, 0], [-0.08, -0.24, 0], [0.09, -0.22, 0]],
        0.025, "#FFE9B0",
    )
    return VGroup(body, calyx, seeds)


def grapes() -> VGroup:
    rows = ((-0.19, 0.19), (-0.285, -0.095, 0.095, 0.285), (-0.19, 0.19), (0.0,))
    cluster = VGroup()
    for row_index, xs in enumerate(rows):
        for x in xs:
            berry = Circle(radius=0.115).move_to([x, 0.16 - row_index * 0.195, 0])
            cluster.add(_filled(berry, GRAPE, 0.45, 2.6))
    stem = _stem(0.2).move_to([0.0, 0.4, 0])
    leaf = _leaf_blade(LEAF, 0.8, -0.5).move_to([-0.17, 0.44, 0])
    return VGroup(cluster, stem, leaf)


def carrot() -> VGroup:
    body = Polygon(
        [-0.2, 0.2, 0], [0.2, 0.2, 0], [0.04, -0.5, 0], [-0.04, -0.5, 0],
    )
    _filled(body, CARROT, 0.4)
    ridges = VGroup(*[
        Line([-0.15 + 0.03 * i, 0.06 - 0.16 * i, 0], [0.15 - 0.04 * i, 0.12 - 0.16 * i, 0],
             color=CARROT, stroke_width=2.4, stroke_opacity=0.75)
        for i in range(3)
    ])
    fronds = VGroup(*[
        _leaf_blade(LEAF, 0.85, angle).move_to([0.16 * np.sin(angle), 0.34, 0])
        for angle in (-0.6, 0.0, 0.6)
    ])
    return VGroup(body, ridges, fronds)


def pizza_slice() -> VGroup:
    body = Polygon([0.0, -0.46, 0], [-0.36, 0.34, 0], [0.36, 0.34, 0])
    _filled(body, CHEESE, 0.3)
    crust = ArcBetweenPoints([-0.36, 0.34, 0], [0.36, 0.34, 0], angle=-0.55)
    crust.set_stroke(CRUST, width=9)
    pepperoni = _dot_cluster([[-0.13, 0.13, 0], [0.13, 0.08, 0], [0.0, -0.14, 0]], 0.062, TOMATO)
    return VGroup(body, crust, pepperoni)


# ---------------------------------------------------------------------------
# Animals
# ---------------------------------------------------------------------------


def _cat_face(fur: str, stripes: bool = False) -> VGroup:
    head = _filled(Circle(radius=0.34), fur, 0.3)
    ears = VGroup(
        Polygon([-0.32, 0.18, 0], [-0.3, 0.52, 0], [-0.06, 0.28, 0]),
        Polygon([0.32, 0.18, 0], [0.3, 0.52, 0], [0.06, 0.28, 0]),
    )
    for ear in ears:
        _filled(ear, fur, 0.3)
    eyes = VGroup(_eye().move_to([-0.13, 0.06, 0]), _eye().move_to([0.13, 0.06, 0]))
    nose = Triangle(color=BERRY, fill_color=BERRY, fill_opacity=0.9, stroke_width=1.6)
    nose.scale(0.05).rotate(PI).move_to([0, -0.08, 0])
    whiskers = VGroup(*[
        Line([side * 0.1, -0.12 + offset, 0], [side * 0.42, -0.08 + offset * 1.6, 0],
             color=cfg.MUTED, stroke_width=2, stroke_opacity=0.8)
        for side in (-1, 1) for offset in (-0.05, 0.05)
    ])
    face = VGroup(head, ears, eyes, nose, whiskers)
    if stripes:
        face.add(VGroup(*[
            Line([-0.1 + i * 0.1, 0.26, 0], [-0.08 + i * 0.1, 0.42, 0],
                 color="#8A4B1E", stroke_width=3)
            for i in range(3)
        ]))
    return face


def cat() -> VGroup:
    return _cat_face(FUR)


def tiger() -> VGroup:
    return _cat_face(TIGER_FUR, stripes=True)


def dog() -> VGroup:
    head = _filled(Circle(radius=0.32), DOG_FUR, 0.3)
    ears = VGroup(
        _filled(Ellipse(width=0.2, height=0.42), DOG_FUR, 0.4).move_to([-0.34, 0.14, 0]).rotate(0.3),
        _filled(Ellipse(width=0.2, height=0.42), DOG_FUR, 0.4).move_to([0.34, 0.14, 0]).rotate(-0.3),
    )
    snout = _filled(Ellipse(width=0.34, height=0.24), SHELL, 0.45).move_to([0, -0.16, 0])
    nose = Dot(radius=0.055, color="#0B1F33", fill_opacity=1).move_to([0, -0.1, 0])
    eyes = VGroup(_eye().move_to([-0.13, 0.1, 0]), _eye().move_to([0.13, 0.1, 0]))
    return VGroup(ears, head, snout, nose, eyes)


def whale() -> VGroup:
    body = _filled(Ellipse(width=0.72, height=0.4), WHALE_BLUE, 0.35).shift(DOWN * 0.04)
    fluke = Polygon([0.3, -0.04, 0], [0.56, 0.2, 0], [0.5, -0.06, 0], [0.56, -0.28, 0])
    _filled(fluke, WHALE_BLUE, 0.4, 2.6)
    fin = _filled(Ellipse(width=0.2, height=0.11), WHALE_BLUE, 0.45).move_to([0.0, -0.18, 0]).rotate(-0.4)
    spout = VGroup(*[
        Line([-0.18, 0.18, 0], [-0.18 + dx, 0.42, 0], color=cfg.CYAN, stroke_width=3, stroke_opacity=0.8)
        for dx in (-0.1, 0.0, 0.1)
    ])
    eye = _eye(radius=0.032).move_to([-0.22, 0.02, 0])
    return VGroup(fluke, body, fin, spout, eye)


def chicken() -> VGroup:
    body = _filled(Ellipse(width=0.56, height=0.46), FEATHER, 0.28).move_to([0.02, -0.12, 0])
    head = _filled(Circle(radius=0.17), FEATHER, 0.28).move_to([-0.2, 0.2, 0])
    comb = VGroup(*[
        _filled(Circle(radius=0.06), APPLE_RED, 0.8, 2).move_to([-0.26 + i * 0.07, 0.36, 0])
        for i in range(3)
    ])
    beak = Polygon([-0.34, 0.2, 0], [-0.5, 0.15, 0], [-0.34, 0.11, 0])
    _filled(beak, BILL, 0.9, 2)
    tail = Polygon([0.22, -0.06, 0], [0.5, 0.18, 0], [0.46, -0.02, 0], [0.5, -0.16, 0])
    _filled(tail, FEATHER, 0.28, 2.6)
    legs = VGroup(*[
        Line([x, -0.32, 0], [x, -0.48, 0], color=BILL, stroke_width=3.2) for x in (-0.06, 0.12)
    ])
    eye = _eye(radius=0.032).move_to([-0.24, 0.23, 0])
    return VGroup(tail, body, legs, head, comb, beak, eye)


def duck() -> VGroup:
    body = _filled(Ellipse(width=0.62, height=0.4), DUCK_BROWN, 0.32).move_to([0.04, -0.14, 0])
    head = _filled(Circle(radius=0.16), DUCK_BROWN, 0.32).move_to([-0.2, 0.18, 0])
    bill = _filled(Ellipse(width=0.26, height=0.1), BILL, 0.85, 2).move_to([-0.42, 0.13, 0])
    tail = Polygon([0.3, -0.08, 0], [0.5, 0.04, 0], [0.3, -0.2, 0])
    _filled(tail, DUCK_BROWN, 0.32, 2.4)
    wave = VGroup(*[
        Line([-0.36 + i * 0.3, -0.36, 0], [-0.18 + i * 0.3, -0.36, 0],
             color=cfg.CYAN, stroke_width=3, stroke_opacity=0.6)
        for i in range(3)
    ])
    eye = _eye(radius=0.032).move_to([-0.24, 0.21, 0])
    return VGroup(tail, body, head, bill, eye, wave)


def platypus() -> VGroup:
    """A mammal that lays eggs — the film's hinge between two rules."""
    body = _filled(Ellipse(width=0.56, height=0.34), PLATY_BROWN, 0.34).move_to([0.02, -0.04, 0])
    bill = _filled(
        RoundedRectangle(width=0.26, height=0.13, corner_radius=0.06), BILL, 0.8, 2.6
    ).move_to([-0.32, -0.04, 0])
    tail = _filled(Ellipse(width=0.24, height=0.17), PLATY_BROWN, 0.45, 2.6).move_to([0.32, -0.1, 0]).rotate(-0.3)
    webs = VGroup(*[
        _filled(Ellipse(width=0.15, height=0.08), BILL, 0.6, 2).move_to([x, -0.22, 0])
        for x in (-0.14, 0.12)
    ])
    eye = _eye(radius=0.03).move_to([-0.16, 0.05, 0])
    return VGroup(tail, body, webs, bill, eye)


def snake() -> VGroup:
    path = VMobject()
    path.set_points_smoothly([
        np.array([-0.36, -0.24, 0]), np.array([-0.12, 0.06, 0]),
        np.array([0.12, -0.16, 0]), np.array([0.32, 0.12, 0]),
    ])
    path.set_stroke(SNAKE_GREEN, width=9)
    head = _filled(Ellipse(width=0.19, height=0.13), SNAKE_GREEN, 0.7, 2.4).move_to([0.38, 0.16, 0])
    tongue = Line([0.46, 0.16, 0], [0.56, 0.19, 0], color=APPLE_RED, stroke_width=2.6)
    eye = _eye(radius=0.026).move_to([0.4, 0.19, 0])
    return VGroup(path, head, tongue, eye)


def egg() -> VGroup:
    body = VMobject()
    outer = ArcBetweenPoints([-0.21, 0.04, 0], [0.21, 0.04, 0], angle=-2.0)
    close = ArcBetweenPoints([0.21, 0.04, 0], [-0.21, 0.04, 0], angle=-3.7)
    body.set_points(np.vstack([outer.points, close.points]))
    return VGroup(_filled(body, SHELL, 0.35))


# ---------------------------------------------------------------------------
# Pizza toppings
# ---------------------------------------------------------------------------


def mozzarella() -> VGroup:
    ball = _filled(Circle(radius=0.3), CHEESE, 0.4)
    shine = _filled(Circle(radius=0.08), "#FFFFFF", 0.55, 0).move_to([-0.1, 0.11, 0])
    drops = _dot_cluster([[0.3, -0.22, 0], [-0.3, -0.18, 0]], 0.045, CHEESE)
    return VGroup(ball, shine, drops)


def ricotta() -> VGroup:
    scoop = VMobject()
    dome = ArcBetweenPoints([-0.3, -0.16, 0], [0.3, -0.16, 0], angle=-2.4)
    base = Line([0.3, -0.16, 0], [-0.3, -0.16, 0])
    scoop.set_points(np.vstack([dome.points, base.points]))
    _filled(scoop, CHEESE, 0.35)
    ripples = VGroup(*[
        Arc(radius=0.14 + 0.07 * i, start_angle=PI * 0.15, angle=PI * 0.7,
            color=CHEESE, stroke_width=2.4, stroke_opacity=0.75).move_to([0, -0.02 + 0.03 * i, 0])
        for i in range(2)
    ])
    plate = Line([-0.33, -0.19, 0], [0.33, -0.19, 0], color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6)
    return VGroup(scoop, ripples, plate)


def bacon() -> VGroup:
    strips = VGroup()
    for index, shade in enumerate((MEAT_PINK, "#FFE1E1")):
        strip = VMobject()
        strip.set_points_smoothly([
            np.array([-0.38, -0.14 + index * 0.02, 0]), np.array([-0.13, 0.12 - index * 0.02, 0]),
            np.array([0.13, -0.12 + index * 0.02, 0]), np.array([0.38, 0.14 - index * 0.02, 0]),
        ])
        strip.set_stroke(shade, width=13 - index * 6)
        strips.add(strip)
    return strips


def sausage() -> VGroup:
    body = _filled(
        RoundedRectangle(width=0.78, height=0.3, corner_radius=0.15), MEAT_PINK, 0.4
    ).rotate(-0.25)
    ties = VGroup(*[
        Line([x, -0.2, 0], [x, 0.2, 0], color="#B65C5C", stroke_width=3, stroke_opacity=0.8).rotate(-0.25)
        for x in (-0.2, 0.2)
    ])
    return VGroup(body, ties)


def mushroom() -> VGroup:
    cap = VMobject()
    dome = ArcBetweenPoints([-0.34, 0.0, 0], [0.34, 0.0, 0], angle=-2.4)
    base = Line([0.34, 0.0, 0], [-0.34, 0.0, 0])
    cap.set_points(np.vstack([dome.points, base.points]))
    _filled(cap, MUSHROOM, 0.4)
    stem = _filled(
        RoundedRectangle(width=0.2, height=0.36, corner_radius=0.07), SHELL, 0.4
    ).move_to([0, -0.18, 0])
    spots = _dot_cluster([[-0.13, 0.14, 0], [0.12, 0.1, 0]], 0.035, "#8A6B3F")
    return VGroup(stem, cap, spots)


def olive() -> VGroup:
    body = _filled(Ellipse(width=0.46, height=0.36), OLIVE_GREEN, 0.45)
    hole = Circle(radius=0.09, color="#0B1F33", fill_color="#0B1F33", fill_opacity=1, stroke_width=0)
    pimento = _filled(Circle(radius=0.055), APPLE_RED, 0.9, 0)
    return VGroup(body, hole, pimento)


def onion() -> VGroup:
    body = _filled(Circle(radius=0.31), ONION, 0.3)
    rings = VGroup(*[
        Circle(radius=0.31 - 0.08 * i, color=ONION, stroke_width=2.4, stroke_opacity=0.7, fill_opacity=0)
        for i in range(1, 4)
    ])
    sprout = VGroup(*[
        Line([0, 0.28, 0], [0.1 * side, 0.5, 0], color=LEAF, stroke_width=3.2)
        for side in (-1, 0.2, 1)
    ])
    return VGroup(body, rings, sprout)


def pepper() -> VGroup:
    body = _filled(Ellipse(width=0.52, height=0.5), PEPPER, 0.32).move_to([0, -0.06, 0])
    lobes = VGroup(*[
        Arc(radius=0.2, start_angle=-PI / 2 - 0.5 + i * 0.5, angle=1.0,
            color=PEPPER, stroke_width=2.4, stroke_opacity=0.7).move_to([(i - 1) * 0.13, -0.1, 0])
        for i in range(3)
    ])
    stalk = _stem(0.18, LEAF).move_to([0, 0.26, 0])
    cap = _filled(Ellipse(width=0.24, height=0.1), LEAF, 0.6, 2.4).move_to([0, 0.19, 0])
    return VGroup(body, lobes, cap, stalk)


# ---------------------------------------------------------------------------
# Lookup: an element's name is the only thing a scene needs to know
# ---------------------------------------------------------------------------

ICONS: dict[str, Callable[[], VGroup]] = {
    "apple": apple,
    "banana": banana,
    "strawberry": strawberry,
    "grapes": grapes,
    "carrot": carrot,
    "pizza": pizza_slice,
    "cat": cat,
    "tiger": tiger,
    "dog": dog,
    "whale": whale,
    "chicken": chicken,
    "duck": duck,
    "platypus": platypus,
    "snake": snake,
    "egg": egg,
    "mozzarella": mozzarella,
    "ricotta": ricotta,
    "bacon": bacon,
    "sausage": sausage,
    "mushroom": mushroom,
    "olive": olive,
    "onion": onion,
    "pepper": pepper,
}

DISPLAY_NAMES: dict[str, str] = {
    "pizza": "pizza",
    "mozzarella": "mozzarella",
    "ricotta": "ricotta",
    "platypus": "platypus",
}


def icon(name: str, height: float = 0.9, *, aspect: float = 1.25) -> VGroup:
    """The drawing for one element, normalised to fit a common box.

    Fitting to a *box* rather than to a height matters: a banana and a strip of
    bacon are wide and short, and scaling those to a fixed height would burst
    them straight out of their card.
    """
    factory = ICONS.get(name)
    if factory is None:
        raise KeyError(f"No icon drawn for {name!r}; add one to manim_scenes.icons.ICONS")
    drawing = factory()
    drawing.scale_to_fit_height(height)
    if drawing.width > height * aspect:
        drawing.scale_to_fit_width(height * aspect)
    return drawing.move_to(ORIGIN)


def display_name(name: str) -> str:
    """The caption printed under a card."""
    return DISPLAY_NAMES.get(name, name)
