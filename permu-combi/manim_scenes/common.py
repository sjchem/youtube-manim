"""Shared visual language for the Permutations & Combinations film.

One grammar runs through every chapter, so a viewer can read the mathematics
straight off the screen:

* an object is always a glowing disc (a **chip**);
* a chip that is still available glows cyan, a chosen chip turns gold,
  and a spent chip fades to grey;
* a position you can fill is always an empty square (a **slot**);
* when order matters the slots are numbered and orange;
* when order does not matter the chips collapse inside one green ring.

Nothing in a scene file should invent a second way of drawing these ideas.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg
from utils.render_helpers import fit_to_safe_frame, fit_width

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
        raise ValueError(
            f"Scene {key} exceeds its target by {-remaining_frames / fps:.2f}s; retime its beats."
        )
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


def cue(scene: Scene, started_at: float, seconds: float) -> None:
    """Hold until a named second inside the chapter, and refuse to run past it."""
    remaining = seconds - (float(scene.time) - started_at)
    key = getattr(scene, "_project_scene_key", "unknown")
    if remaining < -0.14:
        raise ValueError(f"Scene {key} cue {seconds}s overrun by {-remaining:.2f}s")
    if remaining > 1e-6:
        narration_wait(scene, remaining)


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
    color: str = cfg.RESULT,
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
    fit_width(heading, cfg.SAFE_WIDTH / 1.05)
    shadow = heading.copy().set_color(color).set_opacity(0.22).set_stroke(width=0, background=True)
    shadow.scale(1.03).shift(DOWN * 0.07 + RIGHT * 0.05)
    shadow._is_decorative = True
    rule_half = min(heading.width * 0.48, 5.8)
    rule = Line(LEFT * rule_half, RIGHT * rule_half, color=cfg.CYAN, stroke_width=5)
    stack = VGroup(VGroup(shadow, heading), rule).arrange(DOWN, buff=0.26)
    if subtitle:
        sub = fit_width(outlined_text(subtitle, cfg.FONT["body"], cfg.WHITE), cfg.SAFE_WIDTH - 0.6)
        stack.add(sub)
        stack.arrange(DOWN, buff=0.26)
    return fit_to_safe_frame(stack)


def bottom_caption(text: str, color: str = cfg.GOLD) -> Text:
    caption = fit_width(outlined_text(text, cfg.FONT["body"], color, BOLD), cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(DOWN, buff=0.38)


def top_caption(text: str, color: str = cfg.CYAN) -> Text:
    caption = fit_width(outlined_text(text, cfg.FONT["body"], color, BOLD), cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(UP, buff=0.38)


def swap_caption(
    scene: Scene,
    current: Mobject | None,
    text: str,
    color: str = cfg.GOLD,
    run_time: float = 0.6,
    *,
    top: bool = False,
) -> Text:
    """Replace a caption without ever stacking two captions in the same band."""
    fresh = top_caption(text, color) if top else bottom_caption(text, color)
    if current is None:
        paced_play(scene, FadeIn(fresh, shift=UP * 0.15), run_time=run_time)
    else:
        paced_play(scene, FadeOut(current, shift=DOWN * 0.12), FadeIn(fresh, shift=UP * 0.12), run_time=run_time)
    return fresh


# ----------------------------------------------------------------------------
# Glow primitives
# ----------------------------------------------------------------------------


def glow_dot(point: Sequence[float], color: str = cfg.CHOSEN, radius: float = 0.09) -> VGroup:
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


def dashed_ring(
    center: Sequence[float],
    radius: float,
    color: str = cfg.CHOSEN,
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


def boxed_statement(
    text: str,
    color: str = cfg.GOLD,
    font_size: int | None = None,
    tex: bool = False,
    *,
    max_width: float | None = None,
) -> VGroup:
    """A short, emphatic conclusion inside a glowing frame."""
    content = (
        eq(text, color, font_size or cfg.FONT["section"])
        if tex
        else outlined_text(text, font_size or cfg.FONT["body"], color)
    )
    fit_width(content, (max_width or cfg.SAFE_WIDTH) - 1.6)
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
    group = VGroup(halo, box, content.move_to(box.get_center()))
    group.box = box
    group.content = content
    return group


# ----------------------------------------------------------------------------
# The chip: one object you can choose
# ----------------------------------------------------------------------------


def chip(
    label: str,
    color: str = cfg.AVAILABLE,
    radius: float = 0.52,
    *,
    font_size: int | None = None,
    tex: bool = False,
) -> VGroup:
    """A glowing disc carrying a name: the film's picture of one object."""
    halo = Circle(radius=radius * 1.34, color=color, stroke_width=0, fill_color=color, fill_opacity=0.10)
    disc = Circle(
        radius=radius,
        color=color,
        stroke_width=5,
        fill_color=cfg.PANEL,
        fill_opacity=0.96,
    )
    size = font_size or int(radius * 92)
    text = eq(label, color, size) if tex else outlined_text(label, size, color)
    if text.width > radius * 1.5:
        text.scale_to_fit_width(radius * 1.5)
    text.move_to(disc.get_center())
    group = VGroup(halo, disc, text)
    group.halo = halo
    group.disc = disc
    group.label = text
    group.chip_color = color
    return group


def recolor_chip(item: VGroup, color: str, *, fill_opacity: float = 0.10) -> VGroup:
    """Repaint a chip in place, keeping the halo/disc/label relationship intact."""
    item.halo.set_fill(color, opacity=fill_opacity).set_stroke(width=0)
    item.disc.set_stroke(color)
    item.label.set_color(color)
    item.chip_color = color
    return item


def chip_target(item: VGroup, color: str, *, fill_opacity: float = 0.10) -> VGroup:
    """A recoloured copy, for use as a Transform target."""
    return recolor_chip(item.copy(), color, fill_opacity=fill_opacity)


def dim_chip(item: VGroup) -> VGroup:
    """The 'already used, no longer available' state."""
    ghost = chip_target(item, cfg.SPENT, fill_opacity=0.04)
    ghost.set_opacity(0.38)
    ghost.disc.set_fill(cfg.BG, opacity=0.6)
    return ghost


def chip_row(
    labels: Sequence[str],
    color: str = cfg.AVAILABLE,
    *,
    buff: float = 0.42,
    radius: float = 0.52,
    center: Sequence[float] | None = None,
) -> VGroup:
    """The pool of available objects, always drawn as one horizontal row."""
    row = VGroup(*[chip(text, color, radius) for text in labels])
    row.arrange(RIGHT, buff=buff)
    if center is not None:
        row.move_to(np.array(center))
    return row


# ----------------------------------------------------------------------------
# The slot: one position you can fill
# ----------------------------------------------------------------------------


def slot(
    rank: str | None = None,
    *,
    size: float = 1.26,
    color: str | None = None,
    rank_color: str | None = None,
) -> VGroup:
    """An empty position. A ranked slot carries its place number underneath."""
    frame_color = color or (cfg.ORDERED if rank else cfg.MUTED)
    body = RoundedRectangle(
        width=size,
        height=size,
        corner_radius=0.16,
        stroke_color=frame_color,
        stroke_width=4,
        fill_color=cfg.PANEL,
        fill_opacity=0.55,
    )
    body.set_stroke(opacity=0.85)
    halo = body.copy().set_stroke(frame_color, width=16, opacity=0.0).set_fill(opacity=0)
    group = VGroup(halo, body)
    if rank is not None:
        tag = outlined_text(rank, cfg.FONT["small"], frame_color)
        tag.next_to(body, DOWN, buff=0.2)
        group.add(tag)
        group.tag = tag
    group.body = body
    group.halo = halo
    group.slot_color = frame_color
    return group


def slot_row(
    count: int,
    *,
    ranks: Sequence[str] | None = None,
    size: float = 1.26,
    buff: float = 0.36,
    color: str | None = None,
    center: Sequence[float] | None = None,
) -> VGroup:
    """A row of positions. Pass ``ranks`` when the order of the slots matters."""
    slots = VGroup(
        *[
            slot(ranks[index] if ranks else None, size=size, color=color)
            for index in range(count)
        ]
    )
    slots.arrange(RIGHT, buff=buff, aligned_edge=UP)
    if center is not None:
        slots.move_to(np.array(center))
    return slots


def glow_slot(scene: Scene, target: VGroup, color: str | None = None, run_time: float = 0.5) -> None:
    """Light up the slot we are about to fill."""
    shade = color or cfg.CHOSEN
    paced_play(
        scene,
        target.halo.animate.set_stroke(shade, width=20, opacity=0.35),
        target.body.animate.set_stroke(shade, width=6),
        run_time=run_time,
    )


def place_chip(
    scene: Scene,
    item: VGroup,
    target: VGroup,
    *,
    run_time: float = 0.75,
    color: str = cfg.CHOSEN,
    arc: float = -0.5,
) -> VGroup:
    """Fly a chip out of the pool and seat it inside a slot."""
    landed = chip_target(item, color)
    landed.move_to(target.body.get_center())
    if landed.disc.radius * 2.6 > target.body.width:
        landed.scale_to_fit_height(target.body.height * 0.86)
    scene.play(Transform(item, landed, path_arc=arc), run_time=run_time)
    return item


# ----------------------------------------------------------------------------
# The ring: a group in which order has stopped mattering
# ----------------------------------------------------------------------------


def team_ring(
    radius: float = 1.55,
    color: str = cfg.UNORDERED,
    center: Sequence[float] | None = None,
    *,
    label: str | None = None,
) -> VGroup:
    """One glowing enclosure. Inside it, position carries no meaning."""
    ring = Circle(radius=radius, color=color, stroke_width=5, fill_color=color, fill_opacity=0.07)
    halo = Circle(radius=radius * 1.06, color=color, stroke_width=22, stroke_opacity=0.10, fill_opacity=0)
    group = VGroup(halo, ring)
    if center is not None:
        group.move_to(np.array(center))
    if label is not None:
        tag = outlined_text(label, cfg.FONT["small"], color)
        tag.next_to(ring, DOWN, buff=0.26)
        group.add(tag)
        group.tag = tag
    group.ring = ring
    group.halo = halo
    return group


def ring_points(ring: VGroup, count: int, radius_scale: float = 0.56) -> list[np.ndarray]:
    """Evenly spaced seats inside a ring, starting at the top."""
    centre = ring.ring.get_center()
    r = ring.ring.width / 2 * radius_scale
    if count == 1:
        return [centre]
    return [
        centre + r * np.array([np.sin(TAU * i / count), np.cos(TAU * i / count), 0.0])
        for i in range(count)
    ]


def shuffle_inside_ring(scene: Scene, chips: Sequence[VGroup], seats: Sequence[np.ndarray], run_time: float = 1.1) -> None:
    """Rotate the chips between their seats: the picture of 'nothing changed'."""
    order = list(range(len(chips)))
    rotated = order[1:] + order[:1]
    scene.play(
        *[chips[i].animate.move_to(seats[rotated[i]]) for i in order],
        run_time=run_time,
        path_arc=PI / 2,
    )


# ----------------------------------------------------------------------------
# Building an equation the same way the animation built the count
# ----------------------------------------------------------------------------


class ProductChain(VGroup):
    """A product revealed one factor at a time, exactly as the choices appear."""

    def __init__(
        self,
        factors: Sequence[int | str],
        color: str = cfg.CHOSEN,
        font_size: int | None = None,
        *,
        separator: str = r"\times",
    ) -> None:
        super().__init__()
        size = font_size or cfg.FONT["title"]
        self.steps: list[VGroup] = []
        self.terms: list[MathTex] = []
        for index, value in enumerate(factors):
            step = VGroup()
            if index:
                step.add(eq(separator, cfg.MUTED, size))
            term = eq(str(value), color, size)
            step.add(term)
            step.arrange(RIGHT, buff=0.2)
            self.terms.append(term)
            self.steps.append(step)
            self.add(step)
        self.arrange(RIGHT, buff=0.2)

    def reveal(self, scene: Scene, index: int, run_time: float = 0.55) -> VGroup:
        step = self.steps[index]
        paced_play(scene, FadeIn(step, shift=UP * 0.18), run_time=run_time)
        return step

    def tail(self, start: int) -> VGroup:
        """The factors from ``start`` onwards, for greying out or dividing away."""
        return VGroup(*self.steps[start:])


def equals_result(chain: VGroup, value: str, color: str = cfg.RESULT, font_size: int | None = None) -> VGroup:
    """`= 24` placed after a product, ready to fade in on its own beat."""
    size = font_size or cfg.FONT["title"]
    tail = VGroup(eq("=", cfg.MUTED, size), eq(value, color, size)).arrange(RIGHT, buff=0.24)
    tail.next_to(chain, RIGHT, buff=0.3)
    return tail


def formula_panel(latex: str, color: str = cfg.GOLD, font_size: int | None = None) -> VGroup:
    """A boxed general formula: the compressed version of what was just shown."""
    return boxed_statement(latex, color, font_size or cfg.FONT["title"], tex=True)


# ----------------------------------------------------------------------------
# Everyday icons, drawn procedurally so the film needs no image assets
# ----------------------------------------------------------------------------


def shirt_icon(color: str = cfg.RED, scale: float = 1.0) -> VGroup:
    body = Polygon(
        [-0.42, 0.42, 0], [-0.18, 0.56, 0], [0.18, 0.56, 0], [0.42, 0.42, 0],
        [0.68, 0.16, 0], [0.44, -0.06, 0], [0.42, -0.6, 0], [-0.42, -0.6, 0],
        [-0.44, -0.06, 0], [-0.68, 0.16, 0],
        color=color, stroke_width=4, fill_color=color, fill_opacity=0.28,
    )
    collar = ArcBetweenPoints([-0.18, 0.56, 0], [0.18, 0.56, 0], angle=-PI * 0.8, color=color, stroke_width=3.5)
    return VGroup(body, collar).scale(scale)


def trouser_icon(color: str = cfg.GRAY, scale: float = 1.0) -> VGroup:
    body = Polygon(
        [-0.34, 0.6, 0], [0.34, 0.6, 0], [0.34, -0.66, 0], [0.09, -0.66, 0],
        [0.0, 0.06, 0], [-0.09, -0.66, 0], [-0.34, -0.66, 0],
        color=color, stroke_width=4, fill_color=color, fill_opacity=0.3,
    )
    belt = Line([-0.34, 0.46, 0], [0.34, 0.46, 0], color=color, stroke_width=3.5, stroke_opacity=0.7)
    return VGroup(body, belt).scale(scale)


def book_icon(color: str = cfg.CYAN, scale: float = 1.0, title: str | None = None) -> VGroup:
    cover = RoundedRectangle(
        width=0.62, height=1.5, corner_radius=0.06,
        color=color, stroke_width=4, fill_color=color, fill_opacity=0.24,
    )
    spine = Line(cover.get_corner(UL) + RIGHT * 0.13, cover.get_corner(DL) + RIGHT * 0.13, color=color, stroke_width=3)
    bands = VGroup(
        *[
            Line(LEFT * 0.14, RIGHT * 0.14, color=color, stroke_width=2.6, stroke_opacity=0.65)
            .move_to(cover.get_center() + UP * offset + RIGHT * 0.1)
            for offset in (0.34, 0.2)
        ]
    )
    group = VGroup(cover, spine, bands)
    if title:
        tag = outlined_text(title, 34, color)
        tag.move_to(cover.get_center() + DOWN * 0.18 + RIGHT * 0.08)
        group.add(tag)
    group.cover = cover
    return group.scale(scale)


def person_icon(color: str = cfg.CYAN, scale: float = 1.0, name: str | None = None) -> VGroup:
    head = Circle(radius=0.2, color=color, stroke_width=4, fill_color=color, fill_opacity=0.3)
    head.shift(UP * 0.52)
    body = Polygon(
        [-0.3, 0.2, 0], [0.3, 0.2, 0], [0.24, -0.62, 0], [-0.24, -0.62, 0],
        color=color, stroke_width=4, fill_color=color, fill_opacity=0.22,
    )
    body.round_corners(radius=0.1)
    group = VGroup(head, body)
    if name:
        tag = outlined_text(name, 34, color)
        tag.next_to(body, DOWN, buff=0.16)
        group.add(tag)
        group.tag = tag
    group.head = head
    group.body = body
    return group.scale(scale)


def medal_icon(rank: str, color: str, scale: float = 1.0) -> VGroup:
    ribbon = VGroup(
        Polygon([-0.2, 0.62, 0], [-0.05, 0.62, 0], [-0.02, 0.16, 0], [-0.24, 0.2, 0],
                color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.45),
        Polygon([0.2, 0.62, 0], [0.05, 0.62, 0], [0.02, 0.16, 0], [0.24, 0.2, 0],
                color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.45),
    )
    disc = Circle(radius=0.32, color=color, stroke_width=4, fill_color=color, fill_opacity=0.35)
    disc.shift(DOWN * 0.12)
    mark = outlined_text(rank, 32, cfg.WHITE).move_to(disc.get_center())
    halo = Circle(radius=0.44, color=color, stroke_width=0, fill_color=color, fill_opacity=0.10).move_to(disc)
    return VGroup(halo, ribbon, disc, mark).scale(scale)


def lock_icon(color: str = cfg.CYAN, scale: float = 1.0, *, open_shackle: bool = False) -> VGroup:
    body = RoundedRectangle(
        width=1.6, height=1.25, corner_radius=0.16,
        color=color, stroke_width=4.5, fill_color=cfg.PANEL_2, fill_opacity=0.95,
    )
    shackle = Arc(radius=0.46, start_angle=0, angle=PI, color=color, stroke_width=8)
    shackle.next_to(body, UP, buff=-0.06)
    if open_shackle:
        shackle.shift(UP * 0.3 + RIGHT * 0.34).rotate(-0.5, about_point=shackle.get_bottom())
    keyhole = VGroup(
        Circle(radius=0.12, color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.35),
        Polygon([-0.06, -0.04, 0], [0.06, -0.04, 0], [0.04, -0.3, 0], [-0.04, -0.3, 0],
                color=color, stroke_width=3, fill_color=color, fill_opacity=0.35),
    )
    keyhole.move_to(body.get_center() + UP * 0.06)
    group = VGroup(body, shackle, keyhole)
    group.body = body
    group.shackle = shackle
    return group.scale(scale)


def playing_card(
    rank: str,
    suit: str,
    *,
    red: bool = False,
    width: float = 0.92,
    height: float = 1.32,
) -> VGroup:
    """A small, readable card face used for the poker-hand chapter."""
    # Black suits need an ink colour, not the palette white: the face is near-white.
    colour = cfg.RED if red else "#16222E"
    face = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        stroke_color=cfg.MUTED, stroke_width=2.6,
        fill_color="#F2F7FB", fill_opacity=1,
    )
    corner = Text(rank, font_size=26, color=colour, weight=BOLD)
    corner.move_to(face.get_corner(UL) + RIGHT * width * 0.22 + DOWN * height * 0.17)
    pip = Text(suit, font_size=44, color=colour)
    pip.move_to(face.get_center() + DOWN * height * 0.06)
    group = VGroup(face, corner, pip)
    group.face = face
    return group


def card_back(width: float = 0.92, height: float = 1.32, color: str = cfg.BLUE) -> VGroup:
    face = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        stroke_color=color, stroke_width=2.4, fill_color="#0B3B63", fill_opacity=1,
    )
    inner = RoundedRectangle(
        width=width - 0.16, height=height - 0.16, corner_radius=0.07,
        stroke_color=color, stroke_width=1.6, stroke_opacity=0.7, fill_opacity=0,
    )
    return VGroup(face, inner)


# ----------------------------------------------------------------------------
# Trees: the picture of 'choices multiply'
# ----------------------------------------------------------------------------


def branch_tree(
    root: Sequence[float],
    first_targets: Sequence[Sequence[float]],
    color: str = cfg.AVAILABLE,
    width: float = 4.0,
) -> VGroup:
    """Glowing edges from one node out to several children."""
    edges = VGroup()
    for target in first_targets:
        edges.add(glow_line(np.array(root), np.array(target), color, width))
    return edges
