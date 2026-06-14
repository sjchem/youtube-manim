"""Shared Manim helpers for the division-by-zero animation project."""

from __future__ import annotations

import os
from random import Random
from typing import Iterable, Sequence

import numpy as np
from manim import *

from config import (
    COLOR_MAP,
    CYAN,
    CYAN_BRIGHT,
    ERROR_RED,
    LIMIT_PURPLE,
    MAIN_WHITE,
    OCEANIC_BG,
    OCEANIC_GRID,
    OCEANIC_PANEL,
    VALID_GREEN,
    WARNING_ORANGE,
    apply_oceanic_next_theme,
)


def reset_camera(scene: Scene) -> None:
    if hasattr(scene, "camera") and hasattr(scene.camera, "frame"):
        scene.camera.frame.move_to(ORIGIN)
        scene.camera.frame.set(width=config.frame_width)


def add_oceanic_background(scene: Scene) -> VGroup:
    """Add a subtle scientific grid and glow field."""

    apply_oceanic_next_theme()
    plane = NumberPlane(
        x_range=(-9, 9, 1),
        y_range=(-5, 5, 1),
        axis_config={
            "stroke_opacity": 0,
            "include_ticks": False,
            "include_tip": False,
        },
        background_line_style={
            "stroke_color": OCEANIC_GRID,
            "stroke_width": 1,
            "stroke_opacity": 0.25,
        },
    )
    plane.x_axis.set_opacity(0)
    plane.y_axis.set_opacity(0)
    plane.set_z_index(-10)
    rings = VGroup(
        Circle(radius=1.6, color=CYAN, stroke_opacity=0.07, stroke_width=2),
        Circle(radius=2.6, color=CYAN, stroke_opacity=0.045, stroke_width=2),
        Circle(radius=3.8, color=LIMIT_PURPLE, stroke_opacity=0.035, stroke_width=2),
    )
    rings.set_z_index(-9)
    bg = VGroup(plane, rings)
    scene.add(bg)
    return bg


def glow(mobject: Mobject, color=CYAN, layers: int = 3, stroke_width: float = 10) -> VGroup:
    """Wrap a mobject with soft duplicate strokes to mimic glow."""

    halos = VGroup()
    for index in range(layers, 0, -1):
        halo = mobject.copy()
        halo.set_color(color)
        if hasattr(halo, "set_stroke"):
            halo.set_stroke(color=color, width=stroke_width * index, opacity=0.07 / index)
        if hasattr(halo, "set_fill"):
            halo.set_fill(opacity=0)
        halos.add(halo)
    return VGroup(halos, mobject)


def glowing_text(text: str, font_size: int = 54, color=MAIN_WHITE) -> VGroup:
    label = Text(text, font_size=font_size, color=color, weight=BOLD)
    return glow(label, color=color, layers=2, stroke_width=7)


def math_eq(tex: str, font_size: int = 64, color=MAIN_WHITE) -> MathTex:
    eq = MathTex(tex, font_size=font_size, color=color)
    eq.set_stroke(width=1, opacity=0.9)
    return eq


def reveal_equation(scene: Scene, eq: Mobject, run_time: float = 1.0) -> None:
    scene.play(Write(eq), run_time=run_time)
    scene.play(eq.animate.scale(1.03), run_time=0.18)
    scene.play(eq.animate.scale(1 / 1.03), run_time=0.18)


def short_label(text: str, color=CYAN, font_size: int = 32) -> Text:
    return Text(text, font_size=font_size, color=color, weight=MEDIUM)


def warning_label(text: str, font_size: int = 46) -> VGroup:
    return glowing_text(text, font_size=font_size, color=WARNING_ORANGE)


def calculator_panel(width: float = 6.3, height: float = 2.3) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=CYAN,
        stroke_width=2,
        fill_color=OCEANIC_PANEL,
        fill_opacity=0.52,
    )


def camera_zoom(scene: Scene, target: Mobject, scale: float = 0.75, run_time: float = 1.0) -> None:
    if hasattr(scene.camera, "frame"):
        scene.play(scene.camera.frame.animate.move_to(target).scale(scale), run_time=run_time)


def error_glitch_effect(scene: Scene, mobject: Mobject, flashes: int = 5) -> None:
    rng = Random(11)
    original = mobject.copy()
    for _ in range(flashes):
        shift = np.array([rng.uniform(-0.08, 0.08), rng.uniform(-0.05, 0.05), 0])
        scene.play(
            mobject.animate.shift(shift).set_color(rng.choice([ERROR_RED, WARNING_ORANGE, CYAN])),
            run_time=0.055,
        )
    scene.play(Transform(mobject, original), run_time=0.12)


def dot_grid(count: int, color=CYAN, radius: float = 0.075, cols: int = 6) -> VGroup:
    dots = VGroup()
    for i in range(count):
        row = i // cols
        col = i % cols
        dots.add(Dot(radius=radius, color=color).move_to([col * 0.36, -row * 0.36, 0]))
    dots.center()
    return dots


def grouping_boxes(group_count: int, width: float = 1.4, height: float = 1.6) -> VGroup:
    boxes = VGroup()
    for _ in range(group_count):
        boxes.add(
            RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.14,
                stroke_color=CYAN,
                stroke_width=2,
                fill_opacity=0,
            )
        )
    boxes.arrange(RIGHT, buff=0.55)
    return boxes


def arrange_dots_into_boxes(dots: VGroup, boxes: VGroup, per_box: int) -> list[np.ndarray]:
    targets: list[np.ndarray] = []
    offsets = [
        np.array([-0.32, 0.34, 0]),
        np.array([0.0, 0.34, 0]),
        np.array([0.32, 0.34, 0]),
        np.array([-0.16, -0.16, 0]),
        np.array([0.16, -0.16, 0]),
    ]
    for i, _dot in enumerate(dots):
        box = boxes[i // per_box]
        targets.append(box.get_center() + offsets[i % per_box])
    return targets


def number_tokens(values: Sequence[str], color=MAIN_WHITE) -> VGroup:
    tokens = VGroup()
    for value in values:
        token = math_eq(value, font_size=42, color=color)
        tokens.add(token)
    tokens.arrange(RIGHT, buff=0.75)
    return tokens


def collapse_to_zero(scene: Scene, tokens: VGroup, zero_point=ORIGIN, run_time: float = 1.8) -> None:
    trails = VGroup()
    for token in tokens:
        trail = Line(token.get_center(), zero_point, color=CYAN, stroke_opacity=0.22, stroke_width=2)
        trails.add(trail)
    zero = glow(math_eq("0", font_size=78, color=MAIN_WHITE).move_to(zero_point), CYAN)
    scene.play(Create(trails), run_time=0.5)
    scene.play(
        *[token.animate.move_to(zero_point).scale(0.55).set_opacity(0.25) for token in tokens],
        FadeIn(zero),
        run_time=run_time,
        rate_func=rate_functions.ease_in_cubic,
    )
    scene.play(FadeOut(trails), run_time=0.35)


def graph_axes() -> Axes:
    return Axes(
        x_range=(-4, 4, 1),
        y_range=(-8, 8, 2),
        x_length=9,
        y_length=5.4,
        axis_config={"color": CYAN_BRIGHT, "stroke_opacity": 0.75},
        tips=False,
    )


def terminal_panel(lines: Iterable[tuple[str, str]], width: float = 8.4, height: float = 4.3) -> VGroup:
    panel = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        stroke_color=CYAN,
        stroke_width=2,
        fill_color="#071018",
        fill_opacity=0.82,
    )
    rendered = VGroup()
    for code, color in lines:
        rendered.add(Text(code, font="Monospace", font_size=30, color=color))
    rendered.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    rendered.move_to(panel.get_center()).shift(LEFT * 0.18)
    return VGroup(panel, rendered)


def clear_scene(scene: Scene, run_time: float = 0.75) -> None:
    if scene.mobjects:
        scene.play(FadeOut(*scene.mobjects), run_time=run_time)
    reset_camera(scene)


def optional_sound(scene: Scene, path: str, gain: float = -12) -> None:
    if os.path.exists(path):
        scene.add_sound(path, gain=gain)
