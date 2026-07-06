"""Reusable Manim helpers for the 6-7 animation."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np
from manim import *

import config as cfg


def begin_scene(scene: Scene, bubbles: bool = True) -> float:
    """Apply the Oceanic theme, reset camera, and return the start time."""

    cfg.apply_oceanic_next_theme(scene)
    if hasattr(scene.camera, "frame"):
        scene.camera.frame.set(width=cfg.FRAME_WIDTH)
        scene.camera.frame.move_to(ORIGIN)
    scene.add(cinematic_background())
    if bubbles:
        layer = cfg.oceanic_bubbles()
        layer.set_z_index(-18)
        scene.add(layer)
    return scene.time


def end_scene(scene: Scene, _scene_start: float | None = None, hold: float = 0.25) -> None:
    """Small pause used by individual scene previews."""

    scene.wait(hold)


def clear_scene(scene: Scene, run_time: float = 0.55) -> None:
    """Fade all visible mobjects between full-video sections."""

    if scene.mobjects:
        scene.play(*[FadeOut(mob) for mob in scene.mobjects], run_time=run_time)
    scene.wait(0.1)


def narration_wait(scene: Scene, seconds: float = 0.8) -> None:
    """Readable wrapper for narration beats."""

    scene.wait(seconds)


def paced_play(scene: Scene, *animations: Animation, run_time: float = 1.0, **kwargs) -> None:
    """Project-level play helper for consistent pacing."""

    scene.play(*animations, run_time=run_time, **kwargs)


def cinematic_background() -> VGroup:
    """Dark scientific background with subtle grid, particles, and rings."""

    base = Rectangle(
        width=cfg.FRAME_WIDTH * 1.35,
        height=cfg.FRAME_HEIGHT * 1.35,
        fill_color=cfg.OCEANIC_BG,
        fill_opacity=1,
        stroke_opacity=0,
    )
    base.set_z_index(-30)

    plane = NumberPlane(
        x_range=(-8, 8, 1),
        y_range=(-5, 5, 1),
        background_line_style={
            "stroke_color": cfg.GRID,
            "stroke_width": 1,
            "stroke_opacity": 0.16,
        },
        axis_config={"stroke_opacity": 0, "include_ticks": False, "include_tip": False},
    )
    plane.set_z_index(-25)

    rings = VGroup(
        Circle(radius=2.2, color=cfg.CYAN, stroke_width=2, stroke_opacity=0.05),
        Circle(radius=3.6, color=cfg.PURPLE, stroke_width=2, stroke_opacity=0.035),
        Circle(radius=5.2, color=cfg.BLUE, stroke_width=2, stroke_opacity=0.028),
    )
    rings.set_z_index(-24)

    dots = VGroup()
    for i in range(72):
        x = -6.9 + 13.8 * ((i * 37) % 101) / 100
        y = -3.65 + 7.3 * ((i * 53) % 97) / 96
        dot = Dot([x, y, 0], radius=0.012 + 0.01 * (i % 3), color=cfg.CYAN)
        dot.set_opacity(0.12 + 0.12 * ((i * 11) % 7) / 6)
        dots.add(dot)
    dots.set_z_index(-22)
    return VGroup(base, plane, rings, dots)


def fit_safe(mobject: Mobject, width: float = cfg.SAFE_WIDTH, height: float = cfg.SAFE_HEIGHT) -> Mobject:
    """Scale a mobject into the central phone-safe frame."""

    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    if mobject.height > height:
        mobject.scale_to_fit_height(height)
    return mobject


def title_block(title: str, subtitle: str | None = None, color: str = cfg.GOLD) -> VGroup:
    """Large cinematic title block."""

    title_mob = Text(title, font=cfg.TITLE_FONT, font_size=cfg.TITLE_SIZE, color=color, weight=BOLD)
    title_mob.set_stroke("#07131A", width=5, opacity=0.85, background=True)
    if subtitle is None:
        return VGroup(title_mob)
    sub = Text(subtitle, font=cfg.FONT, font_size=cfg.SUBTITLE_SIZE, color=cfg.WHITE, weight=MEDIUM)
    sub.set_stroke("#07131A", width=4, opacity=0.8, background=True)
    group = VGroup(title_mob, sub).arrange(DOWN, buff=0.22)
    return fit_safe(group, width=12.2, height=2.8)


def label(text: str, color: str = cfg.CYAN, font_size: int = cfg.LABEL_SIZE) -> Text:
    """Readable short on-screen label."""

    mob = Text(text, font=cfg.FONT, font_size=font_size, color=color, weight=BOLD)
    mob.set_stroke("#07131A", width=4, opacity=0.85, background=True)
    return fit_safe(mob, width=11.6, height=0.8)


def equation(tex: str, color: str = cfg.WHITE, font_size: int = cfg.EQUATION_SIZE) -> MathTex:
    """Readable MathTex equation."""

    mob = MathTex(tex, font_size=font_size, color=color)
    mob.set_stroke("#07131A", width=3, opacity=0.65, background=True)
    return fit_safe(mob, width=12.0, height=2.0)


def glow(mobject: Mobject, color: str = cfg.CYAN, widths=(16, 8), opacities=(0.08, 0.16)) -> VGroup:
    """Wrap an object with soft glow strokes."""

    layers = VGroup()
    for width, opacity in zip(widths, opacities):
        halo = mobject.copy()
        halo.set_stroke(color=color, width=width, opacity=opacity)
        if hasattr(halo, "set_fill"):
            halo.set_fill(opacity=0)
        layers.add(halo)
    return VGroup(layers, mobject)


def panel(width: float, height: float, color: str = cfg.CYAN, opacity: float = 0.32) -> RoundedRectangle:
    """Subtle framed panel for repeated items."""

    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=2,
        stroke_opacity=0.7,
        fill_color=cfg.PANEL,
        fill_opacity=opacity,
    )


def number_dot_grid(count: int, cols: int = 3, color: str = cfg.CYAN, radius: float = 0.075) -> VGroup:
    """Create a compact countable dot group."""

    dots = VGroup()
    for i in range(count):
        row = i // cols
        col = i % cols
        dots.add(Dot(radius=radius, color=color).move_to([col * 0.34, -row * 0.34, 0]))
    dots.center()
    return dots


def regular_polygon(n: int, radius: float = 1.5, color: str = cfg.CYAN) -> RegularPolygon:
    """Consistent regular polygon style."""

    poly = RegularPolygon(n=n, radius=radius, color=color, stroke_width=5)
    poly.set_fill(color, opacity=0.12)
    return poly


def polygon_vertex_lines(poly: RegularPolygon, color: str = cfg.GRAY) -> VGroup:
    """Lines from polygon center to vertices."""

    center = poly.get_center()
    lines = VGroup()
    for vertex in poly.get_vertices():
        lines.add(Line(center, vertex, color=color, stroke_width=2, stroke_opacity=0.55))
    return lines


def angle_arc_at(point, start_angle: float, angle: float, radius: float = 0.42, color: str = cfg.GOLD) -> Arc:
    """Create an angle arc around a point."""

    return Arc(radius=radius, start_angle=start_angle, angle=angle, color=color, stroke_width=6).move_arc_center_to(point)


def digit_wheel(digits: str, radius: float = 2.05, color: str = cfg.GOLD) -> VGroup:
    """Arrange digits around a circle."""

    wheel = VGroup(Circle(radius=radius, color=cfg.CYAN, stroke_width=3, stroke_opacity=0.75))
    for index, digit in enumerate(digits):
        angle = PI / 2 - TAU * index / len(digits)
        pos = np.array([radius * math.cos(angle), radius * math.sin(angle), 0])
        mob = Text(digit, font=cfg.FONT, font_size=54, color=color, weight=BOLD).move_to(pos)
        mob.set_stroke("#07131A", width=4, opacity=0.85, background=True)
        wheel.add(mob)
    return wheel


def curved_arrow_between(start, end, color: str = cfg.CYAN) -> CurvedArrow:
    """Curved arrow with consistent styling."""

    return CurvedArrow(start, end, angle=-TAU / 7, color=color, stroke_width=4)


def create_all(scene: Scene, group: Iterable[Mobject], run_time: float = 1.0) -> None:
    """Create a collection with a light lag."""

    scene.play(LaggedStart(*[Create(mob) for mob in group], lag_ratio=0.08), run_time=run_time)
