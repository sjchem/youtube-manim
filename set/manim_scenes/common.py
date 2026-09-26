"""The one visual grammar the whole film speaks.

Every idea in set theory is drawn the same way from the first minute to the
last, so that De Morgan's laws arrive as a conclusion rather than a new topic:

* an **element** is a card with a drawing on it;
* the **universe** is the large rectangular board everything sits on;
* a **set** is a glowing boundary drawn on that board;
* ``x ∈ A`` is a card crossing a boundary;
* ``A ⊆ B`` is a whole boundary moving inside another boundary;
* a **union** floods both regions with light;
* an **intersection** spotlights only the overlap;
* a **complement** inverts the mask inside the universe;
* the **empty set** is a transparent boundary with nothing in it.

Nothing in a scene file should invent a second way of drawing these ideas.
The region masks are real path booleans, so the picture a scene highlights is
computed from the geometry — a scene cannot accidentally illuminate a region
that the algebra does not agree with.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg
from utils import math_utils as mu
from utils.render_helpers import fit_to_safe_frame, fit_width
from manim_scenes.icons import icon

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


def add_cinematic_background(scene: Scene, show_bubbles: bool = False) -> VGroup:
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
        font_size=min(font_size or cfg.FONT["section"], 72),
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
        sub = fit_width(outlined_text(subtitle, cfg.FONT["small"], cfg.WHITE), cfg.SAFE_WIDTH - 0.6)
        stack.add(sub)
        stack.arrange(DOWN, buff=0.26)
    return fit_to_safe_frame(stack)


def bottom_caption(text: str, color: str = cfg.GOLD) -> Text:
    caption = fit_width(outlined_text(text, cfg.FONT["small"], color, BOLD), cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(DOWN, buff=0.36)


def top_caption(text: str, color: str = cfg.CYAN) -> Text:
    caption = fit_width(outlined_text(text, cfg.FONT["small"], color, BOLD), cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(UP, buff=0.36)


def swap_caption(
    scene: Scene,
    current: Mobject | None,
    text: str | None,
    color: str = cfg.GOLD,
    run_time: float = 0.6,
    *,
    top: bool = False,
) -> Text | None:
    """Replace a caption without ever stacking two captions in the same band."""
    if text is None:
        if current is not None:
            paced_play(scene, FadeOut(current, shift=DOWN * 0.12), run_time=run_time)
        return None
    fresh = top_caption(text, color) if top else bottom_caption(text, color)
    if current is None:
        paced_play(scene, FadeIn(fresh, shift=UP * 0.15), run_time=run_time)
    else:
        paced_play(scene, FadeOut(current, shift=DOWN * 0.12), FadeIn(fresh, shift=UP * 0.12), run_time=run_time)
    return fresh


# ----------------------------------------------------------------------------
# Glow primitives
# ----------------------------------------------------------------------------


def glow_dot(point: Sequence[float], color: str = cfg.HIGHLIGHT, radius: float = 0.09) -> VGroup:
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
    color = cfg.INSIDE if ok else cfg.OUTSIDE
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
# The card: one object you can sort
# ----------------------------------------------------------------------------


def object_card(
    name: str,
    *,
    color: str = cfg.OBJECT,
    width: float = 1.24,
    height: float = 1.32,
    show_name: bool = False,
) -> VGroup:
    """One element of the universe, drawn as a physical card with a picture."""
    face = RoundedRectangle(
        width=width, height=height, corner_radius=0.16,
        stroke_color=color, stroke_width=3.4,
        fill_color=cfg.PANEL, fill_opacity=0.94,
    )
    halo = face.copy().set_stroke(color, width=16, opacity=0.0).set_fill(opacity=0)
    art = icon(name, height * 0.66)
    art.move_to(face.get_center())
    group = VGroup(halo, face, art)
    if show_name:
        # The name sits under the card, not inside it: squeezing a word like
        # "mozzarella" into the face would shrink it past reading size.
        tag = outlined_text(name, cfg.FONT["tiny"], cfg.MUTED, BOLD)
        fit_width(tag, width * 1.55)
        tag.next_to(face, DOWN, buff=0.12)
        group.add(tag)
        group.tag = tag
    group.face = face
    group.halo = halo
    group.art = art
    group.element = name
    group.card_color = color
    return group


def number_card(value: str, *, color: str = cfg.OBJECT, size: float = 1.18) -> VGroup:
    """A numeral as an element — the same card, with a digit instead of a drawing."""
    face = RoundedRectangle(
        width=size, height=size, corner_radius=0.16,
        stroke_color=color, stroke_width=3.4,
        fill_color=cfg.PANEL, fill_opacity=0.94,
    )
    halo = face.copy().set_stroke(color, width=16, opacity=0.0).set_fill(opacity=0)
    glyph = eq(value, color, 60)
    fit_width(glyph, size * 0.62)
    glyph.move_to(face.get_center())
    group = VGroup(halo, face, glyph)
    group.face = face
    group.halo = halo
    group.art = glyph
    group.element = value
    group.card_color = color
    return group


def recolor_card(card: VGroup, color: str, *, halo_opacity: float = 0.0) -> VGroup:
    """Repaint a card in place, keeping halo/face/art related as they were."""
    card.face.set_stroke(color)
    card.halo.set_stroke(color, width=16, opacity=halo_opacity)
    if isinstance(card.art, (MathTex, Text)):
        card.art.set_color(color)
    card.card_color = color
    return card


def card_target(card: VGroup, color: str, *, halo_opacity: float = 0.0) -> VGroup:
    """A recoloured copy, for use as a Transform target."""
    return recolor_card(card.copy(), color, halo_opacity=halo_opacity)


def dim_card(card: VGroup) -> VGroup:
    """The 'refused by this rule' state: present, but no longer under the light."""
    ghost = card_target(card, cfg.GRAY)
    ghost.set_opacity(0.3)
    ghost.face.set_fill(cfg.BG, opacity=0.55)
    return ghost


def lit_card(card: VGroup, color: str = cfg.INSIDE) -> VGroup:
    """The 'this rule accepts you' state: full opacity and a visible halo."""
    bright = card_target(card, color, halo_opacity=0.3)
    bright.set_opacity(1.0)
    bright.face.set_fill(cfg.PANEL, opacity=0.94)
    bright.halo.set_fill(opacity=0).set_stroke(color, width=16, opacity=0.3)
    return bright


def card_row(
    names: Sequence[str],
    *,
    color: str = cfg.OBJECT,
    buff: float = 0.34,
    width: float = 1.24,
    height: float = 1.32,
    center: Sequence[float] | None = None,
    numbers: bool = False,
) -> VGroup:
    """A row of elements, the film's picture of 'a messy pile, now lined up'."""
    maker = (lambda name: number_card(name, color=color, size=width)) if numbers else (
        lambda name: object_card(name, color=color, width=width, height=height)
    )
    row = VGroup(*[maker(name) for name in names])
    row.arrange(RIGHT, buff=buff)
    if center is not None:
        row.move_to(np.array(center))
    return row


def find_card(cards: Sequence[VGroup], element: str) -> VGroup:
    """Look a card up by the element it carries, never by its index."""
    for card in cards:
        if getattr(card, "element", None) == element:
            return card
    raise KeyError(f"No card on the board for {element!r}")


# ----------------------------------------------------------------------------
# The universe board and the set boundary
# ----------------------------------------------------------------------------


def universe_board(
    label: str = "U",
    *,
    width: float = 12.6,
    height: float = 6.1,
    center: Sequence[float] = (0.0, -0.15, 0.0),
    color: str = cfg.UNIVERSE,
    caption: str | None = None,
) -> VGroup:
    """The rectangle that says 'this, and nothing else, is under discussion'."""
    board = Rectangle(
        width=width, height=height,
        stroke_color=color, stroke_width=4,
        fill_color=cfg.PANEL_2, fill_opacity=0.32,
    )
    board.move_to(np.array(center))
    glow = board.copy().set_stroke(color, width=18, opacity=0.08).set_fill(opacity=0)
    tag = eq(label, color, cfg.FONT["section"])
    tag.next_to(board.get_corner(UL), DR, buff=0.22)
    group = VGroup(glow, board, tag)
    if caption is not None:
        # Bottom-left, not beside the U tag: the top-left corner sits at the
        # same height as the set names, and a long universe name would run
        # straight into them.
        note = outlined_text(caption, cfg.FONT["small"], color)
        note.next_to(board.get_corner(DL), UR, buff=0.24)
        group.add(note)
        group.note = note
    group.board = board
    group.tag = tag
    group.glow = glow
    return group


def set_boundary(
    center: Sequence[float],
    radius: float,
    color: str,
    label: str | None = None,
    *,
    fill_opacity: float = 0.08,
    label_direction: np.ndarray = UP,
    label_size: int | None = None,
) -> VGroup:
    """A glowing rule drawn on the board: everything inside obeys it."""
    ring = Circle(
        radius=radius, color=color, stroke_width=5,
        fill_color=color, fill_opacity=fill_opacity,
    ).move_to(np.array(center))
    halo = Circle(radius=radius * 1.03, color=color, stroke_width=20, stroke_opacity=0.10, fill_opacity=0)
    halo.move_to(ring.get_center())
    group = VGroup(halo, ring)
    if label is not None:
        tag = outlined_text(label, label_size or cfg.FONT["label"], color)
        tag.next_to(ring, label_direction, buff=0.2)
        group.add(tag)
        group.tag = tag
    group.ring = ring
    group.halo = halo
    group.boundary_color = color
    return group


def empty_container(
    center: Sequence[float],
    radius: float = 1.1,
    color: str = cfg.MUTED,
    label: str | None = None,
) -> VGroup:
    """The empty set: a transparent boundary you can see straight through."""
    dashes = VGroup()
    count = 18
    dash_angle = TAU / count * 0.58
    for index in range(count):
        dashes.add(
            Arc(
                radius=radius, start_angle=index * TAU / count, angle=dash_angle,
                arc_center=np.array(center), color=color, stroke_width=4,
            )
        )
    group = VGroup(dashes)
    if label is not None:
        tag = eq(label, color, cfg.FONT["section"])
        tag.next_to(dashes, DOWN, buff=0.26)
        group.add(tag)
        group.tag = tag
    group.dashes = dashes
    group.centre = np.array(center, dtype=float)
    group.radius = radius
    return group


# ----------------------------------------------------------------------------
# The Venn stage: one universe, two rules, and every region it defines
# ----------------------------------------------------------------------------

REGION_KINDS = (
    "a", "b", "only_a", "only_b", "both", "union",
    "neither", "not_a", "not_b", "not_both",
)


class VennStage(VGroup):
    """The recurring stage: a universe rectangle with two rules drawn on it.

    The regions are produced by real path booleans against the same circles the
    viewer can see, so ``stage.region("neither")`` is literally
    ``U \\ (A ∪ B)`` — the film cannot illuminate a shape its own algebra
    would disagree with.
    """

    def __init__(
        self,
        a_label: str,
        b_label: str,
        universe_label: str = "U",
        *,
        radius: float = 2.0,
        separation: float = 2.35,
        center: Sequence[float] = (0.0, -0.2, 0.0),
        board_width: float = 12.6,
        board_height: float = 6.1,
        a_color: str = cfg.SET_A,
        b_color: str = cfg.SET_B,
        universe_caption: str | None = None,
        label_size: int | None = None,
    ) -> None:
        super().__init__()
        self.origin = np.array(center, dtype=float)
        self.radius = radius
        self.separation = separation
        self.a_color = a_color
        self.b_color = b_color

        self.universe = universe_board(
            universe_label, width=board_width, height=board_height,
            center=self.origin, caption=universe_caption,
        )
        offset_a, offset_b = mu.circle_centres(separation)
        self.centre_a = self.origin + offset_a
        self.centre_b = self.origin + offset_b

        self.set_a = set_boundary(
            self.centre_a, radius, a_color, a_label,
            label_direction=UL, label_size=label_size,
        )
        self.set_b = set_boundary(
            self.centre_b, radius, b_color, b_label,
            label_direction=UR, label_size=label_size,
        )
        # Keep both names clear of the board's own U tag and of each other.
        self.set_a.tag.next_to(self.set_a.ring, UP, buff=0.18).shift(LEFT * radius * 0.5)
        self.set_b.tag.next_to(self.set_b.ring, UP, buff=0.18).shift(RIGHT * radius * 0.5)

        # Depth order, fixed once here so no scene has to think about it:
        # board (0) < region floods (1-2) < cards (6) < boundaries (4) < names (8).
        # A complement flood covers the whole board, so the rules it is drawn
        # against, and their names, have to stay on top of it to stay readable.
        self.universe.board.set_z_index(0)
        self.set_a.ring.set_z_index(4)
        self.set_b.ring.set_z_index(4)
        self.set_a.halo.set_z_index(3)
        self.set_b.halo.set_z_index(3)
        for tag in (self.universe.tag, self.set_a.tag, self.set_b.tag):
            tag.set_z_index(8)

        self.add(self.universe, self.set_a, self.set_b)

    CARD_Z = 6
    REGION_Z = 1
    SECOND_REGION_Z = 2

    # -- geometry -----------------------------------------------------------

    def _shape(self, kind: str) -> VMobject:
        board = self.universe.board
        circle_a = self.set_a.ring
        circle_b = self.set_b.ring
        if kind == "a":
            return circle_a.copy()
        if kind == "b":
            return circle_b.copy()
        if kind == "only_a":
            return Difference(circle_a, circle_b)
        if kind == "only_b":
            return Difference(circle_b, circle_a)
        if kind == "both":
            return Intersection(circle_a, circle_b)
        if kind == "union":
            return Union(circle_a, circle_b)
        if kind == "neither":
            return Difference(board, Union(circle_a, circle_b))
        if kind == "not_a":
            return Difference(board, circle_a)
        if kind == "not_b":
            return Difference(board, circle_b)
        if kind == "not_both":
            return Difference(board, Intersection(circle_a, circle_b))
        raise ValueError(f"Unknown region {kind!r}; expected one of {REGION_KINDS}")

    def region(
        self,
        kind: str,
        color: str = cfg.HIGHLIGHT,
        *,
        fill_opacity: float = 0.45,
        stroke_width: float = 0.0,
        glow: bool = True,
    ) -> VGroup:
        """One illuminated region, ready to fade in over the board."""
        shape = self._shape(kind)
        shape.set_stroke(color, width=stroke_width, opacity=1 if stroke_width else 0)
        shape.set_fill(color, opacity=fill_opacity)
        group = VGroup(shape)
        if glow:
            aura = shape.copy().set_fill(color, opacity=fill_opacity * 0.34)
            aura.set_stroke(color, width=16, opacity=0.16)
            group = VGroup(aura, shape)
        group.shape = shape
        group.kind = kind
        group.region_color = color
        return group

    def intersect_regions(
        self,
        first: str,
        second: str,
        color: str = cfg.HIGHLIGHT,
        *,
        fill_opacity: float = 0.45,
    ) -> VGroup:
        """The overlap of two named regions, computed independently.

        Used for the right-hand side of De Morgan's first law: Aᶜ and Bᶜ are
        built separately, then intersected, so the match with (A ∪ B)ᶜ is
        earned rather than assumed.
        """
        shape = Intersection(self._shape(first), self._shape(second))
        shape.set_stroke(width=0, opacity=0).set_fill(color, opacity=fill_opacity)
        aura = shape.copy().set_fill(color, opacity=fill_opacity * 0.34).set_stroke(color, width=16, opacity=0.16)
        group = VGroup(aura, shape)
        group.shape = shape
        group.kind = f"{first}&{second}"
        group.region_color = color
        return group

    def unite_regions(
        self,
        first: str,
        second: str,
        color: str = cfg.HIGHLIGHT,
        *,
        fill_opacity: float = 0.45,
    ) -> VGroup:
        """The union of two named regions — the right-hand side of the second law."""
        shape = Union(self._shape(first), self._shape(second))
        shape.set_stroke(width=0, opacity=0).set_fill(color, opacity=fill_opacity)
        aura = shape.copy().set_fill(color, opacity=fill_opacity * 0.34).set_stroke(color, width=16, opacity=0.16)
        group = VGroup(aura, shape)
        group.shape = shape
        group.kind = f"{first}|{second}"
        group.region_color = color
        return group

    # -- seating ------------------------------------------------------------

    def seats(self, kind: str, count: int) -> list[np.ndarray]:
        """Where cards belonging to a region should physically sit."""
        if count <= 0:
            return []
        if kind in ("only_a", "a"):
            return mu.seats_only_in(self.centre_a, self.centre_b, self.radius, count)
        if kind in ("only_b", "b"):
            return mu.seats_only_in(self.centre_b, self.centre_a, self.radius, count)
        if kind == "both":
            lens_height = mu.lens_half_height(self.radius, self.separation)
            return mu.stacked_seats(
                self.origin, count, columns=1,
                y_step=min(1.05, 1.5 * lens_height / max(count, 1)),
            )
        if kind == "neither":
            return [
                self.origin + point
                for point in mu.scatter_outside(
                    count, self.centre_a - self.origin, self.centre_b - self.origin,
                    self.radius,
                    box=(self.universe.board.width - 1.5, self.universe.board.height - 1.5),
                    seed=cfg.SEED,
                )
            ]
        raise ValueError(f"No seating rule for region {kind!r}")

    def verify_seating(self, seats: Sequence[Sequence[float]], kind: str) -> bool:
        """True when every seat really falls in the region it claims."""
        wanted = {"a": "a", "only_a": "a", "b": "b", "only_b": "b",
                  "both": "both", "neither": "neither"}[kind]
        return all(
            mu.classify_point(seat, self.centre_a, self.centre_b, self.radius) == wanted
            for seat in seats
        )


# ----------------------------------------------------------------------------
# Scanners: the film's way of asking a question about one object
# ----------------------------------------------------------------------------


def scanner_gate(
    label: str,
    color: str = cfg.CYAN,
    *,
    width: float = 2.6,
    height: float = 2.0,
) -> VGroup:
    """A gate a card must pass through: one rule, asked as a question."""
    frame = RoundedRectangle(
        width=width, height=height, corner_radius=0.16,
        stroke_color=color, stroke_width=4,
        fill_color=cfg.PANEL, fill_opacity=0.5,
    )
    beam = Line(frame.get_left() + RIGHT * 0.12, frame.get_right() + LEFT * 0.12, color=color, stroke_width=3)
    beam.set_stroke(opacity=0.55)
    tag = outlined_text(label, cfg.FONT["small"], color)
    fit_width(tag, width - 0.3)
    tag.next_to(frame, UP, buff=0.18)
    group = VGroup(frame, beam, tag)
    group.frame = frame
    group.beam = beam
    group.tag = tag
    return group


def sweep_scanner(
    scene: Scene,
    gate: VGroup,
    color: str,
    *,
    run_time: float = 0.9,
    sweeps: int = 1,
) -> None:
    """Run the gate's beam down and back: the picture of 'checking'."""
    frame = gate.frame
    top = frame.get_top() + DOWN * 0.16
    bottom = frame.get_bottom() + UP * 0.16
    gate.beam.set_stroke(color, opacity=0.9)
    gate.beam.move_to(top)
    for _ in range(sweeps):
        scene.play(
            gate.beam.animate.move_to(bottom),
            run_time=run_time / 2, rate_func=linear,
        )
        scene.play(
            gate.beam.animate.move_to(top),
            run_time=run_time / 2, rate_func=linear,
        )


def membership_note(element: str, set_name: str, member: bool, *, font_size: int | None = None) -> MathTex:
    """``apple ∈ A`` or ``pizza ∉ A``, in the film's one notation."""
    symbol = r"\in" if member else r"\notin"
    color = cfg.INSIDE if member else cfg.OUTSIDE
    return eq(
        rf"\text{{{element}}} \;{symbol}\; {set_name}",
        color,
        font_size or cfg.FONT["title"],
    )


def not_button(label: str = "NOT", color: str = cfg.COMPLEMENT, radius: float = 0.78) -> VGroup:
    """The giant button that inverts a mask — pressed twice in the film."""
    plate = Circle(radius=radius, color=color, stroke_width=5, fill_color=cfg.PANEL_2, fill_opacity=0.95)
    bevel = Circle(radius=radius * 0.84, color=color, stroke_width=2.6, stroke_opacity=0.5, fill_opacity=0)
    halo = Circle(radius=radius * 1.18, color=color, stroke_width=0, fill_color=color, fill_opacity=0.08)
    text = outlined_text(label, cfg.FONT["small"], color)
    fit_width(text, radius * 1.35)
    text.move_to(plate.get_center())
    group = VGroup(halo, plate, bevel, text)
    group.plate = plate
    group.halo = halo
    group.text = text
    return group


def press_button(scene: Scene, button: VGroup, *, run_time: float = 0.6) -> None:
    """Push the NOT button in, and let the shockwave leave the frame."""
    ring = button.plate.copy().set_fill(opacity=0).set_stroke(button.text.get_color(), width=8, opacity=0.9)
    scene.add(ring)
    scene.play(
        button.animate.scale(0.9),
        ring.animate.scale(5.5).set_stroke(opacity=0),
        run_time=run_time,
    )
    scene.remove(ring)
    scene.play(button.animate.scale(1 / 0.9), run_time=run_time * 0.5)
