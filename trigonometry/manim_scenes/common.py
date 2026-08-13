"""Shared visual language and animated constructions."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg
from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles


def begin_scene(scene: Scene, scene_key: str) -> float:
    """Apply the theme and activate this chapter's narration pacing."""
    apply_oceanic_next_theme(scene)
    scene.camera.background_color = cfg.BG
    scene._project_scene_key = scene_key
    scene._project_pace_scale = cfg.SCENE_PACE[scene_key]
    return float(scene.time)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    pace = float(getattr(scene, "_project_pace_scale", cfg.TIMING["pace_scale"]))
    kwargs["run_time"] = kwargs.get("run_time", 1.0) * pace
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Keep the current visual gently alive while narration continues."""
    pace = float(getattr(scene, "_project_pace_scale", cfg.TIMING["pace_scale"]))
    duration = seconds * pace
    focus = None
    for candidate in reversed(scene.mobjects):
        if getattr(candidate, "_is_project_background", False):
            continue
        if candidate.width < 0.2 or candidate.height < 0.08:
            continue
        if candidate.get_family_updaters():
            continue
        focus = candidate
        break
    if focus is None or duration < 0.35:
        scene.wait(duration)
        return
    scene.play(
        focus.animate.scale(1.012),
        run_time=duration,
        rate_func=there_and_back,
    )


def end_scene(
    scene: Scene,
    started_at: float,
    target_seconds: float,
    *,
    fade_background: bool = False,
) -> None:
    """Fade chapter content while preserving the film's continuous world."""
    transition = cfg.TIMING["transition"]
    elapsed = float(scene.time) - started_at
    remaining = target_seconds - elapsed - transition
    if remaining > 1.0:
        key = getattr(scene, "_project_scene_key", "unknown")
        raise RuntimeError(
            f"Scene {key} has {remaining:.2f}s of static end padding. "
            "Add authored motion or update SCENE_PACE."
        )
    if remaining < -0.1:
        key = getattr(scene, "_project_scene_key", "unknown")
        raise RuntimeError(
            f"Scene {key} overruns its narration target by {-remaining:.2f}s. "
            "Reduce authored timing or update SCENE_PACE."
        )
    if remaining > 1e-6:
        scene.wait(remaining)
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
        bubbles = oceanic_bubbles()
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


def add_cinematic_background(scene: Scene, show_bubbles: bool = True) -> VGroup:
    """Reuse one living background when multiple chapters share a Scene."""
    for mob in scene.mobjects:
        if getattr(mob, "_is_project_background", False):
            return mob
    background = cinematic_background(show_bubbles)
    scene.add(background)
    return background


def outlined_text(text: str, font_size: int, color: str = cfg.WHITE, weight=SEMIBOLD) -> Text:
    result = Text(text, font_size=font_size, color=color, weight=weight)
    result.set_stroke(cfg.BG, width=4, opacity=0.95, background=True)
    return result


def section_tag(number: str, text: str, color: str = cfg.GOLD) -> VGroup:
    """Small connective label used instead of a full-screen chapter card."""
    number_text = outlined_text(number, cfg.FONT["tiny"], color, BOLD)
    label = outlined_text(text.upper(), cfg.FONT["tiny"], cfg.WHITE, BOLD)
    rule = Line(ORIGIN, RIGHT * 0.72, color=cfg.CYAN, stroke_width=4)
    tag = VGroup(number_text, rule, label).arrange(RIGHT, buff=0.16)
    tag.to_corner(UL, buff=0.26)
    return tag


def title_card(title: str, subtitle: str | None = None, color: str = cfg.GOLD) -> VGroup:
    heading = outlined_text(title, cfg.FONT["title"], color, BOLD)
    rule = Line(LEFT * min(heading.width * 0.48, 5.7), RIGHT * min(heading.width * 0.48, 5.7), color=cfg.CYAN, stroke_width=4)
    group = VGroup(heading, rule).arrange(DOWN, buff=0.2)
    if subtitle:
        sub = outlined_text(subtitle, cfg.FONT["body"], cfg.WHITE)
        if sub.width > cfg.SAFE_WIDTH - 0.5:
            sub.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
        group.add(sub)
        group.arrange(DOWN, buff=0.2)
    return group


def eq(latex: str, color: str = cfg.WHITE, font_size: int | None = None) -> MathTex:
    result = MathTex(latex, color=color, font_size=font_size or cfg.FONT["section"])
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


def ferris_wheel(center: Sequence[float], radius: float = 2.0, spokes: int = 12) -> VGroup:
    center_array = np.array(center, dtype=float)
    rim = Circle(radius=radius, color=cfg.CYAN, stroke_width=5).move_to(center_array)
    hub = glow_dot(center_array, cfg.WHITE, 0.07)
    spoke_group = VGroup()
    for theta in np.linspace(0, TAU, spokes, endpoint=False):
        endpoint = center_array + radius * np.array([np.cos(theta), np.sin(theta), 0])
        spoke_group.add(Line(center_array, endpoint, color=cfg.GRAY, stroke_width=2, stroke_opacity=0.65))
    supports = VGroup(
        Line(center_array, center_array + np.array([-1.3, -3.0, 0]), color=cfg.MUTED, stroke_width=6),
        Line(center_array, center_array + np.array([1.3, -3.0, 0]), color=cfg.MUTED, stroke_width=6),
        Line(center_array + np.array([-1.65, -3.0, 0]), center_array + np.array([1.65, -3.0, 0]), color=cfg.MUTED, stroke_width=6),
    )
    return VGroup(supports, spoke_group, rim, hub)


def coordinate_axes(x_length: float = 6.8, y_length: float = 4.0) -> Axes:
    return Axes(
        x_range=[0, TAU + 0.25, PI / 2],
        y_range=[-1.25, 1.25, 1],
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.4, "include_ticks": True},
    )


def quarter_turn_labels(axes: Axes) -> VGroup:
    labels = VGroup()
    for x, latex in ((0, "0"), (PI / 2, r"\frac{\pi}{2}"), (PI, r"\pi"), (3 * PI / 2, r"\frac{3\pi}{2}"), (TAU, r"2\pi")):
        item = eq(latex, cfg.MUTED, cfg.FONT["tiny"])
        item.next_to(axes.c2p(x, 0), DOWN, buff=0.14)
        labels.add(item)
    return labels


def speaker_icon(center: Sequence[float], scale: float = 1.0) -> VGroup:
    center_array = np.array(center, dtype=float)
    body = RoundedRectangle(width=1.25, height=2.5, corner_radius=0.14, color=cfg.MUTED, fill_color=cfg.PANEL, fill_opacity=0.9)
    cone = Polygon([-0.25, -0.58, 0], [0.45, -1.02, 0], [0.45, 1.02, 0], [-0.25, 0.58, 0], color=cfg.CYAN, fill_color=cfg.CYAN, fill_opacity=0.25)
    coil = Line([-0.42, -0.56, 0], [-0.42, 0.56, 0], color=cfg.GOLD, stroke_width=8)
    group = VGroup(body, cone, coil).scale(scale).move_to(center_array)
    return group


def color_formula_parts(formula: MathTex) -> MathTex:
    """Apply the film's semantic colors to common symbols when present."""
    formula.set_color_by_tex("sin", cfg.CYAN)
    formula.set_color_by_tex("cos", cfg.GREEN)
    formula.set_color_by_tex("tan", cfg.ORANGE)
    formula.set_color_by_tex("theta", cfg.GOLD)
    return formula
