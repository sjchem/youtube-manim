"""Reusable visual primitives for the motivation physics scenes."""

from __future__ import annotations

import math
import random

import numpy as np
from manim import *

from config import (
    ACCENT_YELLOW,
    BACKGROUND_COLOR,
    BALL_RADIUS,
    DEFAULT_GLOW_STROKE_WIDTH,
    DEFAULT_STROKE_WIDTH,
    DIM_TEXT_COLOR,
    EQUATION_SCALE,
    GRID_COLOR,
    LABEL_FONT_SIZE,
    PRIMARY_GLOW,
    SECONDARY_GLOW,
    SMALL_FONT_SIZE,
    SUCCESS_COLOR,
    SURFACE_COLOR,
    TEXT_COLOR,
    TITLE_FONT_SIZE,
    WARNING_COLOR,
)


def set_scene_style(scene: Scene):
    scene.camera.background_color = BACKGROUND_COLOR


def soft_background():
    grid = NumberPlane(
        x_range=[-9, 9, 1],
        y_range=[-5, 5, 1],
        background_line_style={
            "stroke_color": GRID_COLOR,
            "stroke_width": 1,
            "stroke_opacity": 0.28,
        },
    )
    # Hide the central x/y axes so the scene isn't split into four quadrants
    try:
        grid.x_axis.set_stroke(opacity=0)
        grid.y_axis.set_stroke(opacity=0)
        grid.x_axis.set_opacity(0)
        grid.y_axis.set_opacity(0)
    except Exception:
        pass
    vignette = Rectangle(width=16.5, height=9.5, color=BACKGROUND_COLOR)
    vignette.set_fill(BACKGROUND_COLOR, opacity=0.18)
    vignette.set_stroke(opacity=0)
    return VGroup(grid, vignette)


def glowing_text(text, font_size=TITLE_FONT_SIZE, color=TEXT_COLOR, glow_color=PRIMARY_GLOW):
    base = Text(text, font_size=font_size, color=color)
    glow = base.copy().set_color(glow_color).set_opacity(0.22)
    glow.scale(1.012)
    return VGroup(glow, base)


def label_text(text, font_size=LABEL_FONT_SIZE, color=TEXT_COLOR):
    return Text(text, font_size=font_size, color=color)


def label_badge(text, color=PRIMARY_GLOW, font_size=SMALL_FONT_SIZE):
    label = Text(text, font_size=font_size, color=TEXT_COLOR)
    box = RoundedRectangle(
        corner_radius=0.08,
        width=label.width + 0.38,
        height=label.height + 0.18,
        stroke_color=color,
        stroke_opacity=0.75,
        stroke_width=1.5,
        fill_color=BACKGROUND_COLOR,
        fill_opacity=0.72,
    )
    return VGroup(box, label)


def force_arrow(
    start,
    end,
    color=PRIMARY_GLOW,
    label=None,
    buff=0.0,
    label_font_size=SMALL_FONT_SIZE,
    label_direction=UP,
):
    arrow = Arrow(
        start=start,
        end=end,
        buff=buff,
        color=color,
        stroke_width=DEFAULT_STROKE_WIDTH,
        max_tip_length_to_length_ratio=0.16,
    )
    glow = arrow.copy().set_stroke(color=color, width=DEFAULT_GLOW_STROKE_WIDTH, opacity=0.17)
    group = VGroup(glow, arrow)
    if label:
        text = Text(label, font_size=label_font_size, color=color)
        text.next_to(arrow, label_direction, buff=0.12)
        group.add(text)
    return group


def friction_arrow(start, end, label=None, label_font_size=SMALL_FONT_SIZE, label_direction=UP):
    return force_arrow(
        start,
        end,
        color=WARNING_COLOR,
        label=label,
        label_font_size=label_font_size,
        label_direction=label_direction,
    )


def rolling_ball(radius=BALL_RADIUS, color=PRIMARY_GLOW):
    ball = Circle(radius=radius, stroke_color=color, stroke_width=2.5)
    ball.set_fill(color, opacity=0.88)
    highlight = Dot(radius=radius * 0.22, color=WHITE).move_to(ball.get_center() + 0.07 * UL)
    highlight.set_opacity(0.7)
    glow = Circle(radius=radius * 1.55, stroke_color=color, stroke_width=10)
    glow.set_opacity(0.17)
    return VGroup(glow, ball, highlight)


def spark(radius=0.12, color=PRIMARY_GLOW):
    center = Dot(radius=radius, color=color)
    rays = VGroup()
    for angle in np.linspace(0, TAU, 10, endpoint=False):
        ray = Line(
            radius * 1.5 * np.array([math.cos(angle), math.sin(angle), 0]),
            radius * 3.2 * np.array([math.cos(angle), math.sin(angle), 0]),
            color=color,
            stroke_width=2,
        )
        rays.add(ray)
    glow = Circle(radius=radius * 4.2, stroke_color=color, stroke_width=12, stroke_opacity=0.16)
    return VGroup(glow, rays, center)


def surface_line(width=7.5, y=-2.2, rough=False):
    if rough:
        points = []
        xs = np.linspace(-width / 2, width / 2, 80)
        for i, x in enumerate(xs):
            points.append([x, y + 0.035 * math.sin(i * 2.6), 0])
        line = VMobject(color=SURFACE_COLOR, stroke_width=4)
        line.set_points_smoothly(points)
    else:
        line = Line(LEFT * width / 2 + UP * y, RIGHT * width / 2 + UP * y)
        line.set_stroke(SURFACE_COLOR, width=4)
    return line


def graph_axes(x_range=(0, 8, 1), y_range=(0, 1.2, 0.2), width=8.2, height=4.2):
    axes = Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=width,
        y_length=height,
        tips=False,
        axis_config={"color": DIM_TEXT_COLOR, "stroke_width": 2},
    )
    return axes


def glowing_curve(curve, color=PRIMARY_GLOW):
    glow = curve.copy().set_stroke(color=color, width=11, opacity=0.18)
    core = curve.copy().set_stroke(color=color, width=3.4, opacity=1.0)
    return VGroup(glow, core)


def particle_burst(center=ORIGIN, count=36, color=PRIMARY_GLOW, radius=1.0, seed=7):
    rng = random.Random(seed)
    particles = VGroup()
    for _ in range(count):
        angle = rng.random() * TAU
        distance = radius * (0.25 + 0.75 * rng.random())
        dot = Dot(radius=0.025 + 0.018 * rng.random(), color=color)
        dot.move_to(center + distance * np.array([math.cos(angle), math.sin(angle), 0]))
        dot.set_opacity(0.35 + 0.45 * rng.random())
        particles.add(dot)
    return particles


def motion_trail(points, color=PRIMARY_GLOW, max_width=5):
    trail = VGroup()
    for idx in range(len(points) - 1):
        opacity = 0.08 + 0.45 * idx / max(1, len(points) - 1)
        width = 1 + max_width * idx / max(1, len(points) - 1)
        segment = Line(points[idx], points[idx + 1], color=color, stroke_width=width)
        segment.set_opacity(opacity)
        trail.add(segment)
    return trail


def equation_mobject(tex, color=TEXT_COLOR, scale=EQUATION_SCALE):
    eq = MathTex(tex, color=color)
    eq.scale(scale)
    return eq


def equation_reveal(scene: Scene, tex, position=ORIGIN, scale=EQUATION_SCALE, color=TEXT_COLOR):
    eq = equation_mobject(tex, color=color, scale=scale).move_to(position)
    scene.play(Write(eq), run_time=1.6)
    scene.wait(0.6)
    return eq


def cinematic_title_card(title, subtitle=None):
    title_mob = glowing_text(title, font_size=TITLE_FONT_SIZE, color=TEXT_COLOR)
    if subtitle:
        subtitle_mob = Text(subtitle, font_size=30, color=DIM_TEXT_COLOR)
        subtitle_mob.next_to(title_mob, DOWN, buff=0.24)
        return VGroup(title_mob, subtitle_mob)
    return title_mob


def icon_symbol(kind, color=SECONDARY_GLOW):
    if kind == "gym":
        left = Rectangle(width=0.12, height=0.55, color=color).set_fill(color, 0.9)
        right = left.copy()
        bar = Line(LEFT * 0.45, RIGHT * 0.45, color=color, stroke_width=4)
        left.next_to(bar, LEFT, buff=0.02)
        right.next_to(bar, RIGHT, buff=0.02)
        return VGroup(left, bar, right)
    if kind == "study":
        book = Rectangle(width=0.7, height=0.5, color=color)
        book.set_fill(color, 0.18)
        spine = Line(book.get_left(), book.get_left() + UP * 0.5, color=color)
        return VGroup(book, spine)
    if kind == "project":
        gear = RegularPolygon(n=8, radius=0.34, color=color)
        gear.set_fill(color, 0.15)
        hole = Circle(radius=0.12, color=BACKGROUND_COLOR).set_fill(BACKGROUND_COLOR, 1)
        return VGroup(gear, hole)
    if kind == "calendar":
        rect = Rectangle(width=0.68, height=0.55, color=color)
        rect.set_fill(color, 0.12)
        line = Line(rect.get_left() + UP * 0.12, rect.get_right() + UP * 0.12, color=color)
        return VGroup(rect, line)
    return Dot(color=color)


def simple_clock(radius=0.65):
    face = Circle(radius=radius, color=DIM_TEXT_COLOR, stroke_width=2)
    hour = Line(ORIGIN, UP * radius * 0.45, color=TEXT_COLOR, stroke_width=3)
    minute = Line(ORIGIN, RIGHT * radius * 0.62, color=PRIMARY_GLOW, stroke_width=3)
    return VGroup(face, hour, minute)


def loop_node(text, color=PRIMARY_GLOW):
    dot = Circle(radius=0.66, color=color, stroke_width=2)
    dot.set_fill(BACKGROUND_COLOR, 0.85)
    label = Text(text, font_size=24, color=TEXT_COLOR)
    if label.width > dot.width * 0.9:
        label.scale_to_fit_width(dot.width * 0.9)
    if label.height > dot.height * 0.82:
        label.scale_to_fit_height(dot.height * 0.82)
    return VGroup(dot, label)


def curved_loop_arrow(start, end, color=PRIMARY_GLOW, angle=TAU / 7):
    arrow = CurvedArrow(start, end, angle=angle, color=color, stroke_width=2.5)
    glow = arrow.copy().set_stroke(color=color, width=8, opacity=0.16)
    return VGroup(glow, arrow)


def subtle_end_card():
    line = Line(LEFT * 2.2, RIGHT * 2.2, color=DIM_TEXT_COLOR, stroke_width=1.5)
    text = Text("Subscribe for science stories", font_size=22, color=DIM_TEXT_COLOR)
    text.next_to(line, DOWN, buff=0.18)
    return VGroup(line, text)
