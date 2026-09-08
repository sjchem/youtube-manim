"""Shared visual language and animated constructions for the Functions film.

Everything here exists so that a single idea always *looks* the same:
a machine is always a glowing rounded box, a value in flight is always a pill,
and the colours never change meaning between chapters.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg

# ----------------------------------------------------------------------------
# Scene lifecycle
# ----------------------------------------------------------------------------


def begin_scene(scene: Scene, scene_key: str) -> float:
    """Apply the theme and remember this chapter's start time."""
    cfg.apply_project_theme(scene, bubbles=False)
    scene._project_scene_key = scene_key
    return float(scene.time)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """scene.play with an explicit default run time, so pacing is never accidental."""
    kwargs["run_time"] = kwargs.get("run_time", 1.0)
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Keep the current visual gently alive while the narration continues."""
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
            # Degenerate mobjects cannot report a bounding box; skip defensively.
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
    """Finish on the configured frame boundary, including the closing fade."""
    fps = float(scene.camera.frame_rate)
    fade_frames = round(cfg.TIMING["transition"] * fps)
    elapsed_frames = round((float(scene.time) - started_at) * fps)
    target_frames = round(target_seconds * fps)
    remaining_frames = target_frames - elapsed_frames - fade_frames
    key = getattr(scene, "_project_scene_key", "unknown")
    if remaining_frames < 0:
        raise ValueError(f"Scene {key} exceeds its target by {-remaining_frames / fps:.2f}s; retime its beats.")
    if remaining_frames > 0:
        narration_wait(scene, remaining_frames / fps)
    visible = [
        mob for mob in scene.mobjects
        if fade_background or not getattr(mob, "_is_project_background", False)
    ]
    # A live updater must not rebuild a mobject while FadeOut is hiding it.
    for mob in visible:
        mob.clear_updaters()
    if visible:
        scene.play(FadeOut(*visible), run_time=fade_frames / fps)
        scene.remove(*visible)
    else:
        scene.wait(fade_frames / fps)


# ----------------------------------------------------------------------------
# Background
# ----------------------------------------------------------------------------


def oceanic_bubbles_layer() -> VGroup:
    from themes.oceanic_next import oceanic_bubbles

    return oceanic_bubbles()


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


def add_cinematic_background(scene: Scene, show_bubbles: bool = True) -> VGroup:
    """Reuse one living background when several chapters share a Scene."""
    for mob in scene.mobjects:
        if getattr(mob, "_is_project_background", False):
            return mob
    background = cinematic_background(show_bubbles)
    scene.add(background)
    return background


def clear_background(scene: Scene) -> None:
    """Drop the flat background layer (a 3D chapter must not tilt a flat plane)."""
    layers = [mob for mob in scene.mobjects if getattr(mob, "_is_project_background", False)]
    if layers:
        scene.remove(*layers)


# ----------------------------------------------------------------------------
# Type
# ----------------------------------------------------------------------------


def outlined_text(text: str, font_size: int, color: str = cfg.WHITE, weight=BOLD) -> Text:
    result = Text(text, font_size=font_size, color=color, weight=weight)
    result.set_stroke(cfg.BG, width=4, opacity=0.95, background=True)
    return result


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


def title_card(title: str, subtitle: str | None = None, color: str = cfg.GOLD) -> VGroup:
    """A hero title with a soft coloured shadow behind it."""
    heading = outlined_text(title, cfg.FONT["title"], color, BOLD)
    # The soft shadow sits 3% larger, so fit the glyphs inside a slightly tighter box.
    if heading.width > cfg.SAFE_WIDTH / 1.05:
        heading.scale_to_fit_width(cfg.SAFE_WIDTH / 1.05)
    shadow = heading.copy().set_color(color).set_opacity(0.22).set_stroke(width=0, background=True)
    shadow.scale(1.03).shift(DOWN * 0.07 + RIGHT * 0.05)
    shadow._is_decorative = True
    rule_half = min(heading.width * 0.48, 5.8)
    rule = Line(LEFT * rule_half, RIGHT * rule_half, color=cfg.CYAN, stroke_width=5)
    stack = VGroup(VGroup(shadow, heading), rule).arrange(DOWN, buff=0.26)
    if subtitle:
        sub = outlined_text(subtitle, cfg.FONT["body"], cfg.WHITE)
        if sub.width > cfg.SAFE_WIDTH - 0.6:
            sub.scale_to_fit_width(cfg.SAFE_WIDTH - 0.6)
        stack.add(sub)
        stack.arrange(DOWN, buff=0.26)
    return stack


def bottom_caption(text: str, color: str = cfg.GOLD) -> Text:
    caption = outlined_text(text, cfg.FONT["body"], color, BOLD)
    if caption.width > cfg.SAFE_WIDTH - 0.5:
        caption.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(DOWN, buff=0.38)


def top_caption(text: str, color: str = cfg.CYAN) -> Text:
    caption = outlined_text(text, cfg.FONT["body"], color, BOLD)
    if caption.width > cfg.SAFE_WIDTH - 0.5:
        caption.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(UP, buff=0.38)


def swap_caption(scene: Scene, current: Mobject | None, text: str, color: str = cfg.GOLD, run_time: float = 0.6) -> Text:
    """Replace the bottom caption without ever stacking two captions."""
    fresh = bottom_caption(text, color)
    if current is None:
        paced_play(scene, FadeIn(fresh, shift=UP * 0.15), run_time=run_time)
    else:
        paced_play(scene, FadeOut(current, shift=DOWN * 0.12), FadeIn(fresh, shift=UP * 0.12), run_time=run_time)
    return fresh


# ----------------------------------------------------------------------------
# Glow primitives
# ----------------------------------------------------------------------------


def glow_dot(point: Sequence[float], color: str = cfg.GOLD, radius: float = 0.09) -> VGroup:
    layers = VGroup()
    for size, opacity in ((0.28, 0.05), (0.20, 0.09), (0.14, 0.16)):
        layers.add(Circle(radius=size, color=color, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(point))
    layers.add(Dot(point, radius=radius, color=color))
    return layers


def glow_line(start: Sequence[float], end: Sequence[float], color: str, width: float = 5) -> VGroup:
    return VGroup(
        Line(start, end, color=color, stroke_width=width * 3.2, stroke_opacity=0.1),
        Line(start, end, color=color, stroke_width=width),
    )


def glow_curve(curve: VMobject, color: str = cfg.CYAN, width: float = 18) -> VGroup:
    return VGroup(curve.copy().set_stroke(color, width=width, opacity=0.1), curve)


def dashed_ring(
    center: Sequence[float],
    radius: float,
    color: str = cfg.GOLD,
    num_dashes: int = 14,
    stroke_width: float = 3,
) -> VGroup:
    """A dashed ring built from independent arcs.

    Avoids DashedVMobject, whose generated dashes can include a degenerate,
    zero-point sub-path that crashes rendering when the ring is later faded.
    """
    dash_angle = TAU / num_dashes * 0.6
    gap_angle = TAU / num_dashes - dash_angle
    ring = VGroup()
    for index in range(num_dashes):
        start = index * (dash_angle + gap_angle)
        ring.add(
            Arc(
                radius=radius,
                start_angle=start,
                angle=dash_angle,
                arc_center=np.array(center),
                color=color,
                stroke_width=stroke_width,
            )
        )
    return ring


def check_mark(color: str = cfg.GREEN, scale: float = 1.0) -> VGroup:
    stroke = VMobject(color=color, stroke_width=12)
    stroke.set_points_as_corners([np.array([-0.34, 0.02, 0]), np.array([-0.08, -0.28, 0]), np.array([0.38, 0.34, 0])])
    halo = stroke.copy().set_stroke(color, width=30, opacity=0.12)
    return VGroup(halo, stroke).scale(scale)


def cross_mark(color: str = cfg.RED, scale: float = 1.0) -> VGroup:
    first = Line([-0.32, -0.32, 0], [0.32, 0.32, 0], color=color, stroke_width=12)
    second = Line([-0.32, 0.32, 0], [0.32, -0.32, 0], color=color, stroke_width=12)
    halo = VGroup(first.copy(), second.copy()).set_stroke(color, width=30, opacity=0.12)
    return VGroup(halo, first, second).scale(scale)


def verdict_badge(label: str, ok: bool, scale: float = 1.0) -> VGroup:
    color = cfg.GREEN if ok else cfg.RED
    mark = check_mark(color) if ok else cross_mark(color)
    text = outlined_text(label, cfg.FONT["label"], color)
    return VGroup(mark, text).arrange(RIGHT, buff=0.28).scale(scale)


def boxed_statement(text: str, color: str = cfg.GOLD, font_size: int | None = None, tex: bool = False) -> VGroup:
    """A short, emphatic conclusion inside a glowing frame."""
    content = eq(text, color, font_size or cfg.FONT["section"]) if tex else outlined_text(text, font_size or cfg.FONT["body"], color)
    max_width = cfg.SAFE_WIDTH - 1.6
    if content.width > max_width:
        content.scale_to_fit_width(max_width)
    box = RoundedRectangle(
        width=content.width + 0.9,
        height=content.height + 0.62,
        corner_radius=0.2,
        stroke_color=color,
        stroke_width=4,
        stroke_opacity=0.8,
        fill_color=cfg.PANEL,
        fill_opacity=0.9,
    )
    halo = box.copy().set_stroke(color, width=18, opacity=0.09).set_fill(opacity=0)
    return VGroup(halo, box, content.move_to(box.get_center()))


# ----------------------------------------------------------------------------
# The machine metaphor
# ----------------------------------------------------------------------------


def machine(
    label: str,
    color: str = cfg.RULE_COLOR,
    width: float = 3.4,
    height: float = 2.2,
    *,
    tex: bool = False,
    font_size: int | None = None,
    icon: Mobject | None = None,
) -> VGroup:
    """A glowing rounded box: the film's single, repeated picture of a rule."""
    body = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.24,
        stroke_color=color,
        stroke_width=5,
        fill_color=cfg.PANEL,
        fill_opacity=0.94,
    )
    halo = body.copy().set_stroke(color, width=22, opacity=0.1).set_fill(opacity=0)
    inner = RoundedRectangle(
        width=width - 0.26,
        height=height - 0.26,
        corner_radius=0.17,
        stroke_color=color,
        stroke_width=1.8,
        stroke_opacity=0.4,
        fill_opacity=0,
    )
    text = eq(label, cfg.WHITE, font_size or cfg.FONT["body"]) if tex else outlined_text(label, font_size or cfg.FONT["label"], cfg.WHITE)
    group = VGroup(halo, body, inner)
    if icon is not None:
        icon.scale_to_fit_height(min(height * 0.62, 1.9))
        contents = VGroup(icon, text).arrange(DOWN, buff=0.22)
    else:
        contents = VGroup(text)
    if contents.width > width - 0.44:
        contents.scale_to_fit_width(width - 0.44)
    contents.move_to(body.get_center())
    group.add(contents)
    group.body = body
    group.halo = halo
    group.label = text
    group.contents = contents
    return group


def token(
    label: str,
    color: str = cfg.INPUT_COLOR,
    *,
    tex: bool = True,
    font_size: int | None = None,
) -> VGroup:
    """A value in flight: a glowing pill that enters or leaves a machine."""
    content = eq(label, color, font_size or cfg.FONT["body"]) if tex else outlined_text(label, font_size or cfg.FONT["label"], color)
    width = max(content.width + 0.62, 1.15)
    height = max(content.height + 0.5, 0.95)
    pill = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=min(0.24, height / 2 - 0.02),
        stroke_color=color,
        stroke_width=3.5,
        fill_color=color,
        fill_opacity=0.14,
    )
    glow = pill.copy().set_stroke(color, width=16, opacity=0.13).set_fill(opacity=0)
    group = VGroup(glow, pill, content.move_to(pill.get_center()))
    group.content = content
    group.pill = pill
    return group


def icon_token(
    icon: Mobject,
    label: str,
    color: str = cfg.INPUT_COLOR,
    *,
    tex: bool = True,
    font_size: int | None = None,
) -> VGroup:
    """A value in flight that carries a picture as well as its name."""
    text = eq(label, color, font_size or cfg.FONT["label"]) if tex else outlined_text(label, font_size or cfg.FONT["small"], color)
    icon.scale_to_fit_height(0.86)
    stack = VGroup(icon, text).arrange(DOWN, buff=0.16)
    pill = RoundedRectangle(
        width=max(stack.width + 0.6, 1.5),
        height=stack.height + 0.5,
        corner_radius=0.22,
        stroke_color=color,
        stroke_width=3.5,
        fill_color=color,
        fill_opacity=0.14,
    )
    glow = pill.copy().set_stroke(color, width=16, opacity=0.13).set_fill(opacity=0)
    group = VGroup(glow, pill, stack.move_to(pill.get_center()))
    group.content = stack
    group.pill = pill
    return group


def flow_arrow(start: Sequence[float], end: Sequence[float], color: str = cfg.RULE_COLOR, width: float = 6) -> VGroup:
    arrow = Arrow(
        np.array(start),
        np.array(end),
        color=color,
        stroke_width=width,
        buff=0.0,
        max_tip_length_to_length_ratio=0.3,
        tip_length=0.28,
    )
    glow = arrow.copy().set_stroke(color, width=width * 3.0, opacity=0.12)
    return VGroup(glow, arrow)


def connect(left: Mobject, right: Mobject, color: str = cfg.RULE_COLOR, buff: float = 0.22, width: float = 6) -> VGroup:
    """A flow arrow from the right edge of one mobject to the left edge of another."""
    start = left.get_right() + RIGHT * buff
    end = right.get_left() + LEFT * buff
    if end[0] - start[0] < 0.18:
        end = start + RIGHT * 0.18
    return flow_arrow(start, end, color, width)


def feed_machine(
    scene: Scene,
    mach: VGroup,
    in_token: Mobject,
    out_token: Mobject,
    *,
    run_time: float = 1.8,
    pulse_color: str = cfg.WHITE,
) -> None:
    """Swallow a value, flash the rule, and let the answer emerge on the far side."""
    scene.play(
        in_token.animate.move_to(mach.body.get_center()).scale(0.4).set_opacity(0.0),
        run_time=run_time * 0.42,
        rate_func=rate_functions.ease_in_quad,
    )
    scene.remove(in_token)
    scene.play(
        Indicate(mach.body, color=pulse_color, scale_factor=1.05),
        Indicate(mach.halo, color=pulse_color, scale_factor=1.05),
        run_time=run_time * 0.24,
    )
    out_token.save_state()
    out_token.move_to(mach.body.get_center()).scale(0.4).set_opacity(0.0)
    scene.add(out_token)
    scene.play(Restore(out_token), run_time=run_time * 0.34, rate_func=rate_functions.ease_out_quad)


def value_flight(scene: Scene, mob: Mobject, target, run_time: float = 0.8) -> None:
    """Move a value along a gentle arc, so numbers feel like they travel."""
    scene.play(mob.animate.move_to(target), run_time=run_time, path_arc=-0.35)


# ----------------------------------------------------------------------------
# Sets, mappings, axes
# ----------------------------------------------------------------------------


def oval_set(
    labels: Sequence[str],
    color: str,
    *,
    title: str | None = None,
    width: float = 2.5,
    height: float = 4.2,
    font_size: int | None = None,
    slots: int | None = None,
) -> VGroup:
    """An ellipse of stacked values, used for mapping diagrams.

    Slot centres are computed from geometry, not from the glyphs, so a set can
    reserve room for a value that only appears later: pass ``slots`` larger than
    ``labels`` and read the spare position off ``group.slot_points``.
    """
    count = max(slots or len(labels), len(labels), 1)
    ring = Ellipse(width=width, height=height, color=color, stroke_width=4, fill_color=cfg.PANEL, fill_opacity=0.55)
    halo = ring.copy().set_stroke(color, width=18, opacity=0.08).set_fill(opacity=0)
    usable = max(height - 1.5, 0.6)
    spacing = usable / (count - 1) if count > 1 else 0.0
    slot_points = [
        ring.get_center() + UP * ((count - 1) / 2 - index) * spacing
        for index in range(count)
    ]
    items = VGroup()
    for index, text in enumerate(labels):
        item = eq(text, cfg.WHITE, font_size or cfg.FONT["section"])
        item.move_to(slot_points[index])
        items.add(item)
    group = VGroup(halo, ring, items)
    if title is not None:
        cap = outlined_text(title, cfg.FONT["label"], color)
        cap.next_to(ring, UP, buff=0.24)
        group.add(cap)
        group.title = cap
    group.ring = ring
    group.items = items
    group.slot_points = slot_points
    return group


def map_arrow(source: Mobject, target: Mobject, color: str = cfg.RULE_COLOR, width: float = 5) -> VGroup:
    return flow_arrow(source.get_right() + RIGHT * 0.28, target.get_left() + LEFT * 0.28, color, width)


def fn_axes(
    x_range: Sequence[float] = (-4, 4, 1),
    y_range: Sequence[float] = (-1, 6, 1),
    x_length: float = 7.4,
    y_length: float = 5.4,
) -> Axes:
    return Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.6, "include_ticks": True},
    )


def axis_labels(axes: Axes, x_tex: str = "x", y_tex: str = "f(x)", font_size: int | None = None) -> VGroup:
    size = font_size or cfg.FONT["section"]
    x_label = eq(x_tex, cfg.MUTED, size).next_to(axes.x_axis.get_right(), UP, buff=0.16)
    y_label = eq(y_tex, cfg.MUTED, size).next_to(axes.y_axis.get_top(), RIGHT, buff=0.16)
    return VGroup(x_label, y_label)


def value_table(
    rows: Sequence[tuple[str, str]],
    *,
    head_left: str = "x",
    head_right: str = "f(x)",
    font_size: int | None = None,
    row_buff: float = 0.34,
    col_buff: float = 1.15,
) -> VGroup:
    """A hand-built input/output table, so every row stays individually animatable."""
    size = font_size or cfg.FONT["body"]
    left_head = eq(head_left, cfg.INPUT_COLOR, size)
    right_head = eq(head_right, cfg.OUTPUT_COLOR, size)
    header = VGroup(left_head, right_head).arrange(RIGHT, buff=col_buff)
    body_rows = VGroup()
    for left_text, right_text in rows:
        left = eq(left_text, cfg.INPUT_COLOR, size)
        right = eq(right_text, cfg.OUTPUT_COLOR, size)
        left.move_to(left_head.get_center())
        right.move_to(right_head.get_center())
        row = VGroup(left, right)
        row.left_cell = left
        row.right_cell = right
        body_rows.add(row)
    body_rows.arrange(DOWN, buff=row_buff)
    body_rows.next_to(header, DOWN, buff=row_buff + 0.16)
    rule = Line(LEFT, RIGHT, color=cfg.MUTED, stroke_width=3)
    rule.set_length(max(header.width + 0.5, 2.0))
    rule.next_to(header, DOWN, buff=row_buff * 0.5)
    divider = Line(UP, DOWN, color=cfg.MUTED, stroke_width=2.2, stroke_opacity=0.6)
    group = VGroup(header, rule, body_rows)
    divider.set_length(group.height + 0.2)
    divider.move_to([header.get_center()[0], group.get_center()[1], 0])
    group.add(divider)
    group.header = header
    group.rows = body_rows
    group.rule = rule
    return group


# ----------------------------------------------------------------------------
# Everyday-object icons for the opening chapter
# ----------------------------------------------------------------------------


def vending_machine_icon(color: str = cfg.CYAN, scale: float = 1.0) -> VGroup:
    shell = RoundedRectangle(width=1.35, height=2.0, corner_radius=0.12, color=color, stroke_width=3.5, fill_color=cfg.PANEL_2, fill_opacity=0.95)
    window = RoundedRectangle(width=0.74, height=1.16, corner_radius=0.07, color=cfg.MUTED, stroke_width=2, fill_color="#06283F", fill_opacity=1)
    window.move_to(shell.get_center() + UP * 0.32 + LEFT * 0.24)
    cans = VGroup()
    for row in range(3):
        for col in range(2):
            can = RoundedRectangle(width=0.16, height=0.24, corner_radius=0.05, color=cfg.GOLD, stroke_width=1.4, fill_color=cfg.GOLD, fill_opacity=0.55)
            can.move_to(RIGHT * 0.32 * col + DOWN * 0.34 * row)
            cans.add(can)
    cans.move_to(window.get_center())
    keypad = VGroup(*[Dot(radius=0.035, color=cfg.CYAN) for _ in range(6)])
    keypad.arrange_in_grid(rows=3, cols=2, buff=0.11)
    keypad.move_to(shell.get_center() + RIGHT * 0.44 + UP * 0.36)
    tray = RoundedRectangle(width=0.9, height=0.34, corner_radius=0.06, color=cfg.MUTED, stroke_width=2, fill_color="#06283F", fill_opacity=1)
    tray.move_to(shell.get_center() + DOWN * 0.66)
    return VGroup(shell, window, cans, keypad, tray).scale(scale)


def thermometer_icon(color: str = cfg.RED, scale: float = 1.0) -> VGroup:
    tube = RoundedRectangle(width=0.34, height=1.5, corner_radius=0.17, color=cfg.MUTED, fill_color=cfg.PANEL_2, fill_opacity=0.95, stroke_width=2.6)
    tube.shift(UP * 0.35)
    bulb = Circle(radius=0.27, color=cfg.MUTED, fill_color=cfg.PANEL_2, fill_opacity=0.95, stroke_width=2.6).shift(DOWN * 0.55)
    fill_tube = RoundedRectangle(width=0.15, height=1.0, corner_radius=0.07, color=color, fill_color=color, fill_opacity=1, stroke_width=0)
    fill_tube.move_to(tube.get_center() + DOWN * 0.08)
    fill_bulb = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=1, stroke_width=0).move_to(bulb.get_center())
    ticks = VGroup()
    for index in range(4):
        ticks.add(Line(LEFT * 0.1, RIGHT * 0.1, color=cfg.MUTED, stroke_width=2).move_to(tube.get_center() + UP * (0.5 - 0.3 * index) + LEFT * 0.26))
    return VGroup(tube, bulb, fill_tube, fill_bulb, ticks).scale(scale)


def navigation_icon(color: str = cfg.GREEN, scale: float = 1.0) -> VGroup:
    board = RoundedRectangle(width=1.8, height=1.55, corner_radius=0.12, color=cfg.MUTED, stroke_width=2.6, fill_color=cfg.PANEL_2, fill_opacity=0.95)
    route = VMobject(color=color, stroke_width=6)
    route.set_points_smoothly(
        [
            np.array([-0.62, -0.5, 0]),
            np.array([-0.18, -0.06, 0]),
            np.array([0.16, 0.2, 0]),
            np.array([0.58, 0.46, 0]),
        ]
    )
    start = Dot(np.array([-0.62, -0.5, 0]), radius=0.08, color=cfg.CYAN)
    pin_head = Circle(radius=0.13, color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=1, stroke_width=0)
    pin_head.move_to(np.array([0.58, 0.54, 0]))
    pin_tip = Triangle(color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI)
    pin_tip.next_to(pin_head, DOWN, buff=-0.03)
    return VGroup(board, route, start, pin_head, pin_tip).scale(scale)


def neural_icon(color: str = cfg.PURPLE, scale: float = 1.0, layers: Sequence[int] = (3, 4, 2)) -> VGroup:
    columns = VGroup()
    for index, count in enumerate(layers):
        column = VGroup(*[Dot(radius=0.075, color=color) for _ in range(count)])
        column.arrange(DOWN, buff=0.24)
        column.move_to(RIGHT * 0.72 * index)
        columns.add(column)
    edges = VGroup()
    for left_col, right_col in zip(columns[:-1], columns[1:]):
        for source in left_col:
            for target in right_col:
                edges.add(Line(source.get_center(), target.get_center(), color=color, stroke_width=1.4, stroke_opacity=0.4))
    return VGroup(edges, columns).center().scale(scale)


def cat_icon(color: str = cfg.GOLD, scale: float = 1.0) -> VGroup:
    head = Circle(radius=0.42, color=color, stroke_width=4, fill_color=color, fill_opacity=0.14)
    left_ear = Triangle(color=color, stroke_width=4, fill_color=color, fill_opacity=0.14).scale(0.19)
    left_ear.move_to(head.get_center() + LEFT * 0.27 + UP * 0.42)
    right_ear = left_ear.copy().move_to(head.get_center() + RIGHT * 0.27 + UP * 0.42)
    left_eye = Dot(head.get_center() + LEFT * 0.15 + UP * 0.06, radius=0.05, color=color)
    right_eye = Dot(head.get_center() + RIGHT * 0.15 + UP * 0.06, radius=0.05, color=color)
    nose = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.05).rotate(PI)
    nose.move_to(head.get_center() + DOWN * 0.1)
    whiskers = VGroup()
    for side in (-1, 1):
        for offset in (-0.06, 0.06):
            whiskers.add(
                Line(
                    head.get_center() + RIGHT * side * 0.14 + DOWN * 0.1 + UP * offset,
                    head.get_center() + RIGHT * side * 0.55 + DOWN * 0.06 + UP * offset * 2,
                    color=color,
                    stroke_width=2.2,
                    stroke_opacity=0.8,
                )
            )
    return VGroup(head, left_ear, right_ear, left_eye, right_eye, nose, whiskers).scale(scale)


def coin_icon(color: str = cfg.GOLD, scale: float = 1.0) -> VGroup:
    outer = Circle(radius=0.36, color=color, stroke_width=4, fill_color=color, fill_opacity=0.18)
    inner = Circle(radius=0.27, color=color, stroke_width=2, stroke_opacity=0.6)
    mark = eq(r"\$", color, cfg.FONT["label"]).move_to(outer.get_center())
    return VGroup(outer, inner, mark).scale(scale)
