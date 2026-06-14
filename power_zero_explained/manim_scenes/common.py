"""Reusable Manim objects for the zero-power explainer."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from manim import *

from config import (
    ACCENT_BLUE,
    ACCENT_CYAN,
    ACCENT_ORANGE,
    ACCENT_PURPLE,
    ACCENT_RED,
    ACCENT_TEAL,
    ACCENT_YELLOW,
    BACKGROUND_COLOR,
    EQUATION_FONT_SIZE,
    FONT,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    LABEL_FONT_SIZE,
    MUTED_TEXT,
    PANEL_COLOR,
    PANEL_STROKE,
    SMALL_FONT_SIZE,
    TEXT_COLOR,
    TITLE_FONT_SIZE,
    WORD_COLOR,
    WORD_FONT,
    apply_oceanic_next_theme,
)
from utils.math_utils import latex_fraction, power_sequence


@dataclass
class LadderVisual:
    """A grouped power ladder with convenient access to rows."""

    group: VGroup
    rows: list[VGroup]
    equations: list[MathTex]
    exponents: list[int]
    values: list[int]


SAFE_FRAME_WIDTH = 12.6
SAFE_FRAME_HEIGHT = 6.55
SAFE_EDGE_BUFF = 0.5


def scene_setup(scene: Scene) -> None:
    """Apply theme and reset the moving camera if the scene has one."""

    apply_oceanic_next_theme(scene)
    reset_camera(scene)


def fit_to_safe_frame(
    mobject: Mobject,
    max_width: float = SAFE_FRAME_WIDTH,
    max_height: float = SAFE_FRAME_HEIGHT,
) -> Mobject:
    """Scale a group down if needed so it stays readable inside mobile-safe margins."""

    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def keep_inside_frame(
    mobject: Mobject,
    x_limit: float = FRAME_WIDTH / 2 - SAFE_EDGE_BUFF,
    y_limit: float = FRAME_HEIGHT / 2 - SAFE_EDGE_BUFF,
) -> Mobject:
    """Move a mobject back inside a conservative visible frame."""

    shift = ORIGIN.copy()
    if mobject.get_left()[0] < -x_limit:
        shift += RIGHT * (-x_limit - mobject.get_left()[0])
    if mobject.get_right()[0] > x_limit:
        shift += LEFT * (mobject.get_right()[0] - x_limit)
    if mobject.get_bottom()[1] < -y_limit:
        shift += UP * (-y_limit - mobject.get_bottom()[1])
    if mobject.get_top()[1] > y_limit:
        shift += DOWN * (mobject.get_top()[1] - y_limit)
    mobject.shift(shift)
    return mobject


def reset_camera(scene: Scene, run_time: float = 0) -> None:
    """Return a MovingCameraScene frame to the full canvas."""

    frame = getattr(scene.camera, "frame", None)
    if frame is None:
        return

    if run_time:
        scene.play(frame.animate.set(width=FRAME_WIDTH).move_to(ORIGIN), run_time=run_time)
    else:
        frame.set(width=FRAME_WIDTH)
        frame.move_to(ORIGIN)


def ocean_background(dot_count: int = 80) -> VGroup:
    """Create a deterministic dark scientific background with faint particles."""

    base = Rectangle(
        width=FRAME_WIDTH * 1.4,
        height=FRAME_HEIGHT * 1.4,
        fill_color=BACKGROUND_COLOR,
        fill_opacity=1,
        stroke_opacity=0,
    )
    base.set_z_index(-30)

    grid = VGroup()
    for x in [i * 1.2 - 8.4 for i in range(15)]:
        grid.add(Line([x, -5, 0], [x + 1.3, 5, 0], stroke_width=0.45, color=ACCENT_BLUE))
    for y in [i * 0.9 - 4.5 for i in range(11)]:
        grid.add(Line([-8.5, y, 0], [8.5, y + 0.5, 0], stroke_width=0.35, color=ACCENT_CYAN))
    grid.set_opacity(0.12)
    grid.set_z_index(-25)

    particles = VGroup()
    for i in range(dot_count):
        x = -7.0 + 14.0 * ((i * 37) % 101) / 100
        y = -3.8 + 7.6 * ((i * 53) % 97) / 96
        radius = 0.008 + 0.014 * ((i % 5) / 4)
        dot = Dot([x, y, 0], radius=radius, color=ACCENT_CYAN)
        dot.set_opacity(0.16 + 0.16 * ((i * 7) % 6) / 5)
        particles.add(dot)
    particles.set_z_index(-20)

    return VGroup(base, grid, particles)


def title_text(title: str, subtitle: str | None = None) -> VGroup:
    """Create a large title with an optional small subtitle."""

    main = Text(title, font=WORD_FONT, weight=BOLD, font_size=TITLE_FONT_SIZE, color=WORD_COLOR)
    if subtitle is None:
        return VGroup(main)

    sub = Text(subtitle, font=WORD_FONT, font_size=LABEL_FONT_SIZE, color=WORD_COLOR)
    return VGroup(main, sub).arrange(DOWN, buff=0.22)


def section_label(label: str, color: str = WORD_COLOR, font_size: int = LABEL_FONT_SIZE) -> Text:
    """Small cinematic label used near the edge of a scene."""

    text = Text(label, font=WORD_FONT, font_size=font_size, color=color)
    fit_to_safe_frame(text, max_width=SAFE_FRAME_WIDTH - 0.8, max_height=0.62)
    return text


def with_glow(
    mobject: Mobject,
    glow_color: str = ACCENT_CYAN,
    widths: Sequence[float] = (18, 10, 5),
    opacities: Sequence[float] = (0.06, 0.11, 0.2),
) -> VGroup:
    """Wrap a mobject in soft stroke-only glow copies."""

    glows = VGroup()
    for width, opacity in zip(widths, opacities):
        copy = mobject.copy()
        copy.set_stroke(glow_color, width=width, opacity=opacity)
        copy.set_fill(opacity=0)
        glows.add(copy)
    return VGroup(glows, mobject)


def readable_label(
    mobject: Mobject,
    fill_opacity: float = 0.78,
    buff: float = 0.12,
    corner_radius: float = 0.06,
) -> VGroup:
    """Place a subtle dark plate behind text or equations for small-screen clarity."""

    plate = RoundedRectangle(
        corner_radius=corner_radius,
        width=mobject.width + 2 * buff,
        height=mobject.height + 2 * buff,
        fill_color=BACKGROUND_COLOR,
        fill_opacity=fill_opacity,
        stroke_opacity=0,
    )
    plate.move_to(mobject)
    return VGroup(plate, mobject)


def glowing_equation(
    tex: str,
    font_size: int = EQUATION_FONT_SIZE,
    color: str = TEXT_COLOR,
    glow_color: str = ACCENT_CYAN,
) -> VGroup:
    """Create a glowing MathTex equation."""

    equation = MathTex(tex, font_size=font_size, color=color)
    return with_glow(equation, glow_color=glow_color)


def glow_dot(point, color: str = ACCENT_CYAN, radius: float = 0.07) -> VGroup:
    """Create a bright point with two soft rings."""

    core = Dot(point=point, radius=radius, color=color)
    ring_1 = Circle(radius=radius * 2.8, stroke_color=color, stroke_width=3, stroke_opacity=0.28)
    ring_2 = Circle(radius=radius * 5.0, stroke_color=color, stroke_width=2, stroke_opacity=0.12)
    for ring in (ring_1, ring_2):
        ring.move_to(point)
    return VGroup(ring_2, ring_1, core)


def soft_arrow(start, end, label: str | None = None, color: str = ACCENT_CYAN) -> VGroup:
    """Create a glowing arrow with an optional MathTex label."""

    arrow = Arrow(
        start=start,
        end=end,
        buff=0.08,
        color=color,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.12,
    )
    group = VGroup(arrow)

    if label:
        label_mob = MathTex(label, font_size=30, color=color)
        label_mob.move_to(arrow.get_center())
        shift = rotate_vector(normalize(end - start), PI / 2) * 0.32
        label_mob.shift(shift)
        bg = BackgroundRectangle(label_mob, fill_color=BACKGROUND_COLOR, fill_opacity=0.78, buff=0.08)
        group.add(bg, label_mob)

    return group


def rule_badge(text: str, color: str = ACCENT_CYAN, font_size: int = LABEL_FONT_SIZE) -> VGroup:
    """A compact label for one-line rules."""

    label = Text(text, font=WORD_FONT, font_size=font_size, color=WORD_COLOR)
    box = RoundedRectangle(
        corner_radius=0.08,
        width=label.width + 0.55,
        height=label.height + 0.28,
        fill_color=PANEL_COLOR,
        fill_opacity=0.72,
        stroke_color=color,
        stroke_width=1.4,
        stroke_opacity=0.65,
    )
    box.move_to(label)
    badge = VGroup(box, label)
    fit_to_safe_frame(badge, max_width=4.9, max_height=0.82)
    return badge


def make_power_ladder(
    base: int,
    highest: int,
    lowest: int = 0,
    font_size: int = 44,
    row_width: float = 3.15,
) -> LadderVisual:
    """Build a vertical ladder of powers for a positive integer base."""

    rows: list[VGroup] = []
    equations: list[MathTex] = []
    exponents: list[int] = []
    values: list[int] = []

    for exponent, value in power_sequence(base, highest, lowest):
        value_tex = latex_fraction(value)
        equation = MathTex(
            rf"{base}^{{{exponent}}}",
            "=",
            value_tex,
            font_size=font_size,
            color=TEXT_COLOR,
        )
        box = RoundedRectangle(
            corner_radius=0.08,
            width=row_width,
            height=0.72,
            fill_color=PANEL_COLOR,
            fill_opacity=0.42,
            stroke_color=PANEL_STROKE,
            stroke_width=1.0,
            stroke_opacity=0.75,
        )
        box.move_to(equation)
        row = VGroup(box, equation)
        rows.append(row)
        equations.append(equation)
        exponents.append(exponent)
        values.append(int(value))

    group = VGroup(*rows).arrange(DOWN, buff=0.18)
    return LadderVisual(group=group, rows=rows, equations=equations, exponents=exponents, values=values)


def highlight_box(mobject: Mobject, color: str = ACCENT_CYAN, buff: float = 0.12) -> SurroundingRectangle:
    """Create a highlight rectangle that matches the project style."""

    return SurroundingRectangle(mobject, buff=buff, color=color, stroke_width=3)


def make_factor_chips(symbol: str, count: int, color: str = ACCENT_TEAL) -> VGroup:
    """Create circular factor chips labeled with a symbol."""

    chips = VGroup()
    for _ in range(count):
        circle = Circle(radius=0.34, fill_color=color, fill_opacity=0.22, stroke_color=color, stroke_width=2)
        label = MathTex(symbol, font_size=38, color=TEXT_COLOR)
        label.move_to(circle)
        chips.add(VGroup(circle, label))
    chips.arrange(RIGHT, buff=0.18)
    return chips


def factor_expression(symbol: str, count: int, font_size: int = 46) -> MathTex:
    """Create a compact repeated-multiplication expression."""

    if count == 0:
        return MathTex(r"1", font_size=font_size, color=TEXT_COLOR)
    expression = r" \cdot ".join([symbol] * count)
    return MathTex(expression, font_size=font_size, color=TEXT_COLOR)


def make_block_stack(label: str, color: str = ACCENT_BLUE) -> VGroup:
    """Small block stack used to represent a nonzero quantity."""

    blocks = VGroup()
    for row in range(3):
        for col in range(3):
            block = Square(
                side_length=0.28,
                fill_color=color,
                fill_opacity=0.3 + 0.08 * ((row + col) % 2),
                stroke_color=color,
                stroke_width=1.2,
            )
            block.move_to([col * 0.31, row * 0.31, 0])
            blocks.add(block)
    blocks.move_to(ORIGIN)
    text = MathTex(label, font_size=42, color=TEXT_COLOR).next_to(blocks, DOWN, buff=0.18)
    return VGroup(blocks, text)


def make_exponential_axes(
    base: int,
    color: str = ACCENT_CYAN,
    x_range: Sequence[float] = (-1.25, 3.25, 1),
    y_range: Sequence[float] = (0, 9, 1),
) -> tuple[Axes, VMobject, MathTex]:
    """Create axes, y = base^x, and a curve label."""

    axes = Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=8.0,
        y_length=4.65,
        tips=False,
        axis_config={"color": MUTED_TEXT, "stroke_width": 2},
    )
    x_label = MathTex("x", font_size=28, color=MUTED_TEXT).next_to(axes.x_axis.get_end(), RIGHT, buff=0.12)
    y_label = MathTex("y", font_size=28, color=MUTED_TEXT).next_to(axes.y_axis.get_end(), UP, buff=0.12)
    axes.add(x_label, y_label)

    curve = axes.plot(lambda x: base**x, x_range=[x_range[0], x_range[1]], color=color, stroke_width=5)
    label = MathTex(rf"y={base}^x", font_size=38, color=color)
    label.next_to(curve.point_from_proportion(0.78), UP, buff=0.18)
    return axes, curve, label


def floating_orbit(count: int = 12, radius: float = 2.4, color: str = ACCENT_BLUE) -> VGroup:
    """A subtle circular field for summary scenes."""

    dots = VGroup()
    for i in range(count):
        angle = TAU * i / count
        point = [radius * math.cos(angle), radius * math.sin(angle), 0]
        dot = Dot(point=point, radius=0.025, color=color)
        dot.set_opacity(0.2 + 0.2 * (i % 3) / 2)
        dots.add(dot)
    return dots


def fade_scene(scene: Scene, run_time: float = 0.8) -> None:
    """Fade out all current mobjects except the moving camera frame."""

    if scene.mobjects:
        scene.play(*[FadeOut(mob) for mob in scene.mobjects], run_time=run_time)
