"""Reusable Manim primitives for the descriptive statistics chapter."""

from __future__ import annotations

import random
from dataclasses import dataclass
from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg


PALETTE = [cfg.BLUE, cfg.GREEN, cfg.GOLD, cfg.ORANGE, cfg.PURPLE, cfg.CYAN]


@dataclass(frozen=True)
class SceneClock:
    """Track one scene segment inside standalone and full-video renders."""

    key: str | None
    start_time: float


def current_scene_time(scene: Scene) -> float:
    """Return Manim's current timeline time across renderer versions."""
    renderer = getattr(scene, "renderer", None)
    renderer_time = getattr(renderer, "time", None)
    if renderer_time is not None:
        return float(renderer_time)
    return float(getattr(scene, "time", 0.0))


def begin_scene(scene: Scene, scene_key: str | None = None, include_bubbles: bool = True) -> SceneClock:
    """Apply the project theme and return a simple scene start marker."""
    cfg.apply_project_theme(scene)
    if include_bubbles:
        try:
            from themes.oceanic_next import oceanic_bubbles

            scene.add(oceanic_bubbles())
        except Exception:
            pass
    return SceneClock(scene_key, current_scene_time(scene))


def end_scene(scene: Scene, scene_start: SceneClock | None = None, hold: float = 1.0) -> None:
    """Hold the final composition until it matches the narration duration."""
    if scene_start is None or scene_start.key is None:
        narration_wait(scene, hold)
        return

    target = cfg.SCENE_DURATIONS.get(scene_start.key)
    elapsed = current_scene_time(scene) - scene_start.start_time
    wait_time = max(hold, (target or 0) - elapsed)
    scene.wait(wait_time)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """Play animations using the project-wide pacing multiplier."""
    kwargs["run_time"] = kwargs.get("run_time", 1.0) * cfg.TIMING["pace_scale"]
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, duration: float = 1.0) -> None:
    """Wait using the project-wide pacing multiplier."""
    scene.wait(duration * cfg.TIMING["pace_scale"])


def cinematic_background(show_grid: bool = True) -> VGroup:
    """Create a calm scientific Oceanic background."""
    base = Rectangle(width=16, height=9, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    glow = Circle(radius=4.6, fill_color=cfg.COLORS["background_2"], fill_opacity=0.42, stroke_width=0).shift(RIGHT * 4.2 + UP * 1.7)
    group = VGroup(base, glow)
    if show_grid:
        grid = VGroup()
        for x in np.arange(-8, 8.01, 0.8):
            grid.add(Line([x, -4.5, 0], [x, 4.5, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.14, stroke_width=1))
        for y in np.arange(-4.0, 4.01, 0.8):
            grid.add(Line([-8, y, 0], [8, y, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.12, stroke_width=1))
        group.add(grid)
    return group


def scene_title(title: str, subtitle: str | None = None) -> VGroup:
    """Create a readable mobile-first title stack."""
    main = Text(title, font_size=cfg.FONT_SIZES["title"], color=cfg.CYAN, weight=BOLD)
    main.set_stroke("#02111D", width=5, opacity=0.8, background=True)
    underline = Line(LEFT, RIGHT, color=cfg.GOLD, stroke_width=5).set_width(min(main.width, 7.4))
    underline.next_to(main, DOWN, buff=0.12)
    group = VGroup(main, underline)
    if subtitle:
        sub = Text(subtitle, font_size=cfg.FONT_SIZES["subtitle"], color=cfg.WHITE)
        sub.set_stroke("#02111D", width=4, opacity=0.75, background=True)
        sub.next_to(underline, DOWN, buff=0.16)
        group.add(sub)
    return group


def safe_caption(text: str, color: str = cfg.WHITE, font_size: int = 30) -> Text:
    """Create a large caption that fits the central safe frame."""
    caption = Text(text, font_size=font_size, color=color, weight=BOLD)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    if caption.width > cfg.SAFE_FRAME_WIDTH:
        caption.scale_to_fit_width(cfg.SAFE_FRAME_WIDTH)
    return caption


def equation_box(equation: str, color: str = cfg.GOLD, font_size: int = 46) -> VGroup:
    """Create a framed equation with consistent styling."""
    tex = MathTex(equation, font_size=font_size, color=cfg.WHITE)
    frame = RoundedRectangle(
        corner_radius=0.12,
        width=tex.width + 0.78,
        height=tex.height + 0.5,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.86,
        stroke_color=color,
        stroke_width=2.8,
    )
    return VGroup(frame, tex)


def label_pill(text: str, color: str = cfg.BLUE, font_size: int = 24) -> VGroup:
    """Create a compact label badge."""
    mob = Text(text, font_size=font_size, color=cfg.WHITE, weight=BOLD)
    if mob.width > 2.7:
        mob.scale_to_fit_width(2.7)
    frame = RoundedRectangle(
        corner_radius=0.12,
        width=mob.width + 0.38,
        height=mob.height + 0.22,
        fill_color=cfg.COLORS["panel_alt"],
        fill_opacity=0.9,
        stroke_color=color,
        stroke_width=2,
    )
    return VGroup(frame, mob)


def stat_card(title: str, value: str, color: str = cfg.BLUE, width: float = 2.5) -> VGroup:
    """Create a small statistic readout card."""
    title_mob = Text(title, font_size=22, color=color, weight=BOLD)
    value_mob = Text(value, font_size=34, color=cfg.WHITE, weight=BOLD)
    content = VGroup(title_mob, value_mob).arrange(DOWN, buff=0.1)
    frame = RoundedRectangle(
        corner_radius=0.12,
        width=max(width, content.width + 0.42),
        height=1.18,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.86,
        stroke_color=color,
        stroke_width=2,
    )
    content.move_to(frame)
    return VGroup(frame, content)


def deterministic_values() -> list[float]:
    """Return a stable teaching dataset with mild skew."""
    return [1.0, 1.4, 1.8, 2.0, 2.3, 2.7, 3.0, 3.2, 3.5, 4.1, 4.7, 6.2]


def number_line_with_dots(
    values: Sequence[float],
    x_min: float = 0,
    x_max: float = 8,
    length: float = 8.2,
    color: str = cfg.CYAN,
) -> tuple[NumberLine, VGroup]:
    """Create a number line and dots placed by data value."""
    line = NumberLine(
        x_range=[x_min, x_max, 1],
        length=length,
        include_numbers=True,
        font_size=22,
        color=cfg.MUTED,
        tick_size=0.08,
    )
    dots = VGroup()
    for index, value in enumerate(values):
        dot = Dot(line.n2p(value), radius=0.075, color=PALETTE[index % len(PALETTE)])
        dot.shift(UP * (0.16 + 0.08 * (index % 3)))
        dots.add(dot)
    return line, dots


def vertical_marker(line: NumberLine, value: float, label: str, color: str) -> VGroup:
    """Create a vertical marker on a number line."""
    base = line.n2p(value)
    marker = Line(base + DOWN * 0.34, base + UP * 0.78, color=color, stroke_width=5)
    lab = label_pill(label, color=color, font_size=22).next_to(marker, UP, buff=0.12)
    return VGroup(marker, lab)


def dot_cloud(
    count: int = 90,
    width: float = 6.6,
    height: float = 3.4,
    center: Sequence[float] = ORIGIN,
    seed: int = 3,
    colors: Sequence[str] = tuple(PALETTE),
) -> VGroup:
    """Create a stable cloud of records."""
    rng = random.Random(seed)
    center_vec = np.array(center, dtype=float)
    dots = VGroup()
    for index in range(count):
        x = rng.gauss(0, width / 5)
        y = rng.gauss(0, height / 5)
        x = max(-width / 2, min(width / 2, x))
        y = max(-height / 2, min(height / 2, y))
        dots.add(Dot(center_vec + np.array([x, y, 0]), radius=0.045, color=colors[index % len(colors)], fill_opacity=0.86))
    return dots


def sorted_stack(values: Sequence[float], line: NumberLine) -> VGroup:
    """Place data values as a sorted dot stack above a number line."""
    dots = VGroup()
    for index, value in enumerate(sorted(values)):
        dots.add(Dot(line.n2p(value) + UP * (0.26 + index * 0.045), radius=0.07, color=PALETTE[index % len(PALETTE)]))
    return dots


def scatter_points(
    slope: float = 0.72,
    noise: float = 0.55,
    count: int = 42,
    seed: int = 5,
    color: str = cfg.CYAN,
) -> tuple[Axes, VGroup]:
    """Create axes and a deterministic scatter cloud."""
    axes = Axes(
        x_range=[-3, 3, 1],
        y_range=[-3, 3, 1],
        x_length=4.7,
        y_length=3.4,
        tips=False,
        axis_config={"stroke_color": cfg.MUTED, "stroke_opacity": 0.7, "stroke_width": 2},
    )
    rng = random.Random(seed)
    dots = VGroup()
    for _ in range(count):
        x = rng.uniform(-2.65, 2.65)
        y = slope * x + rng.gauss(0, noise)
        y = max(-2.85, min(2.85, y))
        dots.add(Dot(axes.c2p(x, y), radius=0.045, color=color, fill_opacity=0.9))
    return axes, dots


def tiny_model(label: str = "ML model") -> VGroup:
    """Create a compact neural-network style icon from native Manim shapes."""
    nodes = VGroup()
    layers = [3, 4, 2]
    xs = [-0.72, 0, 0.72]
    for layer_index, size in enumerate(layers):
        for node_index in range(size):
            y = (node_index - (size - 1) / 2) * 0.32
            nodes.add(Circle(radius=0.055, stroke_color=cfg.PURPLE, fill_color=cfg.PURPLE, fill_opacity=0.85).move_to([xs[layer_index], y, 0]))
    lines = VGroup()
    layer_nodes = [nodes[:3], nodes[3:7], nodes[7:9]]
    for left_layer, right_layer in zip(layer_nodes, layer_nodes[1:]):
        for left in left_layer:
            for right in right_layer:
                lines.add(Line(left.get_center(), right.get_center(), color=cfg.PURPLE, stroke_opacity=0.26, stroke_width=1.1))
    frame = RoundedRectangle(corner_radius=0.12, width=2.15, height=1.34, fill_color=cfg.COLORS["panel"], fill_opacity=0.85, stroke_color=cfg.PURPLE)
    text = Text(label, font_size=21, color=cfg.WHITE, weight=BOLD).next_to(frame, DOWN, buff=0.12)
    return VGroup(frame, lines, nodes, text)
