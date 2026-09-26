"""Procedural 3D props, for the three chapters that genuinely need depth.

Set theory is usually drawn flat, and flat drawing hides two things:

* **containment** — ``cats ⊆ mammals ⊆ animals`` is nesting, and nesting reads
  as nesting only when you can look into it (:func:`containment_shells`);
* **the universe** — ``Aᶜ`` means nothing until you can see that the board has
  an edge, and that beyond that edge there is no useful boundary at all
  (:func:`universe_slab`, :func:`void_field`).

The De Morgan chapter then stacks two real masks in depth
(:func:`mask_plate`) so that 'these two regions are the same region' is a
physical alignment, not a claim.

Everything is built face-on to the default camera, which keeps labels readable
at the modest tilts the film actually uses.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import outlined_text

GLASS = "#8ED4FF"
DECK = "#0B2A47"


# ---------------------------------------------------------------------------
# Chapter 03: subsets as nested glass shells
# ---------------------------------------------------------------------------


def containment_shells(
    specs: Sequence[tuple[str, float, float, str]],
    *,
    base_z: float = -1.6,
) -> VGroup:
    """Open glass tubes standing on a deck, each one inside the last.

    ``specs`` runs outermost first: ``(label, radius, height, colour)``. A card
    dropped into the innermost tube is simultaneously inside all of them, which
    is the whole of ``C ⊆ M ⊆ A`` in one picture.
    """
    deck = Cylinder(
        radius=max(radius for _, radius, _, _ in specs) * 1.12,
        height=0.12, direction=OUT, resolution=(4, 36), show_ends=True,
    )
    deck.set_fill(DECK, opacity=0.9).set_stroke(cfg.MUTED, width=1, opacity=0.35)
    deck.move_to([0, 0, base_z])

    shells = VGroup()
    rims = VGroup()
    tags = VGroup()
    for label, radius, height, color in specs:
        tube = Cylinder(
            radius=radius, height=height, direction=OUT,
            resolution=(2, 32), show_ends=False,
        )
        # A dense wireframe reads as noise at this scale; the rim carries the edge.
        tube.set_fill(color, opacity=0.14).set_stroke(color, width=1.0, opacity=0.2)
        tube.move_to([0, 0, base_z + height / 2])
        rim = Circle(radius=radius, color=color, stroke_width=5, fill_opacity=0)
        rim.move_to([0, 0, base_z + height])
        tag = outlined_text(label, cfg.FONT["body"], color)
        tag.rotate(PI / 2, axis=RIGHT)
        tag.move_to([0, -radius - 0.3, base_z + height + 0.28])
        shells.add(tube)
        rims.add(rim)
        tags.add(tag)

    group = VGroup(deck, shells, rims, tags)
    group.deck = deck
    group.shells = shells
    group.rims = rims
    group.tags = tags
    group.base_z = base_z
    group.centres = [np.array([0.0, 0.0, base_z + height]) for _, _, height, _ in specs]
    return group


def lying_card(card: VGroup, position: Sequence[float]) -> VGroup:
    """Place a card face-up in 3D, the way a dropped card actually lands.

    An upright card would turn edge-on as the camera orbits; lying flat it
    stays legible from every angle the film uses.
    """
    flat = card.copy()
    flat.move_to(np.array(position))
    return flat


# ---------------------------------------------------------------------------
# Chapter 08: the universe has an edge, and beyond it there is nothing useful
# ---------------------------------------------------------------------------


def universe_slab(
    width: float = 11.0,
    height: float = 5.8,
    *,
    thickness: float = 0.22,
    color: str = cfg.UNIVERSE,
) -> VGroup:
    """The universe rectangle as a real slab, so it can be seen edge-on."""
    slab = Prism(dimensions=[width, height, thickness])
    slab.set_fill(cfg.PANEL_2, opacity=0.86).set_stroke(color, width=2.2, opacity=0.8)
    rim = Rectangle(width=width, height=height, stroke_color=color, stroke_width=5, fill_opacity=0)
    rim.shift(OUT * (thickness / 2 + 0.01))
    group = VGroup(slab, rim)
    group.slab = slab
    group.rim = rim
    group.surface_z = thickness / 2 + 0.02
    return group


def void_field(
    count: int = 260,
    *,
    inner: float = 8.0,
    outer: float = 26.0,
    depth: float = 14.0,
    seed: int = cfg.SEED,
) -> VGroup:
    """A cold dust field far outside the universe slab: 'not A' with no edge.

    The points are pushed outside an inner radius so they never crowd the
    board, and dimmed with distance so the camera pull-back reads as falling
    away from everything, not as zooming into noise.
    """
    rng = np.random.default_rng(seed)
    field = VGroup()
    for _ in range(count):
        angle = rng.uniform(0, TAU)
        radius = rng.uniform(inner, outer)
        z = rng.uniform(-depth, depth * 0.3)
        brightness = float(np.interp(radius, [inner, outer], [0.55, 0.08]))
        field.add(
            Dot(
                [radius * np.cos(angle), radius * np.sin(angle) * 0.62, z],
                radius=float(rng.uniform(0.02, 0.06)),
                color=cfg.COMPLEMENT if rng.random() < 0.35 else cfg.MUTED,
                fill_opacity=brightness,
            )
        )
    field.submobjects.sort(key=lambda mob: float(mob.get_center()[2]))
    return field


# ---------------------------------------------------------------------------
# Chapter 10: two masks, stacked in depth, proved identical by alignment
# ---------------------------------------------------------------------------


def mask_plate(
    region: VMobject,
    *,
    board_width: float = 11.0,
    board_height: float = 5.6,
    z: float = 0.0,
    frame_color: str = cfg.MUTED,
    title: Mobject | str | None = None,
    title_color: str = cfg.WHITE,
) -> VGroup:
    """One frozen region, mounted on its own transparent sheet at depth ``z``.

    The two sides of De Morgan's law are built on two of these. Sliding one
    plate onto the other is the proof the chapter actually shows.
    """
    sheet = Rectangle(
        width=board_width, height=board_height,
        stroke_color=frame_color, stroke_width=3.4, stroke_opacity=0.75,
        fill_color=cfg.PANEL_2, fill_opacity=0.24,
    )
    # Preserve the mask aspect ratio and keep every edge inside its sheet.
    region.scale(min((board_width - 0.2) / region.width, (board_height - 0.2) / region.height))
    region.move_to(sheet.get_center() + OUT * 0.01)
    plate = VGroup(sheet, region)
    if title is not None:
        # A caller with a formula passes the mobject; plain text is built here.
        tag = title if isinstance(title, Mobject) else outlined_text(title, cfg.FONT["small"], title_color)
        tag.next_to(sheet, UP, buff=0.16)
        plate.add(tag)
        plate.tag = tag
    plate.shift(OUT * z)
    plate.sheet = sheet
    plate.region = region
    return plate


# ---------------------------------------------------------------------------
# Chapter 12: the same regions, standing up in other subjects
# ---------------------------------------------------------------------------


def domain_pillar(
    title: str,
    color: str,
    *,
    width: float = 2.9,
    height: float = 2.0,
    depth: float = 0.2,
) -> VGroup:
    """A titled panel with real thickness, for the closing carousel."""
    body = Prism(dimensions=[width, height, depth])
    body.set_fill(cfg.PANEL, opacity=0.92).set_stroke(color, width=2.4, opacity=0.85)
    face = RoundedRectangle(
        width=width - 0.18, height=height - 0.18, corner_radius=0.12,
        stroke_color=color, stroke_width=3, stroke_opacity=0.7, fill_opacity=0,
    ).shift(OUT * (depth / 2 + 0.01))
    tag = outlined_text(title, cfg.FONT["small"], color)
    if tag.width > width - 0.75:
        tag.scale_to_fit_width(width - 0.75)
    tag.move_to(face.get_top() + DOWN * 0.34 + OUT * (depth / 2 + 0.02))
    group = VGroup(body, face, tag)
    group.body = body
    group.face = face
    group.tag = tag
    group.content_anchor = face.get_center() + DOWN * 0.28 + OUT * (depth / 2 + 0.02)
    return group


def mini_venn(
    color_a: str,
    color_b: str,
    *,
    radius: float = 0.4,
    separation: float = 0.46,
    highlight: str | None = None,
    highlight_color: str = cfg.HIGHLIGHT,
) -> VGroup:
    """A thumbnail Venn diagram, used as the shared glyph of the final chapter."""
    left = Circle(radius=radius, color=color_a, stroke_width=3.4, fill_color=color_a, fill_opacity=0.14)
    right = Circle(radius=radius, color=color_b, stroke_width=3.4, fill_color=color_b, fill_opacity=0.14)
    left.shift(LEFT * separation / 2)
    right.shift(RIGHT * separation / 2)
    # A thumbnail needs its own frame to take a complement against, so one is
    # drawn round the pair and kept invisible unless a complement is asked for.
    frame = Rectangle(
        width=separation + 2 * radius + 0.34, height=2 * radius + 0.3,
        stroke_color=cfg.UNIVERSE, stroke_width=2, stroke_opacity=0.0, fill_opacity=0,
    )
    group = VGroup(frame, left, right)
    if highlight is not None:
        if highlight == "both":
            shape = Intersection(left, right)
        elif highlight == "union":
            shape = Union(left, right)
        elif highlight == "a":
            shape = left.copy()
        elif highlight == "only_a":
            shape = Difference(left, right)
        elif highlight == "not_a":
            shape = Difference(frame, left)
            frame.set_stroke(opacity=0.55)
        elif highlight == "neither":
            shape = Difference(frame, Union(left, right))
            frame.set_stroke(opacity=0.55)
        else:
            raise ValueError(f"mini_venn cannot highlight {highlight!r}")
        shape.set_stroke(width=0, opacity=0).set_fill(highlight_color, opacity=0.55)
        group.add(shape)
        group.highlight = shape
    group.frame = frame
    group.left = left
    group.right = right
    return group
