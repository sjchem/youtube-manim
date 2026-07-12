"""Reusable Manim primitives for the probability-basics chapter."""

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
    """Create a small continuity cue, not a scene-opening title card."""
    cue_text = title if subtitle is None else f"{title} - {subtitle}"
    cue = Text(cue_text, font_size=23, color=cfg.MUTED, weight=BOLD)
    cue.set_stroke("#02111D", width=4, opacity=0.82, background=True)
    if cue.width > cfg.SAFE_FRAME_WIDTH - 1.2:
        cue.scale_to_fit_width(cfg.SAFE_FRAME_WIDTH - 1.2)
    accent = Line(LEFT * 0.48, RIGHT * 0.48, color=cfg.GOLD, stroke_width=3)
    accent.next_to(cue, DOWN, buff=0.08)
    return VGroup(cue, accent)


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


def probability_bar(
    probability: float,
    label: str,
    color: str = cfg.CYAN,
    width: float = 6.0,
    height: float = 0.55,
) -> VGroup:
    """Create a horizontal 0-to-1 probability meter with a filled portion."""
    probability = max(0.0, min(1.0, probability))
    track = RoundedRectangle(
        corner_radius=height / 2,
        width=width,
        height=height,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.9,
        stroke_color=cfg.MUTED,
        stroke_width=1.6,
    )
    fill_width = max(width * probability, height)
    fill = RoundedRectangle(
        corner_radius=height / 2,
        width=fill_width,
        height=height,
        fill_color=color,
        fill_opacity=0.92,
        stroke_width=0,
    ).align_to(track, LEFT)
    fill.move_to(track.get_left() + RIGHT * fill_width / 2)
    zero = Text("0", font_size=20, color=cfg.MUTED).next_to(track, LEFT, buff=0.16)
    one = Text("1", font_size=20, color=cfg.MUTED).next_to(track, RIGHT, buff=0.16)
    value_label = Text(f"{probability:.2f}", font_size=22, color=cfg.WHITE, weight=BOLD)
    value_label.next_to(track, UP, buff=0.12)
    name_label = Text(label, font_size=22, color=color, weight=BOLD).next_to(track, DOWN, buff=0.14)
    return VGroup(track, fill, zero, one, value_label, name_label)


def probability_bar_fill_only(bar: VGroup) -> RoundedRectangle:
    """Return the fill rectangle mobject from a probability_bar group."""
    return bar[1]


def coin_icon(face: str = "H", color: str = cfg.GOLD, radius: float = 0.42) -> VGroup:
    """Create a simple coin token with a face label."""
    disc = Circle(radius=radius, fill_color=color, fill_opacity=0.92, stroke_color=cfg.WHITE, stroke_width=2.4)
    letter = Text(face, font_size=26, color=cfg.BG, weight=BOLD).move_to(disc)
    return VGroup(disc, letter)


def envelope_icon(color: str = cfg.CYAN, width: float = 1.1, height: float = 0.72) -> VGroup:
    """Create a simple email envelope icon."""
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height, fill_color=cfg.COLORS["panel"], fill_opacity=0.95, stroke_color=color, stroke_width=2.6)
    flap = Polygon(
        body.get_corner(UL), body.get_center() + UP * 0.02, body.get_corner(UR),
        color=color, stroke_width=2.2, fill_opacity=0,
    )
    return VGroup(body, flap)


def venn_two_circles(
    label_a: str,
    label_b: str,
    color_a: str = cfg.BLUE,
    color_b: str = cfg.GOLD,
    radius: float = 1.5,
    separation: float = 1.7,
) -> VGroup:
    """Create a two-circle Venn diagram with labels above each circle."""
    circle_a = Circle(radius=radius, color=color_a, fill_color=color_a, fill_opacity=0.28, stroke_width=3).shift(LEFT * separation / 2)
    circle_b = Circle(radius=radius, color=color_b, fill_color=color_b, fill_opacity=0.28, stroke_width=3).shift(RIGHT * separation / 2)
    label_a_mob = Text(label_a, font_size=24, color=color_a, weight=BOLD).next_to(circle_a, UP, buff=0.18).shift(LEFT * 0.3)
    label_b_mob = Text(label_b, font_size=24, color=color_b, weight=BOLD).next_to(circle_b, UP, buff=0.18).shift(RIGHT * 0.3)
    return VGroup(circle_a, circle_b, label_a_mob, label_b_mob)


def joint_probability_grid(
    row_labels: Sequence[str],
    col_labels: Sequence[str],
    values: Sequence[Sequence[float]],
    cell_size: float = 1.15,
) -> VGroup:
    """Create a small labeled grid of joint-probability cells."""
    n_rows, n_cols = len(row_labels), len(col_labels)
    grid = VGroup()
    cells = VGroup()
    for r in range(n_rows):
        for c in range(n_cols):
            value = values[r][c]
            intensity = min(1.0, value / (max(max(row) for row in values) + 1e-9))
            cell = Square(side_length=cell_size, fill_color=cfg.CYAN, fill_opacity=0.18 + 0.55 * intensity, stroke_color=cfg.MUTED, stroke_width=1.4)
            cell.move_to(RIGHT * c * cell_size + DOWN * r * cell_size)
            text = Text(f"{value:.2f}", font_size=20, color=cfg.WHITE, weight=BOLD).move_to(cell)
            cells.add(VGroup(cell, text))
    cells.move_to(ORIGIN)
    col_headers = VGroup(*[
        Text(label, font_size=20, color=cfg.GOLD, weight=BOLD) for label in col_labels
    ])
    row_headers = VGroup(*[
        Text(label, font_size=20, color=cfg.BLUE, weight=BOLD) for label in row_labels
    ])
    for c, header in enumerate(col_headers):
        header.next_to(cells[c], UP, buff=0.18)
    for r, header in enumerate(row_headers):
        header.next_to(cells[r * n_cols], LEFT, buff=0.22)
    grid.add(cells, col_headers, row_headers)
    return grid


def bayes_flow(prior: str, evidence: str, posterior: str) -> VGroup:
    """Create a three-stage prior -> evidence -> posterior flow diagram."""
    prior_card = stat_card("PRIOR BELIEF", prior, cfg.MUTED, width=2.9)
    evidence_card = stat_card("NEW EVIDENCE", evidence, cfg.GOLD, width=2.9)
    posterior_card = stat_card("UPDATED BELIEF", posterior, cfg.GREEN, width=2.9)
    row = VGroup(prior_card, evidence_card, posterior_card).arrange(RIGHT, buff=1.0)
    arrow1 = Arrow(prior_card.get_right(), evidence_card.get_left(), color=cfg.CYAN, buff=0.12, stroke_width=4)
    arrow2 = Arrow(evidence_card.get_right(), posterior_card.get_left(), color=cfg.CYAN, buff=0.12, stroke_width=4)
    return VGroup(row, arrow1, arrow2)


def distribution_bars(
    labels: Sequence[str],
    values: Sequence[float],
    colors: Sequence[str] | None = None,
    max_height: float = 3.2,
    bar_width: float = 0.85,
    gap: float = 0.45,
) -> VGroup:
    """Create a simple vertical bar chart for a discrete distribution."""
    colors = list(colors or PALETTE)
    bars = VGroup()
    labels_mobs = VGroup()
    values_mobs = VGroup()
    x = 0.0
    for index, (label, value) in enumerate(zip(labels, values)):
        height = max(0.18, value * max_height)
        bar = Rectangle(width=bar_width, height=height, fill_color=colors[index % len(colors)], fill_opacity=0.9, stroke_width=0)
        bar.move_to(RIGHT * x + UP * height / 2)
        text = Text(label, font_size=20, color=cfg.WHITE, weight=BOLD).next_to(bar, DOWN, buff=0.14)
        value_text = Text(f"{value:.0%}", font_size=20, color=colors[index % len(colors)], weight=BOLD).next_to(bar, UP, buff=0.1)
        bars.add(bar)
        labels_mobs.add(text)
        values_mobs.add(value_text)
        x += bar_width + gap
    group = VGroup(bars, labels_mobs, values_mobs)
    group.move_to(ORIGIN)
    return group


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
