"""Shared visual language and animated constructions for the calculus film."""

from __future__ import annotations

import warnings
from collections.abc import Callable, Sequence

import numpy as np
from manim import *

import config as cfg


def begin_scene(scene: Scene, scene_key: str) -> float:
    """Apply the theme and remember this chapter's start time."""
    cfg.apply_project_theme(scene, bubbles=False)
    scene._project_scene_key = scene_key
    return float(scene.time)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    kwargs["run_time"] = kwargs.get("run_time", 1.0)
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Keep the current visual gently alive while narration continues."""
    focus = None
    for candidate in reversed(scene.mobjects):
        if getattr(candidate, "_is_project_background", False):
            continue
        try:
            if candidate.width < 0.2 or candidate.height < 0.08:
                continue
            if candidate.get_family_updaters():
                continue
        except (IndexError, ValueError):
            # Some degenerate mobjects (e.g. a DashedVMobject with an empty
            # dash) cannot report their bounding box; skip them defensively.
            continue
        focus = candidate
        break
    if focus is None or seconds < 0.35:
        scene.wait(max(seconds, 0.0))
        return
    scene.play(
        focus.animate.scale(1.012),
        run_time=seconds,
        rate_func=there_and_back,
    )


def end_scene(
    scene: Scene,
    started_at: float,
    target_seconds: float,
    *,
    fade_background: bool = False,
) -> None:
    """Fade chapter content, padding or trimming gently to hit the narration target."""
    transition = cfg.TIMING["transition"]
    elapsed = float(scene.time) - started_at
    remaining = target_seconds - elapsed - transition
    key = getattr(scene, "_project_scene_key", "unknown")
    if 1.0 < remaining <= 3.0:
        narration_wait(scene, remaining)
    elif remaining > 3.0:
        # A large gap means the scene is under-authored relative to its target;
        # take one short breathing pause instead of one long dead hold, and let
        # the timing audit's PADDING status flag the mismatch for retuning.
        narration_wait(scene, 1.2)
    elif remaining < -0.1:
        warnings.warn(f"Scene {key} overruns its narration target by {-remaining:.2f}s.", stacklevel=2)
    visible = [
        mob
        for mob in scene.mobjects
        if fade_background or not getattr(mob, "_is_project_background", False)
    ]
    if visible:
        scene.play(FadeOut(*visible), run_time=transition)
        scene.remove(*visible)


def cinematic_background(show_bubbles: bool = True) -> VGroup:
    """Oceanic background with an extremely slow living bubble layer."""
    base = Rectangle(width=16.4, height=9.3, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    grid = VGroup()
    for x in np.linspace(-8, 8, 17):
        grid.add(Line([x, -4.65, 0], [x, 4.65, 0], color="#173653", stroke_width=0.65, stroke_opacity=0.16))
    for y in np.linspace(-4.5, 4.5, 10):
        grid.add(Line([-8.2, y, 0], [8.2, y, 0], color="#173653", stroke_width=0.65, stroke_opacity=0.11))
    layers = VGroup(base, grid)
    if show_bubbles:
        bubbles = oceanic_bubbles_layer()
        for index, bubble in enumerate(bubbles):
            speed = 0.018 + 0.003 * (index % 5)

            def drift(mob: Mobject, dt: float, velocity: float = speed) -> None:
                mob.shift(UP * velocity * dt)
                if mob.get_bottom()[1] > 4.65:
                    mob.shift(DOWN * 9.3)

            bubble.add_updater(drift)
        layers.add(bubbles)
    layers._is_project_background = True
    return layers


def oceanic_bubbles_layer() -> VGroup:
    from themes.oceanic_next import oceanic_bubbles

    return oceanic_bubbles()


def add_cinematic_background(scene: Scene, show_bubbles: bool = True) -> VGroup:
    """Reuse one living background when multiple chapters share a Scene."""
    for mob in scene.mobjects:
        if getattr(mob, "_is_project_background", False):
            return mob
    background = cinematic_background(show_bubbles)
    scene.add(background)
    return background


def outlined_text(text: str, font_size: int, color: str = cfg.WHITE, weight=BOLD) -> Text:
    result = Text(text, font_size=font_size, color=color, weight=weight)
    result.set_stroke(cfg.BG, width=4, opacity=0.95, background=True)
    return result


def title_card(title: str, subtitle: str | None = None, color: str = cfg.GOLD) -> VGroup:
    heading = outlined_text(title, cfg.FONT["title"], color, BOLD)
    if heading.width > cfg.SAFE_WIDTH:
        heading.scale_to_fit_width(cfg.SAFE_WIDTH)
    rule = Line(LEFT * min(heading.width * 0.48, 5.7), RIGHT * min(heading.width * 0.48, 5.7), color=cfg.CYAN, stroke_width=4)
    group = VGroup(heading, rule).arrange(DOWN, buff=0.2)
    if subtitle:
        sub = outlined_text(subtitle, cfg.FONT["body"], cfg.WHITE)
        if sub.width > cfg.SAFE_WIDTH - 0.5:
            sub.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
        group.add(sub)
        group.arrange(DOWN, buff=0.2)
    return group


def eq(
    latex: str,
    color: str = cfg.WHITE,
    font_size: int | None = None,
    *,
    substrings_to_isolate: Sequence[str] | None = None,
) -> MathTex:
    result = MathTex(
        latex,
        color=color,
        font_size=font_size or cfg.FONT["section"],
        substrings_to_isolate=list(substrings_to_isolate or ()),
    )
    result.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    return result


def equation_card(latex: str, color: str = cfg.WHITE, font_size: int | None = None) -> VGroup:
    formula = eq(latex, color, font_size)
    box = RoundedRectangle(
        width=formula.width + 0.8,
        height=formula.height + 0.48,
        corner_radius=0.16,
        stroke_color=color,
        stroke_opacity=0.55,
        fill_color=cfg.PANEL,
        fill_opacity=0.88,
    )
    halo = box.copy().set_stroke(color, width=12, opacity=0.07)
    return VGroup(halo, box, formula)


def bottom_caption(text: str, color: str = cfg.GOLD) -> Text:
    caption = outlined_text(text, cfg.FONT["body"], color, BOLD)
    if caption.width > cfg.SAFE_WIDTH - 0.5:
        caption.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(DOWN, buff=0.28)


def glow_dot(point: Sequence[float], color: str = cfg.GOLD, radius: float = 0.09) -> VGroup:
    layers = VGroup()
    for size, opacity in ((0.26, 0.05), (0.19, 0.09), (0.14, 0.15)):
        layers.add(Circle(radius=size, color=color, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(point))
    layers.add(Dot(point, radius=radius, color=color))
    return layers


def glow_line(start: Sequence[float], end: Sequence[float], color: str, width: float = 5) -> VGroup:
    return VGroup(
        Line(start, end, color=color, stroke_width=width * 3.2, stroke_opacity=0.1),
        Line(start, end, color=color, stroke_width=width),
    )


def glow_curve(curve: VMobject, color: str = cfg.CYAN) -> VGroup:
    return VGroup(curve.copy().set_stroke(color, width=18, opacity=0.1), curve)


def dashed_ring(center: Sequence[float], radius: float, color: str = cfg.GOLD, num_dashes: int = 14, stroke_width: float = 3) -> VGroup:
    """A dashed circular ring built from independent arcs.

    Avoids DashedVMobject, whose generated dashes can include a degenerate,
    zero-point sub-path that crashes real (non-audit) Manim rendering when
    that ring is later faded out as part of a larger group.
    """
    dash_angle = TAU / num_dashes * 0.6
    gap_angle = TAU / num_dashes - dash_angle
    ring = VGroup()
    for i in range(num_dashes):
        start = i * (dash_angle + gap_angle)
        ring.add(Arc(radius=radius, start_angle=start, angle=dash_angle, arc_center=np.array(center), color=color, stroke_width=stroke_width))
    return ring


def calc_axes(
    x_range: Sequence[float] = (-3, 3, 1),
    y_range: Sequence[float] = (-1, 5, 1),
    x_length: float = 7.0,
    y_length: float = 5.0,
) -> Axes:
    return Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.4, "include_ticks": True},
    )


def calc_axis_labels(axes: Axes, x_tex: str = "x", y_tex: str = "f(x)") -> VGroup:
    """Readable axis labels with consistent placement for phone screens."""
    x_label = eq(x_tex, cfg.MUTED, cfg.FONT["label"]).next_to(axes.x_axis.get_right(), UP, buff=0.1)
    y_label = eq(y_tex, cfg.MUTED, cfg.FONT["label"]).next_to(axes.y_axis.get_top(), RIGHT, buff=0.1)
    return VGroup(x_label, y_label)


def secant_line(
    axes: Axes,
    func: Callable[[float], float],
    x0: float,
    h: float,
    color: str = cfg.CYAN,
    extend: float = 0.6,
) -> VGroup:
    """A glowing secant line through (x0, f(x0)) and (x0+h, f(x0+h)), extended slightly."""
    x1, x2 = x0, x0 + h
    y1, y2 = func(x1), func(x2)
    direction = np.array([x2 - x1, y2 - y1, 0.0])
    norm = np.linalg.norm(direction)
    if norm < 1e-9:
        direction = np.array([1.0, 0.0, 0.0])
        norm = 1.0
    unit = direction / norm
    start = axes.c2p(x1, y1) - unit * extend
    end = axes.c2p(x2, y2) + unit * extend
    return glow_line(start, end, color, width=5)


def tangent_line(
    axes: Axes,
    func: Callable[[float], float],
    dfunc: Callable[[float], float],
    x0: float,
    color: str = cfg.GREEN,
    half_length: float = 1.6,
) -> VGroup:
    """A glowing tangent line at (x0, f(x0)) with the given analytic slope."""
    slope = dfunc(x0)
    y0 = func(x0)
    direction = np.array([1.0, slope, 0.0])
    direction = direction / np.linalg.norm(direction)
    p0 = axes.c2p(x0, y0)
    start = p0 - direction * half_length * axes.x_axis.get_unit_size()
    end = p0 + direction * half_length * axes.x_axis.get_unit_size()
    return glow_line(start, end, color, width=6)


def car_icon(color: str = cfg.CYAN, scale: float = 1.0) -> VGroup:
    """A simple stylized car, facing right."""
    body = RoundedRectangle(width=1.7, height=0.55, corner_radius=0.16, color=color, fill_color=color, fill_opacity=0.85, stroke_width=2)
    body.shift(UP * 0.28)
    cabin = RoundedRectangle(width=0.95, height=0.42, corner_radius=0.14, color=color, fill_color=cfg.PANEL_2, fill_opacity=0.9, stroke_width=2)
    cabin.shift(UP * 0.62)
    wheel_1 = Circle(radius=0.19, color=cfg.GRAY, fill_color="#05121F", fill_opacity=1, stroke_width=3).shift(LEFT * 0.55 + UP * 0.02)
    wheel_2 = Circle(radius=0.19, color=cfg.GRAY, fill_color="#05121F", fill_opacity=1, stroke_width=3).shift(RIGHT * 0.55 + UP * 0.02)
    headlight = Dot(radius=0.055, color=cfg.GOLD).move_to(body.get_right() + UP * 0.02)
    group = VGroup(body, cabin, wheel_1, wheel_2, headlight).scale(scale)
    return group


def speedometer_icon(color: str = cfg.CYAN, scale: float = 1.0) -> VGroup:
    dial = Arc(radius=0.75, start_angle=PI + PI / 6, angle=PI - PI / 3, color=color, stroke_width=6)
    ticks = VGroup()
    for angle in np.linspace(PI + PI / 6, 2 * PI - PI / 6, 5):
        inner = 0.6 * np.array([np.cos(angle), np.sin(angle), 0])
        outer = 0.75 * np.array([np.cos(angle), np.sin(angle), 0])
        ticks.add(Line(inner, outer, color=cfg.MUTED, stroke_width=3))
    needle = Line(ORIGIN, 0.62 * np.array([np.cos(PI + PI / 3), np.sin(PI + PI / 3), 0]), color=cfg.GOLD, stroke_width=6)
    hub = Dot(ORIGIN, radius=0.06, color=cfg.WHITE)
    return VGroup(dial, ticks, needle, hub).scale(scale)


def thermometer_icon(color: str = cfg.RED, scale: float = 1.0) -> VGroup:
    tube = RoundedRectangle(width=0.32, height=1.5, corner_radius=0.16, color=cfg.MUTED, fill_color=cfg.PANEL_2, fill_opacity=0.9, stroke_width=2.5)
    tube.shift(UP * 0.35)
    bulb = Circle(radius=0.26, color=cfg.MUTED, fill_color=cfg.PANEL_2, fill_opacity=0.9, stroke_width=2.5).shift(DOWN * 0.55)
    fill_tube = RoundedRectangle(width=0.14, height=1.05, corner_radius=0.07, color=color, fill_color=color, fill_opacity=1, stroke_width=0)
    fill_tube.move_to(tube.get_center() + DOWN * 0.05)
    fill_bulb = Circle(radius=0.17, color=color, fill_color=color, fill_opacity=1, stroke_width=0).move_to(bulb.get_center())
    return VGroup(tube, bulb, fill_tube, fill_bulb).scale(scale)


def population_icon(color: str = cfg.GREEN, scale: float = 1.0) -> VGroup:
    figures = VGroup()
    for i, height in enumerate((0.35, 0.55, 0.75, 0.95)):
        bar = RoundedRectangle(width=0.28, height=height, corner_radius=0.05, color=color, fill_color=color, fill_opacity=0.85, stroke_width=1.5)
        bar.move_to(RIGHT * 0.4 * i + UP * height / 2)
        figures.add(bar)
    baseline = Line(LEFT * 0.25, RIGHT * 1.55, color=cfg.MUTED, stroke_width=3)
    return VGroup(baseline, figures).scale(scale)


def color_formula_parts(formula: MathTex) -> MathTex:
    """Apply the film's semantic colors to common symbols when present."""
    formula.set_color_by_tex("lim", cfg.PURPLE)
    formula.set_color_by_tex("sin", cfg.CYAN)
    formula.set_color_by_tex("cos", cfg.GREEN)
    formula.set_color_by_tex("tan", cfg.ORANGE)
    return formula
