from __future__ import annotations

import random
from typing import Iterable

import numpy as np
from manim import *

from utils.style import (
    BLUE_GLOW,
    GOLD_GLOW,
    GREEN_GLOW,
    MUTED_TEXT,
    TEXT_COLOR,
    glow_text,
    small_label,
)


def make_glowing_dot(point: np.ndarray, color: str = BLUE_GLOW, radius: float = 0.04) -> VGroup:
    dot = Dot(point=point, radius=radius, color=color)
    halo = Dot(point=point, radius=radius * 2.8, color=color, fill_opacity=0.16, stroke_opacity=0)
    return VGroup(halo, dot)


def create_particle_field(
    num_particles: int = 80,
    bounds: tuple[float, float, float, float] = (-7.0, 7.0, -3.8, 3.8),
    color: str = BLUE_GLOW,
    seed: int = 7,
) -> VGroup:
    rng = np.random.default_rng(seed)
    x_min, x_max, y_min, y_max = bounds
    particles = VGroup()
    for _ in range(num_particles):
        point = np.array([rng.uniform(x_min, x_max), rng.uniform(y_min, y_max), 0])
        p = Dot(point=point, radius=rng.uniform(0.012, 0.032), color=color, fill_opacity=rng.uniform(0.28, 0.8))
        p.velocity = np.array([rng.uniform(-0.08, 0.08), rng.uniform(-0.05, 0.05), 0])
        particles.add(p)
    return particles


def add_particle_drift(particles: VGroup, bounds: tuple[float, float, float, float] = (-7.2, 7.2, -4, 4)) -> VGroup:
    x_min, x_max, y_min, y_max = bounds
    for dot in particles:
        def drift(mob: Mobject, dt: float) -> None:
            mob.shift(mob.velocity * dt)
            x, y, _ = mob.get_center()
            if x < x_min or x > x_max:
                mob.velocity[0] *= -1
            if y < y_min or y > y_max:
                mob.velocity[1] *= -1
        dot.add_updater(drift)
    return particles


def animate_equation_reveal(scene: Scene, equation: Mobject, run_time: float = 1.4) -> None:
    scene.play(FadeIn(glow_text(equation, BLUE_GLOW, opacity=0.15), shift=UP * 0.08), run_time=run_time)


def create_label(text: str, position: np.ndarray, color: str = MUTED_TEXT) -> Text:
    label = small_label(text, color=color)
    label.move_to(position)
    return label


def fade_all(scene: Scene, except_mobjects: Iterable[Mobject] | None = None, run_time: float = 0.8) -> None:
    keep = set(except_mobjects or [])
    fading = [m for m in scene.mobjects if m not in keep]
    if fading:
        scene.play(*[FadeOut(m) for m in fading], run_time=run_time)


def cinematic_wait(scene: Scene, seconds: float = 0.7) -> None:
    scene.wait(seconds)


def jagged_path(start: np.ndarray, end: np.ndarray, segments: int = 13, amplitude: float = 0.35, seed: int = 12) -> VMobject:
    rng = random.Random(seed)
    points = []
    for i in range(segments + 1):
        alpha = i / segments
        point = interpolate(start, end, alpha)
        if 0 < i < segments:
            point += np.array([rng.uniform(-amplitude, amplitude), rng.uniform(-amplitude, amplitude), 0])
        points.append(point)
    path = VMobject()
    path.set_points_as_corners(points)
    path.set_stroke(GOLD_GLOW, width=5)
    return path


def value_label(prefix: str, tracker: ValueTracker, decimals: int = 0, suffix: str = "") -> VGroup:
    number = DecimalNumber(tracker.get_value(), num_decimal_places=decimals, color=TEXT_COLOR, font_size=26)
    number.add_updater(lambda m: m.set_value(tracker.get_value()))
    return VGroup(Text(prefix, font_size=24, color=MUTED_TEXT), number, Text(suffix, font_size=24, color=MUTED_TEXT)).arrange(RIGHT, buff=0.08)


def probability_of_success(p: float, n: float) -> float:
    return 1 - (1 - p) ** n


def mini_icon(label: str, color: str = BLUE_GLOW) -> VGroup:
    box = RoundedRectangle(corner_radius=0.08, width=1.05, height=0.72, stroke_color=color, fill_color=color, fill_opacity=0.08)
    text = Text(label, font_size=18, color=TEXT_COLOR)
    text.move_to(box.get_center())
    return VGroup(box, text)
