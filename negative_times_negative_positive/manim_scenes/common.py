"""Reusable Manim primitives for the video."""

from __future__ import annotations

from manim import *

import config as cfg


def cinematic_background() -> VGroup:
    """Create a dark scientific background with a subtle grid and stars."""
    base = Rectangle(width=16, height=9, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    grid = VGroup()
    for x in [i * 0.8 for i in range(-10, 11)]:
        grid.add(Line([x, -4.5, 0], [x, 4.5, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.18, stroke_width=1))
    for y in [i * 0.8 for i in range(-6, 7)]:
        grid.add(Line([-8, y, 0], [8, y, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.16, stroke_width=1))
    stars = VGroup(
        *[
            Dot(
                point=[-7.4 + (i * 1.37) % 14.8, -4.0 + (i * 2.11) % 8.0, 0],
                radius=0.008 + (i % 3) * 0.004,
                color=cfg.COLORS["muted"],
                fill_opacity=0.22,
            )
            for i in range(55)
        ]
    )
    return VGroup(base, grid, stars)


def create_glow_text(text: str, font_size: int = 42, color: str = cfg.ZERO, weight: str = BOLD) -> VGroup:
    """Create readable text with soft duplicate layers behind it."""
    main = Text(text, font_size=font_size, color=color, weight=weight)
    layers = VGroup()
    for index in range(cfg.VISUAL["glow_layers"], 0, -1):
        layer = main.copy()
        layer.set_color(color)
        layer.set_opacity(cfg.VISUAL["glow_opacity"] / index)
        layer.scale(1 + index * 0.018)
        layers.add(layer)
    return VGroup(layers, main)


def create_title(title: str, subtitle: str | None = None) -> VGroup:
    """Create a compact title stack."""
    title_mob = create_glow_text(title, cfg.FONT_SIZES["title"], cfg.GOLD)
    if subtitle is None:
        return title_mob
    subtitle_mob = Text(subtitle, font_size=cfg.FONT_SIZES["subtitle"], color=cfg.MUTED)
    subtitle_mob.next_to(title_mob, DOWN, buff=0.22)
    return VGroup(title_mob, subtitle_mob)


def create_number_line(start: int = -15, end: int = 15, unit_size: float = 0.38) -> NumberLine:
    """Create a color-ready Manim number line."""
    line = NumberLine(
        x_range=[start, end, 1],
        length=(end - start) * unit_size,
        include_numbers=True,
        include_tip=True,
        font_size=18,
        decimal_number_config={"num_decimal_places": 0},
    )
    line.set_color(cfg.MUTED)
    return line


def create_particle(color: str = cfg.GOLD) -> VGroup:
    """Create a glowing particle."""
    dot = Dot(radius=cfg.VISUAL["particle_radius"], color=color)
    glow = VGroup(
        *[
            Circle(radius=cfg.VISUAL["particle_radius"] * (2 + i), stroke_color=color, stroke_opacity=0.16 / (i + 1), stroke_width=2)
            for i in range(4)
        ]
    )
    return VGroup(glow, dot)


def create_vector_arrow(start=LEFT, end=RIGHT, color: str = cfg.POSITIVE, label: str | None = None) -> VGroup:
    """Create a thick arrow with an optional label."""
    arrow = Arrow(start, end, buff=0, stroke_width=cfg.VISUAL["arrow_stroke"], color=color, max_tip_length_to_length_ratio=0.18)
    glow = arrow.copy().set_stroke(color, width=16, opacity=0.16)
    group = VGroup(glow, arrow)
    if label:
        text = MathTex(label, font_size=cfg.FONT_SIZES["label"], color=color)
        text.next_to(arrow, UP, buff=0.22)
        group.add(text)
    return group


def create_equation_box(equation: str, color: str = cfg.ZERO, font_size: int = 44) -> VGroup:
    """Create a framed equation."""
    eq = MathTex(equation, font_size=font_size, color=color)
    box = RoundedRectangle(
        corner_radius=cfg.VISUAL["corner_radius"],
        width=eq.width + 0.65,
        height=eq.height + 0.42,
        stroke_color=color,
        stroke_opacity=0.75,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.72,
    )
    glow = box.copy().set_stroke(color, width=8, opacity=0.12)
    return VGroup(glow, box, eq)


def create_balance_scale(left_label: str = "-15", right_label: str = "?") -> VGroup:
    """Create a conceptual balance scale."""
    beam = Line(LEFT * 2.5, RIGHT * 2.5, stroke_color=cfg.ZERO, stroke_width=5)
    pivot = Triangle(color=cfg.MUTED, fill_color=cfg.COLORS["line"], fill_opacity=0.8).scale(0.34).rotate(PI)
    pivot.next_to(beam, DOWN, buff=0)
    left_pan = VGroup(Line(LEFT * 2.0, LEFT * 2.0 + DOWN * 0.75, color=cfg.MUTED), Arc(radius=0.55, angle=PI, color=cfg.MUTED))
    left_pan[1].move_to(LEFT * 2.0 + DOWN * 0.85).rotate(PI)
    right_pan = left_pan.copy().shift(RIGHT * 4.0)
    left_text = MathTex(left_label, font_size=30, color=cfg.NEGATIVE).move_to(left_pan[1].get_center() + DOWN * 0.05)
    right_text = MathTex(right_label, font_size=30, color=cfg.GOLD).move_to(right_pan[1].get_center() + DOWN * 0.05)
    return VGroup(beam, pivot, left_pan, right_pan, left_text, right_text)


def create_math_machine(label: str = "distribute") -> VGroup:
    """Create a stylized algebra machine."""
    body = RoundedRectangle(corner_radius=0.18, width=3.1, height=1.55, fill_color="#172033", fill_opacity=0.9, stroke_color=cfg.POSITIVE)
    inner = RoundedRectangle(corner_radius=0.12, width=2.52, height=0.72, stroke_color=cfg.GOLD, stroke_opacity=0.65)
    word = Text(label, font_size=24, color=cfg.ZERO)
    gear_a = Circle(radius=0.18, color=cfg.GOLD).shift(LEFT * 0.82 + DOWN * 0.43)
    gear_b = Circle(radius=0.14, color=cfg.POSITIVE).shift(LEFT * 0.45 + DOWN * 0.43)
    return VGroup(body, inner, word, gear_a, gear_b)


def pulse_mobject(mobject: Mobject, color: str = cfg.GOLD) -> Animation:
    """A short visual emphasis animation."""
    return Indicate(mobject, color=color, scale_factor=1.05)


def flash_color(mobject: Mobject, color: str = cfg.GOLD) -> Animation:
    """Flash an object in a given color."""
    return Flash(mobject, color=color, flash_radius=max(mobject.width, mobject.height) * 0.75 + 0.35)


def smooth_transform_equation(scene: Scene, old: Mobject, new: Mobject, run_time: float = 1.1) -> None:
    """Use matching-tex transformation when possible."""
    try:
        paced_play(scene, TransformMatchingTex(old, new), run_time=run_time)
    except Exception:
        paced_play(scene, ReplacementTransform(old, new), run_time=run_time)


def scene_transition(scene: Scene, keep: list[Mobject] | None = None, run_time: float = 0.55) -> None:
    """Fade out scene objects, optionally leaving selected objects."""
    keep = keep or []
    mobs = [mob for mob in scene.mobjects if mob not in keep]
    if mobs:
        paced_play(scene, FadeOut(*mobs), run_time=run_time)
    narration_wait(scene, 0.12)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """Play animations with a project-wide narration pacing scale."""
    scale = cfg.TIMING["pace_scale"]
    kwargs["run_time"] = kwargs.get("run_time", 1.0) * scale
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, duration: float = 1.0) -> None:
    """Wait with the same project-wide pacing scale."""
    scene.wait(duration * cfg.TIMING["pace_scale"])


def colorize_tex(tex: MathTex, negative_parts: tuple[str, ...] = ("-",), positive_parts: tuple[str, ...] = ("+",)) -> MathTex:
    """Apply consistent sign colors to a MathTex object."""
    for part in negative_parts:
        tex.set_color_by_tex(part, cfg.NEGATIVE)
    for part in positive_parts:
        tex.set_color_by_tex(part, cfg.GOLD)
    return tex
