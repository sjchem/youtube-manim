"""Shared visual language and animated constructions for the integral-calculus film."""

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
    """Keep the current explanation visibly alive while narration continues.

    Long holds are divided into slow focus passes across the most recently
    introduced objects.  This keeps formulas, captions, and diagrams breathing
    without the distracting bounce of a short loop or a completely static
    frame.  Every pass returns the object to its exact authored position.
    """
    if seconds <= 0:
        return

    focuses: list[Mobject] = []
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
        focuses.append(candidate)
        if len(focuses) == 3:
            break
    if not focuses or seconds < 0.35:
        scene.wait(max(seconds, 0.0))
        return

    # Around four seconds per pass is slow enough to feel cinematic, while a
    # 10–20 second narration beat now contains several visible developments.
    pass_count = max(1, int(np.ceil(seconds / 4.0)))
    pass_seconds = seconds / pass_count
    directions = (UP, RIGHT, DOWN, LEFT)
    for index in range(pass_count):
        focus = focuses[index % len(focuses)]
        direction = directions[index % len(directions)]
        scene.play(
            focus.animate.scale(1.014).shift(direction * 0.035),
            run_time=pass_seconds,
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
    if remaining > 0.05:
        # The living wait above can safely cover a larger narration tail
        # without freezing the frame.  Always honor the authored chapter
        # boundary so separately generated voice clips remain synchronized.
        narration_wait(scene, remaining)
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


def riemann_group(
    axes: Axes,
    curve: VMobject,
    func: Callable[[float], float],
    a: float,
    b: float,
    n: int,
    color: str = cfg.CYAN,
    opacity: float = 0.55,
    sample: str = "left",
    bounded_graph: VMobject | None = None,
) -> VGroup:
    """Riemann rectangles under `curve` on [a, b], split into n strips.

    Pass `bounded_graph` (another plotted curve) to build strips between two
    curves instead of between one curve and the x-axis.
    """
    dx = (b - a) / n
    return axes.get_riemann_rectangles(
        curve,
        x_range=[a, b],
        dx=dx,
        input_sample_type=sample,
        color=color,
        fill_opacity=opacity,
        stroke_width=min(1.4, 26 / n),
        stroke_color=cfg.BG,
        bounded_graph=bounded_graph,
    )


def area_region(
    axes: Axes,
    curve: VMobject,
    a: float,
    b: float,
    color: str = cfg.CYAN,
    opacity: float = 0.4,
    bounded_graph: VMobject | None = None,
) -> VMobject:
    """A single smooth shaded region under `curve` on [a, b].

    Pass `bounded_graph` to shade the region between two curves instead.
    """
    return axes.get_area(curve, x_range=[a, b], color=color, opacity=opacity, bounded_graph=bounded_graph)


def thin_strip(
    axes: Axes,
    func: Callable[[float], float],
    x0: float,
    dx: float,
    color: str = cfg.GOLD,
    opacity: float = 0.85,
    lower_func: Callable[[float], float] | None = None,
) -> VGroup:
    """One narrow rectangle of width dx: the geometric meaning of f(x) dx."""
    y_top = func(x0)
    y_bottom = lower_func(x0) if lower_func is not None else 0.0
    p1 = axes.c2p(x0, y_bottom)
    p2 = axes.c2p(x0 + dx, y_bottom)
    p3 = axes.c2p(x0 + dx, y_top)
    p4 = axes.c2p(x0, y_top)
    body = Polygon(p1, p2, p3, p4, color=color, fill_color=color, fill_opacity=opacity, stroke_width=1.5)
    glow = body.copy().set_stroke(color, width=6, opacity=0.12).set_fill(opacity=0)
    return VGroup(glow, body)


def dual_axes(
    top_range: Sequence[float],
    bottom_range: Sequence[float],
    x_range: Sequence[float] = (0, 4, 1),
    x_length: float = 10.5,
    y_length: float = 2.55,
    top_y: float = 1.85,
    bottom_y: float = -2.05,
) -> tuple[Axes, Axes]:
    """Two stacked, x-aligned axes for the synchronized derivative/accumulation view."""
    top = Axes(
        x_range=list(x_range),
        y_range=list(top_range),
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.2, "include_ticks": True},
    ).move_to([0, top_y, 0])
    bottom = Axes(
        x_range=list(x_range),
        y_range=list(bottom_range),
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.2, "include_ticks": True},
    ).move_to([0, bottom_y, 0])
    return top, bottom


def river_garden_diagram(width_value: float, fence: float = 100.0, scale: float = 0.062) -> VGroup:
    """A softly isometric garden beside a river, fenced on three sides.

    The offset shadow, perspective bank, grass rows, and fence posts add 3D
    depth without rotating the instructional coordinate system.
    """
    height_value = fence - 2 * width_value
    w = max(width_value * scale, 0.05)
    h = max(height_value * scale, 0.05)
    depth = np.array([0.22, -0.18, 0.0])
    plot = Rectangle(width=w, height=h, color=cfg.GREEN, fill_color=cfg.GREEN, fill_opacity=0.28, stroke_width=0)
    shadow = plot.copy().set_fill("#020C16", opacity=0.42).shift(depth)

    rows = VGroup()
    for alpha in np.linspace(0.18, 0.82, 4):
        y = plot.get_bottom()[1] + alpha * h
        rows.add(Line([plot.get_left()[0] + 0.08, y, 0], [plot.get_right()[0] - 0.08, y, 0], color=cfg.GREEN, stroke_width=1.4, stroke_opacity=0.5))

    river_bank = Polygon(
        plot.get_corner(UL) + UP * 0.02,
        plot.get_corner(UR) + UP * 0.02,
        plot.get_corner(UR) + UP * 0.28 + depth,
        plot.get_corner(UL) + UP * 0.28 + depth,
        color=cfg.BLUE,
        fill_color=cfg.BLUE,
        fill_opacity=0.42,
        stroke_width=0,
    )
    river = Line(LEFT * (w / 2 + 0.32), RIGHT * (w / 2 + 0.32), color=cfg.CYAN, stroke_width=8)
    river.next_to(plot, UP, buff=0.0)
    fence_left = Line(plot.get_corner(UL), plot.get_corner(DL), color=cfg.GOLD, stroke_width=6)
    fence_right = Line(plot.get_corner(UR), plot.get_corner(DR), color=cfg.GOLD, stroke_width=6)
    fence_bottom = Line(plot.get_corner(DL), plot.get_corner(DR), color=cfg.GOLD, stroke_width=6)
    posts = VGroup()
    for point in (plot.get_corner(UL), plot.get_corner(DL), plot.get_corner(UR), plot.get_corner(DR)):
        posts.add(Line(point + DOWN * 0.08, point + UP * 0.18, color=cfg.WHITE, stroke_width=4))
    return VGroup(shadow, river_bank, plot, rows, fence_left, fence_right, fence_bottom, posts, river)


def uv_rectangle(u_value: float, v_value: float, color_u: str = cfg.CYAN, color_v: str = cfg.GOLD, scale: float = 0.9) -> VGroup:
    """A rectangle with labeled sides u and v, used for the integration-by-parts derivation."""
    width = u_value * scale
    height = v_value * scale
    rect = Rectangle(width=width, height=height, color=cfg.WHITE, fill_color=cfg.PANEL, fill_opacity=0.7, stroke_width=3)
    u_label = eq("u", color_u, cfg.FONT["body"]).next_to(rect, DOWN, buff=0.22)
    v_label = eq("v", color_v, cfg.FONT["body"]).next_to(rect, LEFT, buff=0.22)
    return VGroup(rect, u_label, v_label)


def color_formula_parts(formula: MathTex) -> MathTex:
    """Apply the film's semantic colors to common symbols when present."""
    formula.set_color_by_tex("lim", cfg.PURPLE)
    formula.set_color_by_tex("int", cfg.CYAN)
    formula.set_color_by_tex("sin", cfg.CYAN)
    formula.set_color_by_tex("cos", cfg.GREEN)
    return formula
