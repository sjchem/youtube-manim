"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
final reconstruction reads as a conclusion rather than a new picture:

* an **element** is a rounded tile whose outline is its block's colour;
* the **table** is never typed: every tile goes where ``utils.physics_models``
  says the filling of electrons puts it;
* an **orbital** is a box, a **subshell** is a row of boxes, and an
  **electron** is a spin arrow — cyan up, purple down, as in Part 2;
* a **shape** is a lit 3D polar surface of the angular density ``|Y_lm|^2``;
* a **width** is always shown as a brace with a gold number under it.

Scene files compose these pieces and choreograph them against the beats in
``narration.py``; nothing in a scene file should invent a second way to draw
one of these ideas.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from functools import lru_cache

import numpy as np
from manim import *

import config as cfg
from narration import SCRIPT
from utils import math_utils as mu
from utils import physics_models as pm
from utils.render_helpers import fit_inside, fit_to_safe_frame, fit_width

# ----------------------------------------------------------------------------
# Scene lifecycle
# ----------------------------------------------------------------------------


def start(scene: Scene, key: str, title: str | None = None) -> tuple[float, VGroup | None]:
    """Theme the scene, add the quiet background, and show the chapter heading."""
    cfg.apply_project_theme(scene, bubbles=False)
    scene._project_scene_key = key
    reset_camera(scene)
    add_background(scene)
    started = float(scene.time)
    from utils.voiceover import attach_voiceover

    attach_voiceover(scene, key)
    head = None
    if title:
        head = heading(title)
        hud(scene, head)
        scene.play(FadeIn(head, shift=DOWN * 0.18), run_time=0.6)
    return started, head


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """scene.play with an explicit default run time, so pacing is never accidental."""
    kwargs["run_time"] = kwargs.get("run_time", 1.0)
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Hold the composition steady; live orbital/background updaters keep moving."""
    scene.wait(max(seconds, 0.0))


# How late a cue may arrive before a chapter is refused. The still-frame tools
# (storyboard, layout audit) run at 5 fps, where per-play frame rounding piles
# up; they raise this limit, and timing is enforced by utils.timing_audit.
CUE_TOLERANCE = 0.14


def cue(scene: Scene, started_at: float, seconds: float) -> None:
    """Hold until a named second inside the chapter, and refuse to run past it."""
    import manim_scenes.common as common

    remaining = seconds - (float(scene.time) - started_at)
    key = getattr(scene, "_project_scene_key", "unknown")
    if remaining < -common.CUE_TOLERANCE:
        raise ValueError(f"Scene {key} cue {seconds}s overrun by {-remaining:.2f}s")
    if remaining > 1e-6:
        narration_wait(scene, remaining)


def beat(scene: Scene, started_at: float, index: int) -> None:
    """Hold until narration beat ``index`` of this chapter begins."""
    key = scene._project_scene_key
    cue(scene, started_at, SCRIPT[key][index][0])


def end_scene(scene: Scene, started_at: float, target_seconds: float) -> None:
    """Finish on the configured frame boundary, fade out, and reset the camera."""
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
    visible = [mob for mob in scene.mobjects if not getattr(mob, "_is_project_background", False)]
    for mob in visible:
        mob.clear_updaters()
    if visible:
        scene.play(FadeOut(*visible), run_time=fade_frames / fps)
        scene.remove(*visible)
    else:
        scene.wait(fade_frames / fps)
    reset_camera(scene)


# ----------------------------------------------------------------------------
# Camera
# ----------------------------------------------------------------------------


def is_3d(scene: Scene) -> bool:
    return isinstance(scene, ThreeDScene)


def reset_camera(scene: Scene) -> None:
    """Return to the flat front view and forget every fixed-in-frame registration."""
    if not is_3d(scene):
        return
    scene.set_camera_orientation(phi=0, theta=-PI / 2, gamma=0, zoom=1, frame_center=ORIGIN)
    scene.camera.fixed_in_frame_mobjects = set()
    scene.camera.fixed_orientation_mobjects = {}
    # The shared bubble layer outlives every chapter and must stay pinned to the screen.
    for mob in scene.mobjects:
        if getattr(mob, "_is_project_background", False):
            scene.camera.add_fixed_in_frame_mobjects(mob)


def hud(scene: Scene, *mobjects: Mobject) -> None:
    """Pin text to the screen, so a camera move never tilts or zooms a caption.

    The mobjects are registered but not added; animate them in as usual.
    """
    if is_3d(scene):
        scene.camera.add_fixed_in_frame_mobjects(*mobjects)


def move_camera(scene: Scene, run_time: float = 2.0, **kwargs) -> None:
    if is_3d(scene):
        scene.move_camera(run_time=run_time, **kwargs)
    else:
        scene.wait(run_time)


# ----------------------------------------------------------------------------
# Background
# ----------------------------------------------------------------------------


def add_background(scene: Scene) -> VGroup:
    """A faint, static Oceanic background shared by every chapter.

    There is deliberately no flat backdrop rectangle. In a 3D chapter the
    camera draws every flat mobject after the depth-sorted surfaces, so a
    backdrop would paint over the orbitals. The camera's background colour does
    that job instead, and the bubbles are faint enough to float over anything.
    """
    for mob in scene.mobjects:
        if getattr(mob, "_is_project_background", False):
            return mob
    bubbles = cfg.oceanic_bubbles()
    for part in bubbles.family_members_with_points():
        part.set_fill(opacity=float(part.get_fill_opacity()) * 0.35)
        part.set_stroke(opacity=float(part.get_stroke_opacity()) * 0.35)
    bubbles._is_project_background = True
    bubbles.set_z_index(-10)
    scene.add(bubbles)
    hud(scene, bubbles)
    return bubbles


# ----------------------------------------------------------------------------
# Type
# ----------------------------------------------------------------------------


def txt(body: str, size: int | None = None, color: str = cfg.WHITE, weight=BOLD, font: str | None = None) -> Text:
    """Bold text with a dark outline, so it stays crisp over any glow."""
    kwargs = {"font": font} if font else {}
    result = Text(body, font_size=size or cfg.FONT["body"], color=color, weight=weight, **kwargs)
    result.set_stroke(cfg.BG, width=1.5, opacity=0.85, background=True)
    return result


# Computer Modern sets visibly smaller than Lato at the same nominal
# size; this factor makes ``eq(x, 40)`` read as large as ``txt(y, 40)``.
MATH_SCALE = 1.35


def eq(latex: str, size: int | None = None, color: str = cfg.WHITE, **kwargs) -> MathTex:
    """An equation with the same dark outline as the captions, sized like text."""
    result = MathTex(latex, font_size=(size or cfg.FONT["section"]) * MATH_SCALE, color=color, **kwargs)
    result.set_stroke(cfg.BG, width=1.2, opacity=0.85, background=True)
    return result


def decorative(mob: Mobject) -> Mobject:
    """Mark a glow or shadow copy so the layout audit does not read it as text."""
    for member in mob.get_family():
        member._is_decorative = True
    return mob


def number(value: int, size: int | None = None, color: str = cfg.GOLD) -> Integer:
    """An animatable integer, sized to match ``eq`` and ``txt``."""
    result = Integer(value, font_size=(size or cfg.FONT["section"]) * MATH_SCALE, color=color)
    result.set_stroke(cfg.BG, width=1.2, opacity=0.85, background=True)
    return result


def heading(title: str, color: str = cfg.GOLD, size: int = 46) -> VGroup:
    """Chapter caption: bold gold type with a soft offset shadow, top of frame."""
    main = txt(title, size, color)
    fit_width(main, 13.6)
    shadow = main.copy().set_color(cfg.BG).set_opacity(0.85).shift(RIGHT * 0.05 + DOWN * 0.05)
    shadow.set_stroke(width=0)
    decorative(shadow)
    glow = main.copy().set_color(color).set_opacity(0.10).scale(1.02)
    glow.set_stroke(color, width=10, opacity=0.10)
    decorative(glow)
    group = VGroup(glow, shadow, main)
    group.move_to(UP * 3.86)
    group.main = main
    return group


def swap_heading(scene: Scene, old: VGroup | None, title: str, run_time: float = 0.6) -> VGroup:
    """Replace the chapter caption (fade, never morph, so HUD registration holds)."""
    new = heading(title)
    hud(scene, new)
    if old is not None:
        scene.play(FadeOut(old, shift=UP * 0.15), FadeIn(new, shift=UP * 0.15), run_time=run_time)
        scene.remove(old)
    else:
        scene.play(FadeIn(new, shift=DOWN * 0.15), run_time=run_time)
    return new


def caption(body: str, color: str = cfg.WHITE, size: int | None = None, y: float = -3.85) -> Text:
    """A short bottom caption, on a phone-readable size."""
    line = txt(body, size or cfg.FONT["small"], color)
    fit_width(line, 13.4)
    return line.move_to(UP * y)


def chip(body: str, color: str = cfg.CYAN, size: int | None = None) -> VGroup:
    """A rounded pill with a label: ORDER, SHAPE, ANALOGY..."""
    label = txt(body, size or cfg.FONT["small"], color)
    pill = RoundedRectangle(
        width=label.width + 0.6, height=label.height + 0.36, corner_radius=0.22,
        stroke_color=color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.92,
    )
    return VGroup(pill, label.move_to(pill))


def panel(width: float, height: float, color: str = cfg.MUTED, opacity: float = 0.75) -> RoundedRectangle:
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.22,
        stroke_color=color, stroke_width=2, stroke_opacity=0.6,
        fill_color=cfg.PANEL, fill_opacity=opacity,
    )


# ----------------------------------------------------------------------------
# Glow
# ----------------------------------------------------------------------------


def halo(radius: float, color: str, layers: int = 5, peak_opacity: float = 0.16) -> VGroup:
    """Concentric translucent discs — a soft glow without a raster image."""
    group = VGroup()
    for index in range(layers):
        frac = (index + 1) / layers
        group.add(Circle(radius=radius * (0.35 + 0.65 * frac), stroke_width=0,
                         fill_color=color, fill_opacity=peak_opacity * (1.15 - frac)))
    return group


def glow_dot(point=ORIGIN, radius: float = 0.11, color: str = cfg.ELECTRON_COLOR) -> VGroup:
    core = Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=1)
    shine = Circle(radius=radius * 0.38, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.8)
    shine.shift(UL * radius * 0.3)
    return VGroup(halo(radius * 3.2, color), core, shine).move_to(point)


def glow_frame(mob: Mobject, color: str = cfg.GOLD, buff: float = 0.12, width: float = 4) -> VGroup:
    """A glowing rounded outline around anything — the film's 'look here'."""
    w, h = mob.width + 2 * buff, mob.height + 2 * buff
    group = VGroup()
    for spread, opacity in ((14, 0.10), (8, 0.18), (width, 1.0)):
        group.add(RoundedRectangle(width=w, height=h, corner_radius=min(0.18, h / 3),
                                   stroke_color=color, stroke_width=spread,
                                   stroke_opacity=opacity, fill_opacity=0))
    return group.move_to(mob)


def check_mark(size: float = 0.32, color: str = cfg.GREEN) -> VMobject:
    mark = VMobject(stroke_color=color, stroke_width=8)
    mark.set_points_as_corners([LEFT * size + UP * 0.05, DOWN * size * 0.75 + LEFT * size * 0.15, RIGHT * size + UP * size])
    return mark


def cross_mark(size: float = 0.3, color: str = cfg.RED) -> VGroup:
    return VGroup(
        Line(UL * size, DR * size, stroke_color=color, stroke_width=9),
        Line(UR * size, DL * size, stroke_color=color, stroke_width=9),
    )


def glow_line(start, end, color: str, width: float = 5) -> VGroup:
    return VGroup(
        Line(start, end, stroke_color=color, stroke_width=width * 4, stroke_opacity=0.12),
        Line(start, end, stroke_color=color, stroke_width=width * 2, stroke_opacity=0.25),
        Line(start, end, stroke_color=color, stroke_width=width),
    )


def width_brace(mob: Mobject, number: int | str, color: str = cfg.GOLD,
                direction=UP, size: int | None = None) -> VGroup:
    """A brace with a big number: the film's single way of showing a width."""
    brace = Brace(mob, direction=direction, color=color, buff=0.12)
    label = txt(str(number), size or cfg.FONT["section"], color)
    label.next_to(brace, direction, buff=0.12)
    group = VGroup(brace, label)
    group.brace, group.label = brace, label
    return group


# ----------------------------------------------------------------------------
# Elements and the table
# ----------------------------------------------------------------------------


def block_color(z: int) -> str:
    return cfg.BLOCK_COLORS[pm.block(z)]


def element_tile(
    z: int,
    size: float = 0.66,
    color: str | None = None,
    *,
    symbol: bool = True,
    number: bool = False,
    name: bool = False,
    fill: float = 0.18,
) -> VGroup:
    """One element: a rounded tile outlined in its block colour."""
    colour = color or block_color(z)
    box = RoundedRectangle(
        width=size, height=size, corner_radius=size * 0.12,
        stroke_color=colour, stroke_width=max(1.4, 3.2 * size),
        fill_color=interpolate_color(ManimColor(cfg.PANEL), ManimColor(colour), fill),
        fill_opacity=0.95,
    )
    tile = VGroup(box)
    tile.box, tile.z, tile.color_name = box, z, colour
    if symbol:
        label = Text(pm.symbol_of(z), font_size=48, color=cfg.WHITE, weight=BOLD)
        named = name and pm.symbol_of(z) in pm.NAMES
        # Reserve a distinct header band for the atomic number on hero tiles.
        cap = 0.38 if named else 0.48
        fit_inside(label.scale(size * 0.62 / max(label.height, 1e-6)), size * 0.74, size * cap)
        label.move_to(box).shift(DOWN * size * 0.01 if named else DOWN * size * (0.06 if number else 0))
        label._tile_label = True
        tile.add(label)
        tile.symbol = label
    if number:
        tag = Text(str(z), font_size=48, color=cfg.MUTED, weight=BOLD)
        tag.scale(size * (0.18 if name else 0.2) / tag.height).move_to(
            box.get_corner(UL) + np.array([size * 0.2, -size * 0.16, 0]))
        tag.align_to(box.get_left() + RIGHT * size * 0.1, LEFT)
        tag._tile_label = True
        tile.add(tag)
        tile.number = tag
    if name and pm.symbol_of(z) in pm.NAMES:
        title = Text(pm.NAMES[pm.symbol_of(z)], font_size=48, color=cfg.MUTED, weight=BOLD)
        fit_inside(title.scale(size * 0.13 / title.height), size * 0.86, size * 0.16)
        title.move_to(box.get_bottom() + UP * size * 0.14)
        title._tile_label = True
        tile.add(title)
        tile.title = title
    return tile


def big_tile(z: int, size: float = 1.9, color: str | None = None) -> VGroup:
    """A hero tile with atomic number, symbol and name, for close-ups."""
    return element_tile(z, size, color, number=True, name=True, fill=0.22)


TABLE_PITCH = 0.70
TABLE_CENTER = DOWN * 0.42


def table_point(z: int, layout: str = "standard", pitch: float = TABLE_PITCH, center=TABLE_CENTER) -> np.ndarray:
    """Where element ``z`` sits on screen. The row and column come from the model."""
    row, col = pm.position(z, layout)
    return grid_point(row, col, layout, pitch, center)


def grid_point(row: int, col: int, layout: str = "standard", pitch: float = TABLE_PITCH, center=TABLE_CENTER) -> np.ndarray:
    if layout == "standard":
        gap = 0.38 * pitch
        x = (col - 9.5) * pitch
        y = (8 * pitch + gap) / 2 - (row - 1) * pitch - (gap if row >= 8 else 0)
    else:
        x = (col - 16.5) * pitch
        y = 3 * pitch - (row - 1) * pitch
    return np.array([x, y, 0.0]) + np.asarray(center, dtype=float)


def periodic_table(
    layout: str = "standard",
    pitch: float = TABLE_PITCH,
    center=TABLE_CENTER,
    zs: Iterable[int] | None = None,
    *,
    style: str = "block",
    symbols: bool = True,
    fill_ratio: float = 0.9,
) -> VGroup:
    """The table, assembled from the filling model.

    ``style`` is ``block`` (block colours), ``plain`` (one cyan for all) or
    ``silhouette`` (no symbols, muted — the outline the film opens on).
    """
    table = VGroup()
    table.tiles, table.layout, table.pitch, table.center = {}, layout, pitch, np.asarray(center, dtype=float)
    for z in zs or range(1, len(pm.SYMBOLS) + 1):
        if style == "block":
            colour = None
        elif style == "plain":
            colour = cfg.CYAN
        else:
            colour = cfg.MUTED
        tile = element_tile(z, pitch * fill_ratio, colour, symbol=symbols and style != "silhouette",
                            fill=0.10 if style == "silhouette" else 0.18)
        tile.move_to(table_point(z, layout, pitch, center))
        table.add(tile)
        table.tiles[z] = tile
    return table


# The build board: rows 1-4 of the table, full width, across the top of the
# frame. Chapters 5, 6 and 9 build the table on it, element by element, while
# the orbital boxes are worked on in the space underneath.
BOARD_PITCH = 0.72
BOARD_CENTER = np.array([0.0, -0.3, 0.0])


def board_point(z: int | None = None, row: int | None = None, col: int | None = None) -> np.ndarray:
    if z is not None:
        return table_point(z, pitch=BOARD_PITCH, center=BOARD_CENTER)
    return grid_point(row, col, pitch=BOARD_PITCH, center=BOARD_CENTER)


def build_board(last_z: int = 36) -> VGroup:
    """Ghost slots for the first periods, waiting to be filled."""
    board = periodic_table(pitch=BOARD_PITCH, center=BOARD_CENTER, zs=range(1, last_z + 1), style="silhouette")
    board.set_opacity(0.3)
    return board


def board_tile(z: int, color: str | None = None) -> VGroup:
    return element_tile(z, BOARD_PITCH * 0.9, color).move_to(board_point(z))


def tiles_of(table: VGroup, zs: Iterable[int]) -> VGroup:
    return VGroup(*[table.tiles[z] for z in zs if z in table.tiles])


def block_tiles(table: VGroup, letter: str) -> VGroup:
    return tiles_of(table, pm.elements_in_block(letter))


def covered_labels(cover: Mobject, tiles: Iterable[VGroup], margin: float = 0.2) -> list[Mobject]:
    """Tile labels hidden under (or crowding) an opaque overlay such as a capacity pill.

    The overlay paints over them anyway; fading them out with it keeps the
    picture identical while making sure no text sits beneath other text.
    """
    left, bottom = cover.get_corner(DL)[:2] - margin
    right, top = cover.get_corner(UR)[:2] + margin
    hidden = []
    for tile in tiles:
        for label in (getattr(tile, "symbol", None), getattr(tile, "number", None), getattr(tile, "title", None)):
            if label is None:
                continue
            (lx, ly), (rx, ry) = label.get_corner(DL)[:2], label.get_corner(UR)[:2]
            if rx > left and lx < right and ry > bottom and ly < top:
                hidden.append(label)
    return hidden


def recolor_tiles(tiles: Iterable[VGroup], color_for) -> list[Animation]:
    """Animations that re-outline tiles; ``color_for(z)`` picks each colour."""
    animations = []
    for tile in tiles:
        colour = color_for(tile.z)
        fill = interpolate_color(ManimColor(cfg.PANEL), ManimColor(colour), 0.22)
        animations.append(tile.box.animate.set_stroke(colour).set_fill(fill, 0.95))
    return animations


# ----------------------------------------------------------------------------
# Orbital boxes and spin arrows
# ----------------------------------------------------------------------------


def orbital_row(l: int, label: str | None = None, box: float = 0.86, gap: float = 0.14,
                color: str | None = None, label_size: int | None = None) -> VGroup:
    """A subshell drawn as 2l + 1 boxes. A box counts one orbital; it is not a room."""
    colour = color or cfg.BLOCK_COLORS[pm.L_LETTERS[l]]
    boxes = VGroup(*[
        RoundedRectangle(width=box, height=box, corner_radius=box * 0.12,
                         stroke_color=colour, stroke_width=3,
                         fill_color=cfg.PANEL, fill_opacity=0.85)
        for _ in range(2 * l + 1)
    ]).arrange(RIGHT, buff=gap)
    row = VGroup(boxes)
    row.boxes, row.l, row.box_size, row.color_name = boxes, l, box, colour
    row.tag = None
    if label:
        tag = eq(label, label_size or cfg.FONT["label"], colour)
        tag.next_to(boxes, LEFT, buff=0.32)
        row.add(tag)
        row.tag = tag
    return row


def spin_arrow(box: Mobject, spin: int, size: float | None = None) -> Arrow:
    """Up arrows sit left in a box and are cyan; down arrows sit right, purple."""
    s = size or box.width
    x = box.get_center()[0] + (-0.2 if spin > 0 else 0.2) * s
    y = box.get_center()[1]
    half = 0.33 * s
    start, end = ([x, y - half, 0], [x, y + half, 0]) if spin > 0 else ([x, y + half, 0], [x, y - half, 0])
    return Arrow(start, end, buff=0, color=cfg.SPIN_UP if spin > 0 else cfg.SPIN_DOWN,
                 stroke_width=max(3.0, 6.5 * s), max_tip_length_to_length_ratio=0.32,
                 max_stroke_width_to_length_ratio=12)


def row_arrows(row: VGroup, count: int) -> list[Arrow]:
    """The arrows for ``count`` electrons in this subshell, in Hund order."""
    return [spin_arrow(row.boxes[i], spin, row.box_size) for i, spin in pm.hund_slots(row.l, count)]


def drop_in(arrow: Mobject, height: float = 0.55) -> Animation:
    """An electron arriving: it falls into its box and brightens."""
    return FadeIn(arrow, shift=DOWN * height if arrow.get_vector()[1] > 0 else UP * height, scale=0.8)


def electron_arrives(scene: Scene, arrow: Arrow, origin, run_time: float = 1.0) -> None:
    """A glowing electron flies in along an arc and becomes a spin arrow."""
    dot = glow_dot(origin, 0.1)
    path = ArcBetweenPoints(np.asarray(origin, dtype=float), arrow.get_center(), angle=-PI / 3)
    scene.play(FadeIn(dot, scale=0.5), run_time=0.25)
    scene.play(MoveAlongPath(dot, path), run_time=run_time * 0.6, rate_func=smooth)
    scene.play(ReplacementTransform(dot, arrow), run_time=run_time * 0.4)


def box_ladder(labels: Sequence[str], bottom: float = -3.0, step: float = 0.9, box: float = 0.62,
               x: float = 0.0, label_size: int | None = None, heights: dict[str, float] | None = None) -> VGroup:
    """Subshells as rows of orbital boxes, stacked by (schematic) energy.

    Rows are centred on ``x`` so the diagram reads as a symmetric ladder; the
    labels line up in one column to the left of the widest possible row.
    ``heights`` overrides the even spacing for named rows.
    """
    ladder = VGroup()
    ladder.rows = {}
    widest = 7 * box + 6 * box * 0.16
    for index, label in enumerate(labels):
        l = pm.L_LETTERS.index(label[-1])
        row = orbital_row(l, None, box=box, gap=box * 0.16)
        y = (heights or {}).get(label, bottom + index * step)
        row.boxes.move_to([x, y, 0])
        tag = eq(label, label_size or cfg.FONT["label"], row.color_name)
        tag.move_to([x - widest / 2 - 0.55, y, 0])
        row.add(tag)
        row.tag = tag
        ladder.add(row)
        ladder.rows[label] = row
    return ladder


def energy_ladder(entries: Sequence[tuple[str, float]], x: float = 0.0, width: float = 3.4,
                  label_size: int | None = None) -> VGroup:
    """Horizontal energy shelves with labels at their left (schematic spacing)."""
    group = VGroup()
    group.shelves, group.labels = {}, {}
    for label, y in entries:
        colour = cfg.BLOCK_COLORS[label[-1]]
        shelf = glow_line([x - width / 2, y, 0], [x + width / 2, y, 0], colour, 3.5)
        tag = eq(label, label_size or cfg.FONT["label"], colour).next_to(shelf, LEFT, buff=0.3)
        group.add(shelf, tag)
        group.shelves[label], group.labels[label] = shelf, tag
    return group


# ----------------------------------------------------------------------------
# Atoms
# ----------------------------------------------------------------------------


def nucleon(color: str, radius: float) -> Circle:
    ball = Circle(radius=radius, stroke_color=interpolate_color(ManimColor(color), ManimColor(cfg.BG), 0.45),
                  stroke_width=1.2, fill_color=color, fill_opacity=1)
    ball.set_sheen(-0.45, UL)
    return ball


def nucleus(protons: int, neutrons: int | None = None, radius: float = 0.13) -> VGroup:
    """A packed nucleus. Protons are orange, neutrons gray, interleaved evenly.

    Neutron counts default to the most common isotope's for the few elements
    the film shows; the picture is a count, not a model of nuclear structure.
    """
    if neutrons is None:
        neutrons = {1: 0, 2: 2, 3: 4, 6: 6, 11: 12, 19: 20, 79: 118}.get(protons, protons)
    total = protons + neutrons
    points = mu.sunflower_points(total, radius * 1.05)
    group = VGroup()
    group.protons, group.neutrons = VGroup(), VGroup()
    for index, point in enumerate(points):
        is_proton = int((index + 1) * protons / total) > int(index * protons / total)
        ball = nucleon(cfg.PROTON_COLOR if is_proton else cfg.NEUTRON_COLOR, radius)
        ball.move_to(point)
        (group.protons if is_proton else group.neutrons).add(ball)
    # Draw from the outside in, so the centre of the cluster sits on top.
    for ball in sorted(group.protons.submobjects + group.neutrons.submobjects,
                       key=lambda m: -np.linalg.norm(m.get_center())):
        group.add(ball)
    return group


def electron_cloud(radius: float, color: str = cfg.ELECTRON_COLOR, opacity: float = 0.2) -> VGroup:
    """A soft, edge-less cloud — where electrons are likely, not a path they follow."""
    return halo(radius, color, layers=8, peak_opacity=opacity)


# ----------------------------------------------------------------------------
# 3D: orbital silhouettes and extruded tiles
# ----------------------------------------------------------------------------

# Mesh resolution (theta, phi) per l. Every face is shaded in Python each frame,
# so these are tuned to look smooth at 1080p without making 3D frames crawl.
MESH: dict[int, tuple[int, int]] = {0: (12, 24), 1: (16, 26), 2: (20, 34), 3: (22, 40)}
# Coarser meshes for small, distant or secondary shapes.
SMALL_MESH: dict[int, tuple[int, int]] = {0: (10, 20), 1: (12, 18), 2: (14, 24), 3: (16, 28)}

# Representative real orbitals for each family: s, p_z, d_xy, f_xyz.
ORBITAL_FAMILY: dict[str, tuple[int, int]] = {"s": (0, 0), "p": (1, 0), "d": (2, -2), "f": (3, -2)}


@lru_cache(maxsize=None)
def _angular_peak(l: int, m: int) -> float:
    theta, phi = np.meshgrid(np.linspace(0, PI, 181), np.linspace(0, TAU, 361))
    return float((mu.real_spherical_harmonic(l, m, theta, phi) ** 2).max())


def orbital_surface(l: int, m: int, size: float = 1.6, resolution: tuple[int, int] | None = None,
                    opacity: float = 0.96) -> Surface:
    """A lit polar surface of the angular density |Y_lm|^2.

    Distance from the centre in each direction is proportional to how likely
    the electron is to be found in that direction. Lobe colour is the sign of
    the real angular function (cyan +, purple −), never electric charge.
    """
    peak = _angular_peak(l, m)
    if resolution is None:
        resolution = MESH[l]

    def point(u: float, v: float) -> np.ndarray:
        r = size * float(mu.real_spherical_harmonic(l, m, u, v) ** 2) / peak
        if l == 0:
            r = size
        return np.array([r * np.sin(u) * np.cos(v), r * np.sin(u) * np.sin(v), r * np.cos(u)])

    surface = Surface(point, u_range=[1e-3, PI - 1e-3], v_range=[0, TAU], resolution=resolution,
                      fill_opacity=opacity, stroke_width=0)
    for face in surface:
        centre = face.get_center()
        colour = cfg.PHASE_POS if mu.direction_sign(l, m, centre) >= 0 else cfg.PHASE_NEG
        # No stroke: Cairo shades and strokes every face separately, and the
        # stroke pass is a third of a 3D frame's cost with no visible benefit.
        face.set_fill(colour, opacity)
        face.set_stroke(width=0)
    surface.orbital_state = (l, m)
    return surface


def family_orbital(letter: str, size: float = 1.6, opacity: float = 0.96, small: bool = False) -> Surface:
    l, m = ORBITAL_FAMILY[letter]
    return orbital_surface(l, m, size, resolution=SMALL_MESH[l] if small else None, opacity=opacity)


def present_3d(mob: Mobject, tilt: float = 62 * DEGREES, turn: float = 25 * DEGREES) -> Mobject:
    """Tilt a 3D object toward the viewer, so the flat front camera sees depth."""
    mob.rotate(turn, axis=OUT)
    mob.rotate(-tilt, axis=RIGHT)
    return mob


def spin_forever(mob: Mobject, rate: float = 0.35, axis=None) -> Mobject:
    """A slow ambient rotation about the object's own (tilted) vertical."""
    spin_axis = np.array([0.0, np.sin(62 * DEGREES), np.cos(62 * DEGREES)]) if axis is None else np.asarray(axis)

    def turn(m: Mobject, dt: float) -> None:
        m.rotate(rate * dt, axis=spin_axis, about_point=m.get_center())

    mob.add_updater(turn)
    return mob


def tile_prism(point, size: float, height: float, color: str, opacity: float = 0.92) -> Prism:
    """An extruded element tile for the 3D skyline shots."""
    prism = Prism(dimensions=[size, size, height], fill_color=color, fill_opacity=opacity,
                  stroke_color=interpolate_color(ManimColor(color), ManimColor(cfg.WHITE), 0.35),
                  stroke_width=0.6)
    prism.move_to(np.asarray(point, dtype=float) + OUT * height / 2)
    return prism


# ----------------------------------------------------------------------------
# Small compositions reused across chapters
# ----------------------------------------------------------------------------


def config_eq(z: int, size: int | None = None, color: str = cfg.WHITE, core: bool = True) -> MathTex:
    """An element's ground configuration, computed by the model."""
    return eq(pm.config_latex(z, core=core), size or cfg.FONT["label"], color)


def arrow_between(start, end, color: str = cfg.MUTED, width: float = 4) -> Arrow:
    return Arrow(start, end, buff=0.1, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def subscribe_card() -> VGroup:
    """The channel's closing card, in the house style."""
    thank_you = txt("THANK YOU FOR WATCHING", 40, cfg.CYAN)
    subscribe = Text("SUBSCRIBE", font_size=96, color=cfg.GOLD, weight=BOLD)
    subscribe.set_stroke("#351F05", width=3, opacity=0.75, background=True)
    rule = Line(LEFT * 3.4, RIGHT * 3.4, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(
        txt("Stay curious.", 44, cfg.WHITE),
        txt("Next: periodic trends", 36, cfg.CYAN),
    ).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "np"]
