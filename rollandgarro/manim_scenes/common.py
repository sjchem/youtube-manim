"""Shared imports and helpers for individual Manim scene files."""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np
from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import (  # noqa: E402,F401
    BACKGROUND,
    BALL,
    CLAY,
    CLAY_DARK,
    CLAY_LIGHT,
    DEEP_NAVY,
    DRAG_COLOR,
    FRICTION_COLOR,
    GOLD,
    GRAVITY_COLOR,
    HARD_COURT,
    MAGNUS_COLOR,
    OFF_WHITE,
    RedClayScene,
    SPIN_COLOR,
    VELOCITY_COLOR,
    create_court_surface,
    create_dust_particles,
    create_equation_box,
    create_force_arrow,
    create_spin_indicator,
    create_split_screen,
    create_tennis_ball,
    create_title_card,
    create_velocity_vector,
    path_mobject,
    trajectory_with_spin,
)


def science_panel(title: str, rows: list[str], width: float = 4.5, font_size: int = 18) -> VGroup:
    """Compact scientific annotation panel for scene-specific details."""

    heading = Text(title, font_size=21, color=GOLD, weight=BOLD)
    body = VGroup(*[Text(row, font_size=font_size, color=OFF_WHITE) for row in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    content = VGroup(heading, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    box = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=content.height + 0.45,
        fill_color=DEEP_NAVY,
        fill_opacity=0.82,
        stroke_color=OFF_WHITE,
        stroke_opacity=0.25,
    )
    content.move_to(box.get_center())
    return VGroup(box, content)


def coefficient_bar(label: str, value: float, max_value: float, color: str, width: float = 2.5) -> VGroup:
    """Horizontal bar for comparing coefficients such as friction or speed retention."""

    label_text = Text(label, font_size=18, color=OFF_WHITE)
    track = Rectangle(width=width, height=0.16, fill_color="#233044", fill_opacity=1, stroke_width=0)
    fill = Rectangle(width=max(0.04, width * value / max_value), height=0.16, fill_color=color, fill_opacity=1, stroke_width=0)
    fill.align_to(track, LEFT)
    value_text = Text(f"{value:.2f}", font_size=17, color=color)
    row = VGroup(label_text, track, value_text).arrange(RIGHT, buff=0.16)
    return row


def clay_layer_stack(width: float = 4.4) -> VGroup:
    """Layered cross-section inspired by red clay court construction."""

    layers = [
        ("2 mm red brick dust", CLAY_LIGHT, 0.24),
        ("crushed brick / shale", CLAY, 0.36),
        ("limestone moisture layer", "#C9B47A", 0.38),
        ("gravel drainage base", "#5E6470", 0.42),
    ]
    parts = VGroup()
    for label, color, height in layers:
        rect = Rectangle(width=width, height=height, fill_color=color, fill_opacity=0.95, stroke_color=OFF_WHITE, stroke_opacity=0.18)
        text = Text(label, font_size=16, color=OFF_WHITE)
        text.move_to(rect.get_center())
        parts.add(VGroup(rect, text))
    parts.arrange(DOWN, buff=0.03)
    title = Text("clay is layered material", font_size=19, color=GOLD, weight=BOLD).next_to(parts, UP, buff=0.12)
    return VGroup(title, parts)


def airflow_lines(y_values: np.ndarray, color: str = "#2E5D80") -> VGroup:
    """Curved streamlines for visualizing air around a tennis ball."""

    lines = VGroup()
    for y in y_values:
        line = VMobject(color=color, stroke_opacity=0.48, stroke_width=2)
        points = []
        for x in np.linspace(-6.5, 6.5, 28):
            bend = 0.25 * math.exp(-0.28 * x * x) * np.sign(y if abs(y) > 0.1 else 1)
            wiggle = 0.06 * math.sin(2.4 * x + y)
            points.append(np.array([x, y + bend + wiggle, 0]))
        line.set_points_smoothly(points)
        lines.add(line)
    return lines


def mini_axes(width: float = 4.4, height: float = 2.4, x_label: str = "distance", y_label: str = "height") -> VGroup:
    x_axis = Line(ORIGIN, RIGHT * width, color=OFF_WHITE, stroke_opacity=0.55)
    y_axis = Line(ORIGIN, UP * height, color=OFF_WHITE, stroke_opacity=0.55)
    labels = VGroup(
        Text(x_label, font_size=15, color=OFF_WHITE).next_to(x_axis, DOWN, buff=0.08),
        Text(y_label, font_size=15, color=OFF_WHITE).next_to(y_axis, LEFT, buff=0.08).rotate(PI / 2),
    )
    return VGroup(x_axis, y_axis, labels)
