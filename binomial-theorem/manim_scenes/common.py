"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
final synthesis reads as a conclusion rather than a new picture:

* a **bracket** ``(a+b)`` is a *choice machine*: a rounded panel with two round
  doors, a (blue) and b (rose). Exactly one door opens per term;
* a **choice list** is a row of letter cells — outlined blue for a, filled rose for b;
* a **term** is coloured LaTeX: gold coefficient, blue power of a, rose power of b;
* a **coefficient** is always gold, and so is every number in Pascal's triangle;
* a **path** is a glowing polyline down the triangle: left steps blue, right rose;
* a **pile** is a stack of choice lists with a gold count beneath it.

Every coefficient comes from ``utils.math_utils``, which finds it by expanding
the brackets as choice lists; nothing numeric is typed into a scene file.
Scene files compose these pieces and choreograph them against the beats in
``narration.py``.
"""

from __future__ import annotations

from collections.abc import Sequence

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


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Hold the composition steady; live updaters keep moving."""
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
    scene.stop_ambient_camera_rotation()
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


# ----------------------------------------------------------------------------
# Background
# ----------------------------------------------------------------------------


def add_background(scene: Scene) -> VGroup:
    """A faint, static Oceanic bubble layer shared by every chapter.

    There is no flat backdrop rectangle: in a 3D chapter the camera draws flat
    mobjects after the depth-sorted solids, so a backdrop would paint over the
    cube. The camera's background colour does that job instead.
    """
    for mob in scene.mobjects:
        if getattr(mob, "_is_project_background", False):
            return mob
    bubbles = cfg.oceanic_bubbles()
    for part in bubbles.family_members_with_points():
        part.set_fill(opacity=float(part.get_fill_opacity()) * 0.45)
        part.set_stroke(opacity=float(part.get_stroke_opacity()) * 0.45)
    bubbles._is_project_background = True
    bubbles.set_z_index(-10)
    scene.add(bubbles)
    hud(scene, bubbles)
    return bubbles


# ----------------------------------------------------------------------------
# Type
# ----------------------------------------------------------------------------


def txt(body: str, size: int | None = None, color: str = cfg.WHITE, weight=BOLD) -> Text:
    """Bold text with a dark outline, so it stays crisp over any glow."""
    result = Text(body, font_size=size or cfg.FONT["body"], color=color, weight=weight)
    result.set_stroke(cfg.BG, width=1.5, opacity=0.85, background=True)
    return result


# Computer Modern sets visibly smaller than Lato at the same nominal
# size; this factor makes ``eq(x, 40)`` read as large as ``txt(y, 40)``.
MATH_SCALE = 1.35

ROLE_COLORS: dict[str, str] = {
    "coef": cfg.COEF_COLOR,
    "a": cfg.A_COLOR,
    "b": cfg.B_COLOR,
    "op": cfg.WHITE,
    "muted": cfg.MUTED,
    "limit": cfg.LIMIT_COLOR,
    "ok": cfg.GREEN,
}


def eq(latex: str, size: int | None = None, color: str = cfg.WHITE, **kwargs) -> MathTex:
    """An equation with the same dark outline as the captions, sized like text."""
    result = MathTex(latex, font_size=(size or cfg.FONT["section"]) * MATH_SCALE, color=color, **kwargs)
    result.set_stroke(cfg.BG, width=1.2, opacity=0.85, background=True)
    return result


def colored_tex(parts: Sequence[tuple[str, str]], size: int | None = None) -> MathTex:
    """One typeset line from (tex, role) pieces, each piece coloured by its role.

    Typesetting the pieces together keeps a common baseline; ``.pieces[i]`` is
    the glyph group of piece ``i`` and ``.roles[i]`` its role.
    """
    result = MathTex(*[tex for tex, _ in parts], font_size=(size or cfg.FONT["section"]) * MATH_SCALE)
    for piece, (_, role) in zip(result.submobjects, parts):
        piece.set_color(ROLE_COLORS[role])
    result.set_stroke(cfg.BG, width=1.2, opacity=0.85, background=True)
    result.pieces = list(result.submobjects)
    result.roles = [role for _, role in parts]
    return result


def term_tex(coefficient: int | str, a_exp: int, b_exp: int, size: int | None = None,
             show_one: bool = False) -> MathTex:
    """A single coloured term such as 10 a^3 b^2 (a coefficient of 1 is unwritten)."""
    letters = [p for p in mu.term_parts(1, a_exp, b_exp) if p[1] != "coef"]
    if isinstance(coefficient, str) or coefficient != 1 or show_one or not letters:
        return colored_tex([(str(coefficient), "coef")] + letters, size)
    return colored_tex(letters, size)


def lhs_parts(n: int | str, sep: str = "=") -> list[tuple[str, str]]:
    """(a + b)^n = as coloured pieces."""
    parts = [("(", "op"), ("a", "a"), ("+", "op"), ("b", "b"), (f")^{{{n}}}", "op")]
    if sep:
        parts.append((sep, "op"))
    return parts


def expansion_tex(n: int, size: int | None = None, *, lhs: bool = True,
                  coefs: Sequence[str] | None = None, max_width: float = 14.4) -> MathTex:
    """(a+b)^n = ... with every term coloured; coefficients from the model.

    ``coefs`` replaces the printed coefficients (for example with "?"), and
    then every term shows one, including the 1s. Attributes: ``.terms[k]``,
    ``.coefs[k]`` (None where a 1 is unwritten), ``.pluses``, ``.lhs``.
    """
    parts: list[tuple[str, str]] = lhs_parts(n) if lhs else []
    lhs_count = len(parts)
    term_slices: list[list[int]] = []
    plus_index: list[int] = []
    for k, c in enumerate(mu.coefficients(n)):
        if k:
            plus_index.append(len(parts))
            parts.append(("+", "op"))
        pieces = mu.term_parts(c, n - k, k)
        if coefs is not None:
            pieces = [(coefs[k], "coef")] + [p for p in pieces if p[1] != "coef"]
        term_slices.append(list(range(len(parts), len(parts) + len(pieces))))
        parts.extend(pieces)
    result = colored_tex(parts, size)
    fit_width(result, max_width)
    pieces = result.pieces
    result.lhs = VGroup(*pieces[:lhs_count])
    result.terms = [VGroup(*[pieces[i] for i in indices]) for indices in term_slices]
    result.coefs = [pieces[indices[0]] if result.roles[indices[0]] == "coef" else None
                    for indices in term_slices]
    result.pluses = [pieces[i] for i in plus_index]
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
    """Chapter caption: bold gold type with a soft offset shadow and glow, top of frame."""
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
    """A rounded pill with a label."""
    label = txt(body, size or cfg.FONT["small"], color)
    pill = RoundedRectangle(
        width=label.width + 0.6, height=label.height + 0.36, corner_radius=0.22,
        stroke_color=color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.92,
    )
    group = VGroup(pill, label.move_to(pill))
    group.pill, group.label = pill, label
    return group


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


def glow_dot(point=ORIGIN, radius: float = 0.11, color: str = cfg.CYAN) -> VGroup:
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


def glow_line(start, end, color: str, width: float = 5) -> VGroup:
    return VGroup(
        Line(start, end, stroke_color=color, stroke_width=width * 4, stroke_opacity=0.12),
        Line(start, end, stroke_color=color, stroke_width=width * 2, stroke_opacity=0.25),
        Line(start, end, stroke_color=color, stroke_width=width),
    )


def check_mark(size: float = 0.32, color: str = cfg.GREEN) -> VMobject:
    mark = VMobject(stroke_color=color, stroke_width=8)
    mark.set_points_as_corners([LEFT * size + UP * 0.05, DOWN * size * 0.75 + LEFT * size * 0.15, RIGHT * size + UP * size])
    return mark


def arrow_between(start, end, color: str = cfg.MUTED, width: float = 5) -> Arrow:
    return Arrow(start, end, buff=0.1, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def count_brace(mob: Mobject, label: str | int, color: str = cfg.GOLD, direction=DOWN,
                size: int | None = None) -> VGroup:
    """A brace with a big label: the film's single way of showing 'this many'."""
    brace = Brace(mob, direction=direction, color=color, buff=0.12)
    tag = txt(str(label), size or cfg.FONT["section"], color)
    tag.next_to(brace, direction, buff=0.12)
    group = VGroup(brace, tag)
    group.brace, group.label = brace, tag
    return group


# ----------------------------------------------------------------------------
# Brackets as choice machines
# ----------------------------------------------------------------------------


class ChoiceMachine(VGroup):
    """One bracket (a + b): a panel with an a-door and a b-door.

    ``choose(letter)`` opens one door (it glows; the other dims) and is
    animatable: ``machine.animate.choose("b")``. ``reset()`` closes both.
    """

    def __init__(self, index: int | None = None, width: float = 2.3, height: float = 1.45,
                 door: float = 0.45, show_index: bool = False) -> None:
        super().__init__()
        self.body = RoundedRectangle(width=width, height=height, corner_radius=0.3,
                                     stroke_color=cfg.CYAN, stroke_width=3.5,
                                     fill_color=cfg.PANEL, fill_opacity=0.92)
        self.doors: dict[str, VGroup] = {}
        for letter, side in (("a", LEFT), ("b", RIGHT)):
            colour = ROLE_COLORS[letter]
            ring = Circle(radius=door, stroke_color=colour, stroke_width=4,
                          fill_color=colour, fill_opacity=0.12)
            label = eq(letter, cfg.FONT["section"], colour)
            label.scale_to_fit_height(door * 0.9)
            group = VGroup(ring, label).move_to(side * width * 0.24)
            group.ring, group.label = ring, label
            self.doors[letter] = group
        self.add(self.body, self.doors["a"], self.doors["b"])
        self.index = index
        self.tag = None
        if show_index and index is not None:
            self.tag = txt(str(index), cfg.FONT["tiny"], cfg.MUTED).next_to(self.body, DOWN, buff=0.16)
            self.add(self.tag)
        self.choice: str | None = None

    def choose(self, letter: str) -> ChoiceMachine:
        for name, door in self.doors.items():
            colour = ROLE_COLORS[name]
            if name == letter:
                door.ring.set_fill(colour, 0.92).set_stroke(cfg.WHITE, 4, 1)
                door.label.set_color(cfg.BG).set_opacity(1)
            else:
                door.ring.set_fill(colour, 0.04).set_stroke(colour, 3, cfg.CONTEXT_OPACITY)
                door.label.set_color(colour).set_opacity(cfg.CONTEXT_OPACITY)
        self.body.set_stroke(ROLE_COLORS[letter], 4.5, 1)
        self.choice = letter
        return self

    def reset(self) -> ChoiceMachine:
        for name, door in self.doors.items():
            colour = ROLE_COLORS[name]
            door.ring.set_fill(colour, 0.12).set_stroke(colour, 4, 1)
            door.label.set_color(colour).set_opacity(1)
        self.body.set_stroke(cfg.CYAN, 3.5, 1)
        self.choice = None
        return self


def machine_row(n: int = 5, width: float = 2.3, gap: float = 0.42, y: float = 1.2,
                show_index: bool = False, height: float = 1.45, door: float = 0.45) -> VGroup:
    """n brackets side by side — (a+b)^n as n independent choices."""
    row = VGroup(*[ChoiceMachine(i + 1, width, height, door, show_index) for i in range(n)])
    row.arrange(RIGHT, buff=gap).move_to(UP * y)
    return row


def set_word(machines: VGroup, word: str) -> VGroup:
    """Make each machine choose the matching letter of ``word`` (instantly)."""
    for machine, letter in zip(machines, word):
        machine.choose(letter)
    return machines


# ----------------------------------------------------------------------------
# Choice lists
# ----------------------------------------------------------------------------


def choice_cell(letter: str, size: float = 0.62, glyph: str | None = None) -> VGroup:
    """One letter of a choice list. b cells are bright, so the b's pop out.

    ``glyph`` relabels the cell (H for a, T for b on a coin) without changing
    its colour, which always follows the underlying letter.
    """
    colour = ROLE_COLORS[letter]
    is_b = letter == "b"
    box = RoundedRectangle(width=size, height=size, corner_radius=size * 0.2,
                           stroke_color=colour, stroke_width=max(1.6, 4 * size),
                           fill_color=colour, fill_opacity=0.88 if is_b else 0.14)
    mark = MathTex(glyph or letter, color=cfg.BG if is_b else colour)
    mark.scale_to_fit_height(size * 0.46 * (1.15 if glyph else 1))
    mark.move_to(box)
    # A glyph belongs to its choice tile, rather than being a free caption.
    # The layout audit still rejects overlaps, but uses tile spacing instead
    # of caption breathing room for the compact 32-list grids.
    mark._tile_label = True
    cell = VGroup(box, mark)
    cell.box, cell.glyph, cell.letter = box, mark, letter
    return cell


COIN_GLYPHS = {"a": r"\mathrm{H}", "b": r"\mathrm{T}"}


def choice_list(word: str, size: float = 0.62, gap: float | None = None, glyphs: dict | None = None) -> VGroup:
    """A choice list such as a a b a b, drawn as a row of cells (``glyphs=COIN_GLYPHS`` for flips)."""
    row = VGroup(*[choice_cell(letter, size, (glyphs or {}).get(letter)) for letter in word])
    row.arrange(RIGHT, buff=size * 0.16 if gap is None else gap)
    row.word = word
    return row


def product_of(word: str, size: int | None = None) -> MathTex:
    """The single term a choice list multiplies to, e.g. a^3 b^2 for aabab."""
    k = word.count("b")
    return term_tex(1, len(word) - k, k, size)


# ----------------------------------------------------------------------------
# Pascal's triangle and paths
# ----------------------------------------------------------------------------


def pascal_point(n: int, k: int, pitch_x: float = 1.15, pitch_y: float = 0.82, top=UP * 2.7) -> np.ndarray:
    """Screen position of entry (n, k): row n, k places from the left."""
    return np.asarray(top, dtype=float) + np.array([(k - n / 2) * pitch_x, -n * pitch_y, 0.0])


def pascal_triangle(rows: int, pitch_x: float = 1.15, pitch_y: float = 0.82, top=UP * 2.7,
                    size: int | None = None, color: str = cfg.GOLD) -> VGroup:
    """Rows 0..rows-1, every number built by addition in ``utils.math_utils``."""
    triangle = VGroup()
    triangle.entries = {}
    triangle.pitch = (pitch_x, pitch_y)
    triangle.top = np.asarray(top, dtype=float)
    for n, row in enumerate(mu.pascal_rows(rows)):
        for k, value in enumerate(row):
            entry = txt(str(value), size or cfg.FONT["body"], color)
            entry.move_to(pascal_point(n, k, pitch_x, pitch_y, top))
            triangle.add(entry)
            triangle.entries[(n, k)] = entry
    return triangle


def triangle_row(triangle: VGroup, n: int) -> VGroup:
    return VGroup(*[triangle.entries[(n, k)] for k in range(n + 1)])


def peg(point, radius: float = 0.07, color: str = cfg.MUTED) -> VGroup:
    return VGroup(Circle(radius=radius * 2.2, stroke_width=0, fill_color=color, fill_opacity=0.12),
                  Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=0.9)).move_to(point)


def path_line(word: str, point_of, width: float = 6, opacity: float = 1.0) -> VGroup:
    """A route down the triangle: one glowing segment per step, coloured by its letter."""
    cells = mu.path_cells(word)
    segments = VGroup()
    for (n0, k0), (n1, k1), letter in zip(cells, cells[1:], word):
        segment = glow_line(point_of(n0, k0), point_of(n1, k1), ROLE_COLORS[letter], width)
        segment.set_opacity(opacity)
        segments.add(segment)
    segments.word = word
    return segments


def bounce_path(word: str, point_of, hop: float = 0.28) -> VMobject:
    """A ball's route: a small arc from each peg to the next, like a bounce."""
    cells = mu.path_cells(word)
    curve = VMobject()
    curve.start_new_path(point_of(*cells[0]))
    for (n0, k0), (n1, k1) in zip(cells, cells[1:]):
        a, b = point_of(n0, k0), point_of(n1, k1)
        mid = (a + b) / 2 + UP * hop
        curve.add_quadratic_bezier_curve_to(mid, b)
    return curve


# ----------------------------------------------------------------------------
# Coins and bars
# ----------------------------------------------------------------------------


def coin(face: str, radius: float = 0.55) -> VGroup:
    """A coin: H is blue (it plays the role of a), T is rose (it plays b)."""
    colour = cfg.A_COLOR if face == "H" else cfg.B_COLOR
    rim = Circle(radius=radius, stroke_color=colour, stroke_width=5, fill_color=cfg.PANEL_2, fill_opacity=1)
    inner = Circle(radius=radius * 0.8, stroke_color=colour, stroke_width=2, stroke_opacity=0.5, fill_opacity=0)
    letter = txt(face, cfg.FONT["section"], colour)
    letter.scale_to_fit_height(radius * 0.85).move_to(rim)
    group = VGroup(halo(radius * 1.5, colour, peak_opacity=0.1), rim, inner, letter)
    group.letter = letter
    return group


def bar_set(values: Sequence[float], unit: float, width: float = 0.8, gap: float = 0.2,
            baseline=DOWN * 3.0, colors: Sequence[str] | None = None, opacity: float = 0.85) -> VGroup:
    """Vertical bars standing on a common baseline, centred on x = 0."""
    bars = VGroup()
    count = len(values)
    for index, value in enumerate(values):
        colour = colors[index] if colors else cfg.GOLD
        bar = Rectangle(width=width, height=max(value * unit, 1e-3), stroke_color=colour, stroke_width=2.5,
                        fill_color=colour, fill_opacity=opacity)
        x = (index - (count - 1) / 2) * (width + gap)
        bar.move_to(np.asarray(baseline, dtype=float) + np.array([x, bar.height / 2, 0]))
        bars.add(bar)
    return bars


def mix_color(k: int, n: int) -> ManimColor:
    """Blue for all a, rose for all b, and the honest mix in between."""
    return interpolate_color(ManimColor(cfg.A_COLOR), ManimColor(cfg.B_COLOR), k / n if n else 0)


# ----------------------------------------------------------------------------
# 3D
# ----------------------------------------------------------------------------


def block(dims: Sequence[float], color, opacity: float = 0.9) -> Prism:
    """A solid box for the cube of a + b; its outline is a lighter tint of its colour."""
    edge = interpolate_color(ManimColor(color), ManimColor(cfg.WHITE), 0.45)
    return Prism(dimensions=list(dims), fill_color=color, fill_opacity=opacity,
                 stroke_color=edge, stroke_width=1.2)


# ----------------------------------------------------------------------------
# Closing card
# ----------------------------------------------------------------------------


def subscribe_card() -> VGroup:
    """The channel's closing card, in the house style, sized for a phone."""
    thank_you = txt("THANK YOU FOR WATCHING", 40, cfg.CYAN)
    subscribe = Text("SUBSCRIBE", font_size=96, color=cfg.GOLD, weight=BOLD)
    subscribe.set_stroke("#351F05", width=3, opacity=0.75, background=True)
    rule = Line(LEFT * 3.4, RIGHT * 3.4, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(
        txt("Stay curious.", 44, cfg.WHITE),
        txt("Keep following the physics and mathematics.", 36, cfg.WHITE),
    ).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.set_stroke("#06131B", width=4, opacity=0.9, background=True)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "mu", "pm", "np"]
