"""Shared visual primitives for Statistics for ML — Part 1, Chapter 1."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from manim import *

import config as cfg
from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles


# ── Scene lifecycle ──────────────────────────────────────────────────────────

def begin_scene(scene: Scene) -> float:
    """Apply the Oceanic theme and return the current scene clock."""
    try:
        apply_oceanic_next_theme(scene)
    except Exception:
        scene.camera.background_color = cfg.BG
    return float(getattr(scene, "time", 0.0))


def narration_wait(scene: Scene, duration: float = 1.0) -> None:
    scene.wait(duration * cfg.TIMING["pace_scale"])


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    kwargs["run_time"] = kwargs.get("run_time", 1.0) * cfg.TIMING["pace_scale"]
    scene.play(*animations, **kwargs)


def scene_transition(scene: Scene, run_time: float = 0.45) -> None:
    mobs = list(scene.mobjects)
    if mobs:
        scene.play(FadeOut(*mobs), run_time=run_time * cfg.TIMING["pace_scale"])
        scene.remove(*mobs)
    scene.wait(0.08)


def end_scene(
    scene: Scene,
    start_time: float,
    target_seconds: float,
    transition_run_time: float = 0.45,
) -> None:
    """Pad the scene to the target duration, then fade out."""
    elapsed = float(getattr(scene, "time", 0.0)) - start_time
    transition_cost = (transition_run_time + 0.08) * cfg.TIMING["pace_scale"]
    remaining = target_seconds - elapsed - transition_cost
    if remaining > 0:
        scene.wait(remaining)
    scene_transition(scene, run_time=transition_run_time)


# ── Background ───────────────────────────────────────────────────────────────

def cinematic_background(show_bubbles: bool = True) -> VGroup:
    """Return a layered Oceanic background: fill + grid + bubbles."""
    base = Rectangle(
        width=16.6, height=9.4,
        fill_color=cfg.BG, fill_opacity=1, stroke_width=0,
    )
    grid = VGroup()
    for x in np.linspace(-8, 8, 17):
        grid.add(Line([x, -4.7, 0], [x, 4.7, 0],
                      stroke_color=cfg.COLORS["line"], stroke_opacity=0.16, stroke_width=0.7))
    for y in np.linspace(-4.5, 4.5, 10):
        grid.add(Line([-8.3, y, 0], [8.3, y, 0],
                      stroke_color=cfg.COLORS["line"], stroke_opacity=0.11, stroke_width=0.7))
    bubbles = oceanic_bubbles() if show_bubbles else VGroup()
    return VGroup(base, grid, bubbles)


# ── Text helpers ─────────────────────────────────────────────────────────────

def title_card(
    main: str,
    sub: str | None = None,
    color: str = cfg.WHITE,
    sub_color: str = cfg.CYAN,
) -> VGroup:
    t = Text(main, font_size=cfg.FONT["title"], color=color, weight=BOLD)
    t.set_stroke(cfg.BG, width=5, background=True)
    rule = Line(LEFT * min(t.width * 0.55, 5.8), RIGHT * min(t.width * 0.55, 5.8),
                color=sub_color, stroke_width=3.5)
    rule.next_to(t, DOWN, buff=0.18)
    group = VGroup(t, rule)
    if sub:
        s = Text(sub, font_size=cfg.FONT["body"], color=sub_color)
        s.next_to(rule, DOWN, buff=0.22)
        group.add(s)
    return group


def label(text: str, font_size: int | None = None, color: str = cfg.WHITE) -> Text:
    fs = font_size if font_size is not None else cfg.FONT["label"]
    t = Text(text, font_size=fs, color=color)
    t.set_stroke(cfg.BG, width=3, background=True)
    return t


def eq(latex: str, color: str = cfg.WHITE, font_size: int | None = None) -> MathTex:
    fs = font_size if font_size is not None else cfg.FONT["section"]
    m = MathTex(latex, color=color, font_size=fs)
    m.set_stroke(cfg.BG, width=3, background=True)
    return m


# ── Glow effects ─────────────────────────────────────────────────────────────

def glow_dot(
    point: Sequence[float],
    radius: float = 0.09,
    color: str = cfg.CYAN,
    glow_opacity: float = 0.22,
    layers: int = 3,
) -> VGroup:
    g = VGroup()
    for i in range(layers, 0, -1):
        c = Circle(radius=radius + i * 0.055, color=color,
                   stroke_width=0, fill_opacity=glow_opacity / i)
        c.move_to(point)
        g.add(c)
    core = Dot(point=point, radius=radius, color=color)
    g.add(core)
    return g


def glow_line(
    start: Sequence[float],
    end: Sequence[float],
    color: str = cfg.CYAN,
    stroke_width: float = 4.5,
    glow_width: float = 14.0,
    glow_opacity: float = 0.12,
) -> VGroup:
    shadow = Line(start, end, color=color,
                  stroke_width=glow_width, stroke_opacity=glow_opacity)
    core   = Line(start, end, color=color, stroke_width=stroke_width)
    return VGroup(shadow, core)


def glow_curve(vmob: VMobject, color: str = cfg.CYAN, glow_width: float = 16.0) -> VGroup:
    shadow = vmob.copy().set_stroke(color, width=glow_width, opacity=0.12)
    return VGroup(shadow, vmob)


def equation_card(latex: str, color: str = cfg.WHITE) -> VGroup:
    """Equation inside a softly lit panel box."""
    m = eq(latex, color=color, font_size=cfg.FONT["section"])
    box = RoundedRectangle(
        corner_radius=0.16, width=m.width + 1.0, height=m.height + 0.55,
        stroke_color=color, stroke_opacity=0.55,
        fill_color=cfg.COLORS["panel"], fill_opacity=0.80,
    )
    halo = box.copy().set_stroke(color, width=10, opacity=0.09)
    return VGroup(halo, box, m)


# ── Axes helpers ─────────────────────────────────────────────────────────────

def stat_axes(
    x_range: list[float],
    y_range: list[float],
    x_length: float = 7.5,
    y_length: float = 4.5,
    x_label: str = "",
    y_label: str = "",
) -> tuple[Axes, VGroup]:
    axes = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.2, "include_tip": False},
        tips=False,
    )
    labels = VGroup()
    if x_label:
        xl = label(x_label, font_size=cfg.FONT["small"], color=cfg.MUTED)
        xl.next_to(axes.x_axis.get_right(), DOWN, buff=0.20)
        labels.add(xl)
    if y_label:
        yl = label(y_label, font_size=cfg.FONT["small"], color=cfg.MUTED)
        yl.rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.28)
        labels.add(yl)
    return axes, labels


# ── Reusable decorations ─────────────────────────────────────────────────────

def series_badge() -> VGroup:
    """Compact corner badge showing series & chapter identity."""
    part = Text(cfg.SERIES_PART, font_size=cfg.FONT["tiny"], color=cfg.CYAN)
    ch   = Text(cfg.CHAPTER_NUMBER, font_size=cfg.FONT["tiny"], color=cfg.MUTED)
    grp  = VGroup(part, ch).arrange(RIGHT, buff=0.25)
    grp.to_corner(UL, buff=0.22)
    grp.set_stroke(cfg.BG, width=2, background=True)
    return grp


def bottom_caption(text: str, color: str = cfg.GOLD) -> Text:
    """A bold caption pinned to the bottom of the frame."""
    t = Text(text, font_size=cfg.FONT["body"], color=color, weight=BOLD)
    t.set_stroke(cfg.BG, width=5, background=True)
    if t.width > cfg.SAFE_WIDTH - 0.5:
        t.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    t.to_edge(DOWN, buff=0.32)
    return t
