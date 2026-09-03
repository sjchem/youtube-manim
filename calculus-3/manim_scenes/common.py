"""Shared visual language and animated constructions for the differential-equations film."""

from __future__ import annotations

import warnings
from collections.abc import Callable, Sequence

import numpy as np
from manim import *

import config as cfg
from utils.math_utils import normalized_slope_step
from utils.render_helpers import slope_field_rows


# ---------------------------------------------------------------------------
# Chapter scaffolding
# ---------------------------------------------------------------------------


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
    # 10-20 second narration beat now contains several visible developments.
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
    reset_flat_camera(scene)
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


# ---------------------------------------------------------------------------
# 3D camera helpers
#
# The full film renders as one ThreeDScene so flat and dimensional chapters can
# share a timeline.  Every helper degrades to a no-op under a flat camera, which
# keeps the individual 2D scene classes and the frame-free audit tools working.
# ---------------------------------------------------------------------------


def has_3d_camera(scene: Scene) -> bool:
    return isinstance(getattr(scene, "camera", None), ThreeDCamera)


def set_3d_view(scene: Scene, phi: float, theta: float, zoom: float = 1.0) -> None:
    """Jump straight to a 3D viewpoint, ignored when the camera is flat."""
    if has_3d_camera(scene):
        scene.set_camera_orientation(phi=phi, theta=theta, zoom=zoom)


def move_3d_view(scene: Scene, phi: float, theta: float, run_time: float = 2.0, **kwargs) -> None:
    """Glide to a 3D viewpoint, or simply hold the beat under a flat camera."""
    if has_3d_camera(scene):
        scene.move_camera(phi=phi, theta=theta, run_time=run_time, **kwargs)
    else:
        scene.wait(run_time)


def reset_flat_camera(scene: Scene) -> None:
    """Return the camera to the head-on orientation the 2D chapters assume."""
    if has_3d_camera(scene):
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        scene.stop_ambient_camera_rotation()


def orbit_hold(scene: Scene, seconds: float, rate: float = 0.045) -> None:
    """Hold a 3D beat alive by drifting the camera rather than nudging mobjects.

    `narration_wait` keeps a flat frame breathing by scaling the most recent
    mobjects, which is the wrong move for a Surface or a disk stack: it is
    expensive to re-render and it distorts the geometry being explained.  Under
    a 3D camera the drift itself supplies the motion; under a flat camera this
    falls back to the usual living wait.
    """
    if not has_3d_camera(scene):
        narration_wait(scene, seconds)
        return
    # Alternate the drift direction on each hold.  Always drifting the same way
    # walks the camera right around the subject over a long chapter, and a
    # chapter about slicing a solid along the x-axis is ruined the moment the
    # camera ends up looking down that axis: the coin stack reads as a set of
    # concentric rings.  Swaying keeps every hold near its authored viewpoint.
    sign = getattr(scene, "_orbit_drift_sign", 1.0)
    scene._orbit_drift_sign = -sign
    scene.begin_ambient_camera_rotation(rate=rate * sign)
    scene.wait(seconds)
    scene.stop_ambient_camera_rotation()


def pin_to_frame(scene: Scene, *mobjects: Mobject) -> None:
    """Keep captions and formulas facing the viewer while the 3D camera moves."""
    if has_3d_camera(scene):
        scene.add_fixed_in_frame_mobjects(*mobjects)
    else:
        scene.add(*mobjects)



# ---------------------------------------------------------------------------
# Background and typography
# ---------------------------------------------------------------------------


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


def hide_background(scene: Scene) -> VGroup | None:
    """Detach the flat background before a 3D beat, returning it for later reuse."""
    for mob in list(scene.mobjects):
        if getattr(mob, "_is_project_background", False):
            mob.suspend_updating()
            scene.remove(mob)
            return mob
    return None


def restore_background(scene: Scene, background: VGroup | None) -> None:
    """Return to the flat viewpoint, then put the shared background back.

    The background is a flat rectangle living in the z = 0 plane, so adding it
    while the camera is still tilted renders it skewed across the frame.
    Resetting the camera here keeps the two steps from ever being separated.
    """
    reset_flat_camera(scene)
    if background is None:
        return
    background.resume_updating()
    scene.add(background)


def outlined_text(text: str, font_size: int, color: str = cfg.WHITE, weight=BOLD) -> Text:
    result = Text(text, font_size=font_size, color=color, weight=weight)
    result.set_stroke(cfg.BG, width=4, opacity=0.95, background=True)
    return result


def title_card(title: str, subtitle: str | None = None, color: str = cfg.GOLD) -> VGroup:
    """The film's hero title: a glowing shadow layer under a rules-and-subtitle stack."""
    heading = outlined_text(title, cfg.FONT["title"], color, BOLD)
    if heading.width > cfg.SAFE_WIDTH:
        heading.scale_to_fit_width(cfg.SAFE_WIDTH)
    shadow = heading.copy().set_color(color).set_opacity(0.18).set_stroke(width=0, background=True)
    shadow.shift(DOWN * 0.06 + RIGHT * 0.06).scale(1.02)
    # A drop shadow is meant to sit under its own glyphs; the layout audit
    # skips it so the deliberate overlap is not reported as a collision.
    for glyph in shadow.get_family():
        glyph._is_decorative_shadow = True
    stacked = VGroup(shadow, heading)
    rule = Line(
        LEFT * min(heading.width * 0.48, 5.7),
        RIGHT * min(heading.width * 0.48, 5.7),
        color=cfg.CYAN,
        stroke_width=4,
    )
    group = VGroup(stacked, rule).arrange(DOWN, buff=0.2)
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


def fitted_eq(latex: str, color: str = cfg.WHITE, font_size: int | None = None, width: float | None = None) -> MathTex:
    """An equation guaranteed to stay inside the safe frame."""
    formula = eq(latex, color, font_size)
    limit = width or cfg.SAFE_WIDTH
    if formula.width > limit:
        formula.scale_to_fit_width(limit)
    return formula


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


def live_readout(
    label: str,
    value: Callable[[], float],
    color: str = cfg.WHITE,
    font_size: int | None = None,
    decimal_places: int = 1,
    suffix: str | None = None,
) -> VGroup:
    """A static LaTeX label beside a number that updates every frame.

    Rebuilding a MathTex from an f-string inside `always_redraw` forces a fresh
    LaTeX compile for every distinct value it ever displays, which quietly
    dominates render time for a counter that sweeps a range.  A DecimalNumber
    reuses cached digit glyphs instead, so only the label is ever compiled.

    The number re-anchors to the label each frame, so the readout stays put as
    its digit count changes, and the caller can position the whole group.
    """
    size = font_size or cfg.FONT["small"]
    tag = eq(label, color, size)
    number = DecimalNumber(value(), num_decimal_places=decimal_places, color=color, font_size=size)
    number.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    tail = eq(suffix, color, size) if suffix else None

    parts = [tag, number] + ([tail] if tail else [])
    group = VGroup(*parts).arrange(RIGHT, buff=0.16)

    def refresh(mob: Mobject) -> None:
        mob.set_value(value())
        mob.next_to(tag, RIGHT, buff=0.16)
        if tail is not None:
            tail.next_to(mob, RIGHT, buff=0.10)

    number.add_updater(refresh)
    return group


def bottom_caption(text: str, color: str = cfg.GOLD) -> Text:
    caption = outlined_text(text, cfg.FONT["body"], color, BOLD)
    if caption.width > cfg.SAFE_WIDTH - 0.5:
        caption.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(DOWN, buff=0.28)


def top_caption(text: str, color: str = cfg.CYAN) -> Text:
    caption = outlined_text(text, cfg.FONT["body"], color, BOLD)
    if caption.width > cfg.SAFE_WIDTH - 0.5:
        caption.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(UP, buff=0.30)


def chip(text: str, color: str = cfg.CYAN, font_size: int | None = None) -> VGroup:
    """A small labelled plate used for the film's concept chains."""
    label = outlined_text(text, font_size or cfg.FONT["tiny"], color, BOLD)
    frame = RoundedRectangle(
        width=label.width + 0.46,
        height=label.height + 0.42,
        corner_radius=0.13,
        color=color,
        stroke_width=2.6,
        fill_color=cfg.PANEL,
        fill_opacity=0.78,
    )
    return VGroup(frame, label)


# ---------------------------------------------------------------------------
# Glow primitives
# ---------------------------------------------------------------------------


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


def dashed_connector(start: Sequence[float], end: Sequence[float], color: str = cfg.MUTED, dashes: int = 12, stroke_width: float = 2.6) -> VGroup:
    """A dashed guide line assembled from separate segments, safe to fade out."""
    start_point = np.array(start, dtype=float)
    end_point = np.array(end, dtype=float)
    group = VGroup()
    for index in range(dashes):
        a = index / dashes
        b = (index + 0.55) / dashes
        group.add(Line(start_point + (end_point - start_point) * a, start_point + (end_point - start_point) * b, color=color, stroke_width=stroke_width))
    return group


# ---------------------------------------------------------------------------
# Axes
# ---------------------------------------------------------------------------


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


def labelled_axes(
    axes: Axes,
    x_tex: str,
    y_tex: str,
    color: str = cfg.CYAN,
    font_size: int | None = None,
) -> VGroup:
    """Axis labels placed outside the plot area so shading never hides them."""
    size = font_size or cfg.FONT["label"]
    x_label = eq(x_tex, color, size).next_to(axes.x_axis.get_right(), RIGHT, buff=0.20).shift(DOWN * 0.08)
    y_label = eq(y_tex, color, size).next_to(axes.y_axis.get_top(), LEFT, buff=0.20).shift(UP * 0.02)
    return VGroup(x_label, y_label)


def compact_axis_labels(
    axes: Axes,
    x_tex: str,
    y_tex: str,
    color: str = cfg.MUTED,
    font_size: int | None = None,
) -> VGroup:
    """Axis labels tucked under and above a panel that sits near the frame edge.

    `labelled_axes` hangs its labels off the ends of the axes, which runs out
    of room for a wide plot pushed to one side; this variant keeps both labels
    within the plot's own column.
    """
    size = font_size or cfg.FONT["small"]
    x_label = eq(x_tex, color, size).next_to(axes.x_axis, DOWN, buff=0.30)
    y_label = eq(y_tex, color, size).next_to(axes.y_axis.get_top(), UP, buff=0.18)
    return VGroup(x_label, y_label)


def stacked_axes(
    x_range: Sequence[float],
    top_y_range: Sequence[float],
    bottom_y_range: Sequence[float],
    x_length: float = 9.6,
    y_length: float = 2.5,
    top_center: float = 1.75,
    bottom_center: float = -2.05,
) -> tuple[Axes, Axes]:
    """Two x-aligned panels: the rate on top, what it accumulates underneath."""
    top = Axes(
        x_range=list(x_range),
        y_range=list(top_y_range),
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.2, "include_ticks": True},
    ).move_to([0, top_center, 0])
    bottom = Axes(
        x_range=list(x_range),
        y_range=list(bottom_y_range),
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.2, "include_ticks": True},
    ).move_to([0, bottom_center, 0])
    return top, bottom


def area_region(
    axes: Axes,
    curve: VMobject,
    a: float,
    b: float,
    color: str = cfg.CYAN,
    opacity: float = 0.4,
    bounded_graph: VMobject | None = None,
) -> VMobject:
    """A single smooth shaded region under `curve` on [a, b]."""
    return axes.get_area(curve, x_range=[a, b], color=color, opacity=opacity, bounded_graph=bounded_graph)


# ---------------------------------------------------------------------------
# Slope fields: the central visual idea of the film
# ---------------------------------------------------------------------------


def slope_tick(
    axes: Axes,
    x: float,
    y: float,
    slope: float,
    color: str,
    half_length: float = 0.20,
    stroke_width: float = 3.4,
) -> Line:
    """One direction tick of fixed screen length, tilted by the local slope."""
    dx, dy = normalized_slope_step(slope, half_length)
    return Line(
        axes.c2p(x - dx, y - dy),
        axes.c2p(x + dx, y + dy),
        color=color,
        stroke_width=stroke_width,
    )


def slope_tick_color(slope: float, limit: float = 2.6) -> str:
    """Cyan where the field is gentle, gold where it steepens, purple at the extremes."""
    magnitude = min(abs(slope) / limit, 1.0)
    if magnitude < 0.34:
        return cfg.CYAN
    if magnitude < 0.72:
        return cfg.BLUE
    return cfg.GOLD


def slope_field(
    axes: Axes,
    slope_fn: Callable[[float, float], float],
    x_range: Sequence[float],
    y_range: Sequence[float],
    half_length: float = 0.20,
    color: str | None = None,
) -> list[VGroup]:
    """The slope field as a list of rows, bottom row first, ready for a staged reveal."""
    rows: list[VGroup] = []
    for row in slope_field_rows(x_range, y_range):
        band = VGroup()
        for x, y in row:
            slope = slope_fn(x, y)
            band.add(slope_tick(axes, x, y, slope, color or slope_tick_color(slope), half_length))
        rows.append(band)
    return rows


def solution_curve(
    axes: Axes,
    solution: Callable[[float], float],
    x_start: float,
    x_end: float,
    color: str = cfg.GREEN,
    stroke_width: float = 6,
    y_clip: tuple[float, float] | None = None,
) -> VMobject:
    """A solution drawn only where it stays inside the visible window."""
    samples = np.linspace(x_start, x_end, 220)
    points: list[np.ndarray] = []
    low, high = y_clip if y_clip else (-np.inf, np.inf)
    for x in samples:
        y = solution(float(x))
        if not np.isfinite(y) or y < low or y > high:
            break
        points.append(axes.c2p(float(x), float(y)))
    if len(points) < 2:
        points = [axes.c2p(x_start, solution(x_start))] * 2
    curve = VMobject(color=color, stroke_width=stroke_width)
    curve.set_points_smoothly(points)
    return curve


# ---------------------------------------------------------------------------
# Physical props
# ---------------------------------------------------------------------------


def car_icon(color: str = cfg.CYAN, scale: float = 1.0) -> VGroup:
    """A simple stylized car, facing right."""
    body = RoundedRectangle(width=1.7, height=0.55, corner_radius=0.16, color=color, fill_color=color, fill_opacity=0.85, stroke_width=2)
    body.shift(UP * 0.28)
    cabin = RoundedRectangle(width=0.95, height=0.42, corner_radius=0.14, color=color, fill_color=cfg.PANEL_2, fill_opacity=0.9, stroke_width=2)
    cabin.shift(UP * 0.62)
    wheel_1 = Circle(radius=0.19, color=cfg.GRAY, fill_color="#05121F", fill_opacity=1, stroke_width=3).shift(LEFT * 0.55 + UP * 0.02)
    wheel_2 = Circle(radius=0.19, color=cfg.GRAY, fill_color="#05121F", fill_opacity=1, stroke_width=3).shift(RIGHT * 0.55 + UP * 0.02)
    headlight = Dot(radius=0.055, color=cfg.GOLD).move_to(body.get_right() + UP * 0.02)
    return VGroup(body, cabin, wheel_1, wheel_2, headlight).scale(scale)


def speedometer(radius: float = 0.85, color: str = cfg.CYAN) -> tuple[VGroup, VGroup]:
    """A fluorescent, layered dashboard dial and its independently moving needle."""
    shadow = Circle(
        radius=radius * 1.10,
        fill_color=BLACK,
        fill_opacity=0.48,
        stroke_width=0,
    ).shift(RIGHT * radius * 0.08 + DOWN * radius * 0.10)

    outer_glow = VGroup(
        Circle(radius=radius * 1.18, color=color, stroke_width=28, stroke_opacity=0.06),
        Circle(radius=radius * 1.11, color=color, stroke_width=16, stroke_opacity=0.14),
        Circle(radius=radius * 1.055, color=color, stroke_width=7, stroke_opacity=0.45),
    )
    bezel = Circle(
        radius=radius * 1.02,
        color=cfg.GRAY,
        stroke_width=9,
        fill_color="#06111B",
        fill_opacity=1,
    )
    bezel_shadow = Arc(
        radius=radius * 1.02,
        start_angle=195 * DEGREES,
        angle=175 * DEGREES,
        color="#02070C",
        stroke_width=11,
        stroke_opacity=0.92,
    )
    bezel_highlight = Arc(
        radius=radius * 1.02,
        start_angle=15 * DEGREES,
        angle=155 * DEGREES,
        color=cfg.WHITE,
        stroke_width=4,
        stroke_opacity=0.38,
    )
    face = Circle(
        radius=radius * 0.91,
        color=color,
        stroke_width=2.4,
        stroke_opacity=0.82,
        fill_color="#020D16",
        fill_opacity=0.98,
    )
    inner_halo = Circle(radius=radius * 0.84, color=color, stroke_width=8, stroke_opacity=0.055)

    # A 270-degree sweep: zero at lower-left, maximum at lower-right.
    ticks = VGroup()
    tick_glow = VGroup()
    numbers = VGroup()
    for index in range(21):
        angle = (225 - 13.5 * index) * DEGREES
        direction = np.array([np.cos(angle), np.sin(angle), 0])
        major = index % 4 == 0
        outer = radius * (0.80 if major else 0.78) * direction
        inner = radius * (0.64 if major else 0.70) * direction
        width = 3.2 if major else 1.8
        opacity = 1.0 if major else 0.72
        tick_glow.add(Line(inner, outer, color=color, stroke_width=width * 3.4, stroke_opacity=0.10))
        ticks.add(Line(inner, outer, color=color, stroke_width=width, stroke_opacity=opacity))
        if major:
            number = Text(str(index * 10), font_size=max(14, int(radius * 18)), color=cfg.WHITE, weight=MEDIUM)
            number.move_to(radius * 0.49 * direction)
            numbers.add(number)

    unit = Text("km/h", font_size=max(14, int(radius * 18)), color=cfg.MUTED, weight=MEDIUM)
    unit.move_to([0, -radius * 0.62, 0])

    start_angle = 225 * DEGREES
    needle_direction = np.array([np.cos(start_angle), np.sin(start_angle), 0])
    needle_start = -radius * 0.10 * needle_direction
    needle_end = radius * 0.68 * needle_direction
    needle_glow = Line(needle_start, needle_end, color=cfg.RED, stroke_width=17, stroke_opacity=0.13)
    needle_core = Line(needle_start, needle_end, color=cfg.RED, stroke_width=5.5)
    needle_tip = Dot(needle_end, radius=radius * 0.035, color=cfg.GOLD)
    needle = VGroup(needle_glow, needle_core, needle_tip)

    hub_glow = Circle(radius=radius * 0.16, color=color, stroke_width=0, fill_color=color, fill_opacity=0.10)
    hub_ring = Circle(radius=radius * 0.105, color=cfg.GRAY, stroke_width=3, fill_color="#071521", fill_opacity=1)
    hub = Dot(ORIGIN, radius=radius * 0.055, color=cfg.RED)
    glass_reflection = Arc(
        radius=radius * 0.73,
        start_angle=34 * DEGREES,
        angle=105 * DEGREES,
        color=cfg.WHITE,
        stroke_width=5,
        stroke_opacity=0.16,
    )

    dial = VGroup(
        shadow,
        outer_glow,
        bezel,
        bezel_shadow,
        bezel_highlight,
        face,
        inner_halo,
        tick_glow,
        ticks,
        numbers,
        unit,
        needle,
        hub_glow,
        hub_ring,
        hub,
        glass_reflection,
    )
    return dial, needle


def mug(temperature_color: str = cfg.ORANGE, scale: float = 1.0) -> VGroup:
    """A shaded perspective mug assembled from crisp vector layers."""
    ground_shadow = Ellipse(
        width=1.52,
        height=0.22,
        fill_color=BLACK,
        fill_opacity=0.34,
        stroke_width=0,
    ).move_to([0.08, -0.82, 0])

    # The handle is drawn first so the cup body correctly occludes its left side.
    handle_shadow = Arc(
        radius=0.47,
        start_angle=-82 * DEGREES,
        angle=164 * DEGREES,
        color=BLACK,
        stroke_width=20,
        stroke_opacity=0.35,
    ).move_to([0.76, -0.02, 0]).shift(RIGHT * 0.05 + DOWN * 0.04)
    handle = Arc(
        radius=0.46,
        start_angle=-82 * DEGREES,
        angle=164 * DEGREES,
        color=temperature_color,
        stroke_width=15,
    ).move_to([0.76, -0.02, 0])
    handle_inner = Arc(
        radius=0.46,
        start_angle=-78 * DEGREES,
        angle=156 * DEGREES,
        color=cfg.PANEL_2,
        stroke_width=6,
    ).move_to([0.76, -0.02, 0])
    handle_glint = Arc(
        radius=0.46,
        start_angle=24 * DEGREES,
        angle=48 * DEGREES,
        color=cfg.WHITE,
        stroke_width=3,
        stroke_opacity=0.55,
    ).move_to([0.76, -0.02, 0])

    body = Polygon(
        [-0.66, 0.58, 0],
        [0.66, 0.58, 0],
        [0.53, -0.68, 0],
        [0.38, -0.76, 0],
        [-0.38, -0.76, 0],
        [-0.53, -0.68, 0],
        color=cfg.WHITE,
        fill_color=temperature_color,
        fill_opacity=0.90,
        stroke_width=3.5,
    )
    left_shade = Polygon(
        [-0.65, 0.55, 0],
        [-0.37, 0.55, 0],
        [-0.29, -0.69, 0],
        [-0.50, -0.66, 0],
        fill_color="#5A2A16",
        fill_opacity=0.34,
        stroke_width=0,
    )
    right_glow = Polygon(
        [0.24, 0.53, 0],
        [0.53, 0.49, 0],
        [0.43, -0.57, 0],
        [0.20, -0.62, 0],
        fill_color=cfg.WHITE,
        fill_opacity=0.17,
        stroke_width=0,
    )

    bottom_rim = Ellipse(
        width=0.94,
        height=0.18,
        color=cfg.MUTED,
        fill_color="#5B2C18",
        fill_opacity=0.62,
        stroke_width=2.4,
    ).move_to([0, -0.71, 0])
    lip = Ellipse(
        width=1.34,
        height=0.31,
        color=cfg.WHITE,
        fill_color="#F4D7B0",
        fill_opacity=1,
        stroke_width=3.5,
    ).move_to([0, 0.58, 0])
    coffee = Ellipse(
        width=1.17,
        height=0.22,
        color="#FFD7A0",
        fill_color="#632B16",
        fill_opacity=1,
        stroke_width=2.0,
    ).move_to([0, 0.58, 0])
    coffee_glow = Arc(
        radius=0.51,
        start_angle=18 * DEGREES,
        angle=142 * DEGREES,
        color=cfg.ORANGE,
        stroke_width=4,
        stroke_opacity=0.80,
    ).stretch(0.21, 1).move_to([0, 0.59, 0])
    body_glint = Line(
        [-0.18, 0.40, 0],
        [-0.12, -0.48, 0],
        color=cfg.WHITE,
        stroke_width=5,
        stroke_opacity=0.23,
    )

    return VGroup(
        ground_shadow,
        handle_shadow,
        handle,
        handle_inner,
        handle_glint,
        body,
        left_shade,
        right_glow,
        bottom_rim,
        lip,
        coffee,
        coffee_glow,
        body_glint,
    ).scale(scale)


def spring_shape(
    start: Sequence[float],
    end: Sequence[float],
    coils: int = 9,
    amplitude: float = 0.30,
    color: str = cfg.CYAN,
    stroke_width: float = 4.5,
) -> VMobject:
    """A zig-zag spring drawn between two points, stretching as the ends move."""
    start_point = np.array(start, dtype=float)
    end_point = np.array(end, dtype=float)
    axis = end_point - start_point
    length = float(np.linalg.norm(axis))
    if length < 1e-6:
        axis = np.array([1.0, 0.0, 0.0])
        length = 1.0
    unit = axis / length
    normal = np.array([-unit[1], unit[0], 0.0])
    lead = 0.16 * length
    points = [start_point, start_point + unit * lead]
    segments = coils * 2
    span = length - 2 * lead
    for index in range(1, segments):
        offset = normal * amplitude * (1 if index % 2 else -1)
        points.append(start_point + unit * (lead + span * index / segments) + offset)
    points.extend([end_point - unit * lead, end_point])
    coil = VMobject(color=color, stroke_width=stroke_width)
    coil.set_points_as_corners(points)
    return coil


def block(size: float = 0.78, color: str = cfg.GOLD, label: str | None = None) -> VGroup:
    """The oscillating mass: a solid plate with an optional label."""
    face = RoundedRectangle(width=size, height=size, corner_radius=0.10, color=color, fill_color=color, fill_opacity=0.55, stroke_width=4)
    highlight = RoundedRectangle(width=size * 0.7, height=size * 0.22, corner_radius=0.06, color=cfg.WHITE, fill_color=cfg.WHITE, fill_opacity=0.16, stroke_width=0)
    highlight.move_to(face.get_center() + UP * size * 0.24)
    group = VGroup(face, highlight)
    if label:
        group.add(eq(label, cfg.BG, cfg.FONT["small"]).move_to(face.get_center()))
    return group


def particle_cloud(
    count: int,
    width: float = 4.2,
    height: float = 2.6,
    color: str = cfg.GREEN,
    seed: int = cfg.SEED,
    radius: float = 0.075,
) -> VGroup:
    """A deterministic scatter of particles, centred on the origin.

    The seed is explicit so a chapter's particles land in the same places on
    every render, which matters when a later beat fades them out in a computed
    order rather than at random.
    """
    rng = np.random.default_rng(seed)
    cloud = VGroup()
    for _ in range(count):
        x = float(rng.uniform(-width / 2, width / 2))
        y = float(rng.uniform(-height / 2, height / 2))
        cloud.add(Dot([x, y, 0], radius=radius, color=color).set_stroke(cfg.BG, width=1.4))
    return cloud


# ---------------------------------------------------------------------------
# 3D constructions
# ---------------------------------------------------------------------------


def three_d_axes(
    x_range: Sequence[float] = (-2, 2, 1),
    y_range: Sequence[float] = (-2, 2, 1),
    z_range: Sequence[float] = (-2, 2, 1),
    unit: float = 1.25,
) -> ThreeDAxes:
    """3D axes with one shared scale on all three directions.

    Deriving every axis length from the same scene-units-per-data-unit keeps
    the geometry honest: a sphere of radius 1 renders as a sphere rather than
    an ellipsoid, which matters when the whole point of a chapter is a volume.
    """
    return ThreeDAxes(
        x_range=list(x_range),
        y_range=list(y_range),
        z_range=list(z_range),
        x_length=(x_range[1] - x_range[0]) * unit,
        y_length=(y_range[1] - y_range[0]) * unit,
        z_length=(z_range[1] - z_range[0]) * unit,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.2, "include_ticks": False},
    )


def revolution_surface(
    axes: ThreeDAxes,
    profile: Callable[[float], float],
    x_start: float,
    x_end: float,
    resolution: tuple[int, int] = (24, 40),
    color: str = cfg.BLUE,
    opacity: float = 0.55,
) -> Surface:
    """The solid swept out by spinning y = profile(x) about the x-axis."""

    # Sample x through a cosine substitution rather than uniformly.  A profile
    # like sqrt(1 - x^2) has a vertical tangent at each end, so uniform samples
    # leave one enormous, nearly edge-on band of quads at the poles, which the
    # Cairo renderer draws as long radiating slivers.  Clustering the samples
    # towards the ends is exactly how a clean sphere mesh is built.
    midpoint = 0.5 * (x_start + x_end)
    half_span = 0.5 * (x_end - x_start)

    def parametrization(s: float, v: float) -> np.ndarray:
        x = midpoint - half_span * np.cos(s)
        radius = profile(x)
        return axes.c2p(x, radius * np.cos(v), radius * np.sin(v))

    surface = Surface(
        parametrization,
        u_range=[0, PI],
        v_range=[0, TAU],
        resolution=resolution,
        fill_opacity=opacity,
        stroke_width=0.6,
        checkerboard_colors=[color, cfg.CYAN],
    )
    surface.set_stroke(cfg.BG, width=0.6, opacity=0.35)
    return surface


def disk_stack(
    axes: ThreeDAxes,
    profile: Callable[[float], float],
    count: int,
    radius: float = 1.0,
    color: str = cfg.GOLD,
    opacity: float = 0.72,
) -> VGroup:
    """The solid rebuilt as `count` flat disks of thickness dx, standing on the x-axis."""
    from utils.render_helpers import disk_slice_positions

    unit = float(np.linalg.norm(axes.c2p(1, 0, 0) - axes.c2p(0, 0, 0)))
    stack = VGroup()
    for center_x, dx in disk_slice_positions(count, radius):
        disk_radius = profile(center_x)
        if disk_radius <= 1e-3:
            continue
        # Cylinder inherits Surface's checkerboard colouring, which silently
        # overrides fill_color; the two-tone stack below is what actually
        # decides how these disks look.
        disk = Cylinder(
            radius=disk_radius * unit,
            height=dx * unit,
            direction=RIGHT,
            checkerboard_colors=[color, cfg.ORANGE],
            fill_opacity=opacity,
            stroke_width=0.8,
            stroke_color=cfg.BG,
            resolution=(2, 22),
            # The generated end caps ignore the checkerboard colours and render as
            # one flat disk that hides the whole stack behind it.
            show_ends=False,
        )
        disk.move_to(axes.c2p(center_x, 0, 0))
        stack.add(disk)
    return stack


def phase_helix(
    axes: ThreeDAxes,
    position: Callable[[float], float],
    velocity: Callable[[float], float],
    t_start: float,
    t_end: float,
    time_scale: float,
    velocity_scale: float,
    color: str = cfg.PURPLE,
    stroke_width: float = 5,
) -> VMobject:
    """Position and velocity plotted against time: the oscillator's trajectory as a helix."""
    samples = np.linspace(t_start, t_end, 320)
    points = [
        axes.c2p(position(float(t)), velocity(float(t)) * velocity_scale, (float(t) - t_start) * time_scale)
        for t in samples
    ]
    helix = VMobject(color=color, stroke_width=stroke_width)
    helix.set_points_smoothly(points)
    return helix


def orbit_path(axes: ThreeDAxes, trajectory: np.ndarray, color: str = cfg.CYAN, stroke_width: float = 4.5) -> VMobject:
    """A numerically integrated orbit, drawn on 3D axes in the z = 0 plane."""
    stride = max(len(trajectory) // 320, 1)
    points = [axes.c2p(float(x), float(y), 0.0) for x, y in trajectory[::stride]]
    path = VMobject(color=color, stroke_width=stroke_width)
    path.set_points_smoothly(points)
    return path
