"""Reusable Manim primitives for the population/sample chapter."""

from __future__ import annotations

import math
import random
from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg


PALETTE = [cfg.BLUE, cfg.GREEN, cfg.YELLOW, cfg.RED, cfg.PURPLE, cfg.ORANGE, cfg.TEAL]


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """Play animations using the project-wide pacing multiplier."""
    kwargs["run_time"] = kwargs.get("run_time", 1.0) * cfg.TIMING["pace_scale"]
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, duration: float = 1.0) -> None:
    """Wait using the project-wide pacing multiplier."""
    scene.wait(duration * cfg.TIMING["pace_scale"])


def cinematic_background(show_bubbles: bool = False) -> VGroup:
    """Create a dark scientific background with a subtle grid."""
    base = Rectangle(width=16, height=9, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    grid = VGroup()
    for x in [i * 0.8 for i in range(-10, 11)]:
        grid.add(Line([x, -4.5, 0], [x, 4.5, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.13, stroke_width=1))
    for y in [i * 0.8 for i in range(-6, 7)]:
        grid.add(Line([-8, y, 0], [8, y, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.12, stroke_width=1))
    specks = VGroup(
        *[
            Dot(
                [-7.6 + (i * 1.47) % 15.2, -4.2 + (i * 2.09) % 8.4, 0],
                radius=0.006 + (i % 4) * 0.003,
                color=cfg.MUTED,
                fill_opacity=0.22,
            )
            for i in range(70)
        ]
    )
    group = VGroup(base, grid, specks)
    if show_bubbles:
        bubbles = VGroup()
        for index in range(18):
            x = -7.2 + (index * 1.83) % 14.4
            y = -4.0 + (index * 2.37) % 8.0
            bubble = Circle(
                radius=0.08 + (index % 4) * 0.035,
                stroke_color=cfg.BLUE if index % 2 else cfg.YELLOW,
                stroke_width=1.5,
                stroke_opacity=0.25,
                fill_opacity=0,
            ).move_to([x, y, 0])
            bubbles.add(bubble)
        group.add(bubbles)
    return group


def scene_title(title: str, subtitle: str | None = None) -> VGroup:
    """Create a compact title stack for scene headers."""
    main = Text(title, font_size=cfg.FONT_SIZES["title"], color=cfg.TEXT, weight=BOLD)
    main.set_stroke(width=0, opacity=0)
    underline = Line(LEFT, RIGHT, color=cfg.BLUE, stroke_width=4).set_width(min(main.width, 6.2))
    underline.next_to(main, DOWN, buff=0.12)
    group = VGroup(main, underline)
    if subtitle:
        sub = Text(subtitle, font_size=cfg.FONT_SIZES["subtitle"], color=cfg.MUTED)
        sub.next_to(underline, DOWN, buff=0.16)
        group.add(sub)
    return group


def labeled_box(label: str, width: float = 2.5, height: float = 1.25, color: str = cfg.BLUE, font_size: int = 24) -> VGroup:
    """Create a labeled rounded rectangle."""
    box = RoundedRectangle(
        corner_radius=cfg.VISUAL["corner_radius"],
        width=width,
        height=height,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.85,
        stroke_color=color,
        stroke_width=2.5,
    )
    text = Text(label, font_size=font_size, color=cfg.TEXT, weight=BOLD)
    if text.width > width - 0.25:
        text.scale_to_fit_width(width - 0.25)
    return VGroup(box, text)


def equation_box(equation: str, color: str = cfg.YELLOW, font_size: int = 42) -> VGroup:
    """Create a framed MathTex equation."""
    tex = MathTex(equation, font_size=font_size, color=cfg.TEXT)
    frame = RoundedRectangle(
        corner_radius=cfg.VISUAL["corner_radius"],
        width=tex.width + 0.7,
        height=tex.height + 0.38,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.82,
        stroke_color=color,
        stroke_width=2.5,
    )
    return VGroup(frame, tex)


def info_card(
    title: str,
    lines: Sequence[str],
    width: float = 3.15,
    color: str = cfg.BLUE,
    title_size: int = 20,
    line_size: int = 15,
) -> VGroup:
    """Create a compact explanatory card with a title and short lines."""
    title_mob = Text(title, font_size=title_size, color=color, weight=BOLD)
    body = VGroup(*[Text(line, font_size=line_size, color=cfg.TEXT) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    if content.width > width - 0.35:
        content.scale_to_fit_width(width - 0.35)
    frame = RoundedRectangle(
        corner_radius=cfg.VISUAL["corner_radius"],
        width=width,
        height=content.height + 0.48,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.84,
        stroke_color=color,
        stroke_opacity=0.75,
        stroke_width=2,
    )
    content.move_to(frame.get_center())
    return VGroup(frame, content)


def scene_transition(scene: Scene, keep: Sequence[Mobject] | None = None, run_time: float = 0.55) -> None:
    """Fade out the scene, optionally keeping specified mobjects."""
    keep = list(keep or [])
    mobs = [mob for mob in scene.mobjects if mob not in keep]
    if mobs:
        paced_play(scene, FadeOut(*mobs), run_time=run_time)
    narration_wait(scene, 0.12)


def dot_cloud(
    count: int = 120,
    width: float = 6.0,
    height: float = 3.6,
    center: Sequence[float] = ORIGIN,
    colors: Sequence[str] = tuple(PALETTE[:4]),
    seed: int = 1,
    radius: float | None = None,
    opacity: float = 0.86,
    clusters: Sequence[Sequence[float]] | None = None,
) -> VGroup:
    """Create a deterministic colored cloud of dots."""
    rng = random.Random(seed)
    radius = radius if radius is not None else cfg.VISUAL["dot_radius"]
    center_vec = np.array(center, dtype=float)
    dots = VGroup()
    cluster_points = [np.array(point, dtype=float) for point in clusters] if clusters else []
    for index in range(count):
        if cluster_points:
            cluster = cluster_points[index % len(cluster_points)]
            x = rng.gauss(cluster[0], width / 12)
            y = rng.gauss(cluster[1], height / 10)
            pos = center_vec + np.array([x, y, 0])
        else:
            pos = center_vec + np.array([rng.uniform(-width / 2, width / 2), rng.uniform(-height / 2, height / 2), 0])
        dot = Dot(pos, radius=radius, color=colors[index % len(colors)], fill_opacity=opacity)
        dots.add(dot)
    return dots


def sample_frame(width: float = 2.0, height: float = 1.3, color: str = cfg.YELLOW) -> Rectangle:
    """Create a thin selection frame."""
    return Rectangle(width=width, height=height, stroke_color=color, stroke_width=3, fill_opacity=0)


def dataset_table(rows: int = 4, cols: int = 6, cell: float = 0.28, colors: Sequence[str] = tuple(PALETTE[:4])) -> VGroup:
    """Create a small table-like grid filled with colored records."""
    cells = VGroup()
    for row in range(rows):
        for col in range(cols):
            rect = Rectangle(width=cell, height=cell, stroke_color=cfg.COLORS["line"], stroke_width=1)
            rect.set_fill(colors[(row * cols + col) % len(colors)], opacity=0.5)
            rect.move_to([(col - (cols - 1) / 2) * cell, ((rows - 1) / 2 - row) * cell, 0])
            cells.add(rect)
    frame = RoundedRectangle(corner_radius=0.08, width=cols * cell + 0.24, height=rows * cell + 0.32, stroke_color=cfg.BLUE)
    return VGroup(frame, cells)


def arrow_between(start: Mobject | Sequence[float], end: Mobject | Sequence[float], color: str = cfg.BLUE, label: str | None = None) -> VGroup:
    """Create a thick arrow between two mobjects or points."""
    start_point = start.get_center() if isinstance(start, Mobject) else np.array(start, dtype=float)
    end_point = end.get_center() if isinstance(end, Mobject) else np.array(end, dtype=float)
    arrow = Arrow(start_point, end_point, buff=0.25, stroke_width=cfg.VISUAL["arrow_stroke"], color=color, max_tip_length_to_length_ratio=0.18)
    group = VGroup(arrow)
    if label:
        text = Text(label, font_size=cfg.FONT_SIZES["small"], color=color, weight=BOLD)
        text.next_to(arrow, UP, buff=0.12)
        group.add(text)
    return group


def simple_model(label: str = "Model", color: str = cfg.PURPLE) -> VGroup:
    """Create a small neural-network style model icon."""
    nodes = VGroup()
    layers = [3, 4, 2]
    x_positions = [-0.72, 0, 0.72]
    for layer_index, size in enumerate(layers):
        for node_index in range(size):
            y = (node_index - (size - 1) / 2) * 0.34
            nodes.add(Circle(radius=0.055, stroke_color=color, fill_color=color, fill_opacity=0.8).move_to([x_positions[layer_index], y, 0]))
    lines = VGroup()
    layer_nodes = [nodes[:3], nodes[3:7], nodes[7:9]]
    for left_layer, right_layer in zip(layer_nodes, layer_nodes[1:]):
        for left in left_layer:
            for right in right_layer:
                lines.add(Line(left.get_center(), right.get_center(), stroke_color=color, stroke_opacity=0.28, stroke_width=1.2))
    frame = RoundedRectangle(corner_radius=0.12, width=2.2, height=1.35, stroke_color=color, fill_color=cfg.COLORS["panel"], fill_opacity=0.84)
    text = Text(label, font_size=cfg.FONT_SIZES["small"], color=cfg.TEXT, weight=BOLD).next_to(frame, DOWN, buff=0.12)
    return VGroup(frame, lines, nodes, text)


def icon_tile(label: str, symbol: str, color: str, width: float = 1.55) -> VGroup:
    """Create a symbolic domain tile using simple text glyphs."""
    box = RoundedRectangle(corner_radius=0.1, width=width, height=0.85, fill_color=cfg.COLORS["panel_alt"], fill_opacity=0.85, stroke_color=color)
    sym = Text(symbol, font_size=25, color=color, weight=BOLD).shift(UP * 0.12)
    lab = Text(label, font_size=13, color=cfg.TEXT).next_to(sym, DOWN, buff=0.04)
    return VGroup(box, sym, lab)


def bell_curve(color: str = cfg.BLUE, shift_x: float = 0.0, stretch: float = 1.0, skew: float = 0.0) -> VGroup:
    """Create axes and a stylized probability curve."""
    axes = Axes(
        x_range=[-3, 3, 1],
        y_range=[0, 1.1, 0.5],
        x_length=3.0,
        y_length=1.55,
        tips=False,
        axis_config={"stroke_color": cfg.MUTED, "stroke_opacity": 0.55, "stroke_width": 2},
    )

    def fn(x: float) -> float:
        base = math.exp(-((x - shift_x) ** 2) / (2 * stretch**2))
        return base * (1 + skew * x / 4)

    curve = axes.plot(fn, color=color, stroke_width=4)
    return VGroup(axes, curve)


def road_scene(weather: str = "sun", color: str = cfg.BLUE) -> VGroup:
    """Create a simple road condition thumbnail from geometry only."""
    sky = Rectangle(width=2.35, height=1.42, fill_color="#1E293B", fill_opacity=1, stroke_color=color, stroke_width=2)
    road = Polygon([-1.05, -0.7, 0], [1.05, -0.7, 0], [0.36, 0.0, 0], [-0.36, 0.0, 0], fill_color="#202938", fill_opacity=1, stroke_width=0)
    stripe = DashedLine([0, -0.62, 0], [0, -0.04, 0], dash_length=0.08, color=cfg.YELLOW, stroke_width=2)
    horizon = Line([-1.08, 0.0, 0], [1.08, 0.0, 0], stroke_color=cfg.MUTED, stroke_opacity=0.45)
    group = VGroup(sky, road, stripe, horizon)
    if weather == "sun":
        group.add(Circle(radius=0.14, fill_color=cfg.YELLOW, fill_opacity=1, stroke_width=0).move_to([-0.72, 0.43, 0]))
    elif weather == "rain":
        group.add(*[Line([x, 0.48, 0], [x - 0.11, 0.22, 0], color=cfg.BLUE, stroke_width=2) for x in [-0.65, -0.25, 0.18, 0.58]])
    elif weather == "fog":
        group.add(*[Line([-0.82, y, 0], [0.86, y, 0], color=cfg.MUTED, stroke_opacity=0.45, stroke_width=4) for y in [0.18, 0.34, 0.5]])
    elif weather == "night":
        group.add(Circle(radius=0.11, fill_color=cfg.TEXT, fill_opacity=0.85, stroke_width=0).move_to([0.72, 0.46, 0]))
    elif weather == "snow":
        group.add(*[Text("*", font_size=17, color=cfg.TEXT).move_to([x, y, 0]) for x, y in [(-0.7, 0.44), (-0.22, 0.28), (0.28, 0.52), (0.72, 0.22)]])
    elif weather == "glare":
        group.add(Polygon([-1.1, 0.55, 0], [1.1, 0.15, 0], [1.1, 0.52, 0], [-1.1, 0.72, 0], fill_color=cfg.YELLOW, fill_opacity=0.28, stroke_width=0))
    return group


def warning_label(text: str = "All must represent the future use case") -> VGroup:
    """Create a warning badge."""
    tri = Triangle(color=cfg.WARNING, fill_color=cfg.WARNING, fill_opacity=0.2).scale(0.18).rotate(PI)
    bang = Text("!", font_size=22, color=cfg.WARNING, weight=BOLD).move_to(tri.get_center() + DOWN * 0.01)
    label = Text(text, font_size=cfg.FONT_SIZES["small"], color=cfg.WARNING, weight=BOLD).next_to(tri, RIGHT, buff=0.12)
    return VGroup(tri, bang, label)
