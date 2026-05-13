"""Reusable Manim objects for the tennis probability scenes."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from manim import *  # noqa: F403

from config import (
    BACKGROUND,
    BALL_YELLOW,
    BLUE,
    BODY_SIZE,
    COURT_DARK,
    COURT_GREEN,
    LINE_WHITE,
    MUTED,
    RECEIVER_RED,
    SERVER_GREEN,
    SUBTITLE_SIZE,
    TENNIS_GOLD,
    TITLE_SIZE,
)


class TennisScene(Scene):
    """Base scene with shared dark styling."""

    def setup(self) -> None:
        self.camera.background_color = BACKGROUND

    def title(self, text: str) -> Text:
        title = Text(text, font_size=TITLE_SIZE, color=LINE_WHITE, weight=BOLD)
        max_width = config.frame_width - 1.0
        if title.width > max_width:
            title.scale(max_width / title.width)
        return title

    def caption(self, text: str) -> Text:
        return Text(text, font_size=BODY_SIZE, color=MUTED)


def make_court(width: float = 10.5, height: float = 5.2) -> VGroup:
    """Create a stylized top-down tennis court."""

    court = RoundedRectangle(width=width, height=height, corner_radius=0.08)
    court.set_fill(COURT_GREEN, opacity=0.95).set_stroke(LINE_WHITE, 3)
    inner = Rectangle(width=width * 0.78, height=height * 0.78).set_stroke(LINE_WHITE, 2)
    service_left = Line(UP * height * 0.39, DOWN * height * 0.39).set_stroke(LINE_WHITE, 2)
    service_line_top = Line(LEFT * width * 0.39, RIGHT * width * 0.39).shift(UP * height * 0.18)
    service_line_bottom = Line(LEFT * width * 0.39, RIGHT * width * 0.39).shift(DOWN * height * 0.18)
    net = Line(UP * height * 0.5, DOWN * height * 0.5).set_stroke("#DDE7DD", 4)
    for line in (service_line_top, service_line_bottom):
        line.set_stroke(LINE_WHITE, 2)
    return VGroup(court, inner, service_left, service_line_top, service_line_bottom, net)


def tennis_ball(radius: float = 0.16) -> VGroup:
    """Create a glowing tennis ball dot."""

    glow = Circle(radius=radius * 2.2).set_fill(BALL_YELLOW, 0.16).set_stroke(width=0)
    ball = Dot(radius=radius, color=BALL_YELLOW)
    return VGroup(glow, ball)


def formula_box(tex: str, color: str = LINE_WHITE) -> MathTex:
    """Return a large equation object."""

    return MathTex(tex, font_size=40, color=color)


def percent_label(label: str, value: float, color: str = BALL_YELLOW) -> VGroup:
    """Create a compact label/value pair."""

    top = Text(label, font_size=SUBTITLE_SIZE, color=LINE_WHITE)
    bottom = Text(f"{100 * value:.1f}%", font_size=48, color=color, weight=BOLD)
    return VGroup(top, bottom).arrange(DOWN, buff=0.18)


def branch(start: Mobject, end: Mobject, label: str, color: str = LINE_WHITE) -> VGroup:
    """Create an arrow branch with a probability label."""

    direction = end.get_center() - start.get_center()
    norm = np.linalg.norm(direction)
    unit = RIGHT if norm == 0 else direction / norm
    arrow = Arrow(
        start.get_boundary_point(unit),
        end.get_boundary_point(-unit),
        buff=0.1,
        color=color,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.16,
    )
    text = Text(label, font_size=22, color=color).next_to(arrow, UP, buff=0.1)
    return VGroup(arrow, text)
