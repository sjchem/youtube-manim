"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing synthesis reads as a conclusion rather than a new picture:

* a **Lewis structure** is flat type on the screen: element letters, white
  bond lines, muted dots for outer lone pairs and **purple** dots for lone
  pairs on the central atom;
* a **molecule** is a ball-and-stick model on a turning 3D ``Stage``
  (``stage3d.py``), coloured close to the CPK convention;
* a **bonding electron region** is a translucent **cyan** lobe; a **lone
  pair** is a fatter, shorter **purple** lobe — present, space-filling, and
  never mistaken for an atom. Showing the electron geometry means showing
  the lobes; showing the molecular shape means fading the purple ones away;
* **angles** are gold arcs with gold values; crowded 90-degree contacts are
  red; a revealed shape name is green;
* **orbitals** are computed |psi| surfaces: blue where the wave function is
  positive, rose where it is negative, purple for p orbitals left out of a
  hybrid set;
* **dipoles** are orange arrows along bonds, and their sum is a green arrow.

Scene files compose these pieces and choreograph them against the beats in
``narration.py``; nothing in a scene file should invent a second way to draw
one of these ideas, or type a number that the data modules can supply.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

import numpy as np
from manim import *

import config as cfg
from manim_scenes.stage3d import (AngleArc, Ball, Blob, Body, Face, Halo, Lobe, Overlay, Param, Rod, Segment, Stage,
                                  Tag, Vector)
from narration import SCRIPT
from utils import geometry_data as gd
from utils import math_utils as mu
from utils import molecule_library as ml
from utils import orbital_models as om
from utils import physics_models as pm
from utils.render_helpers import fit_inside, fit_to_safe_frame, fit_width


# ----------------------------------------------------------------------------
# Scene lifecycle
# ----------------------------------------------------------------------------


def _leaf_animations(animations):
    for animation in animations:
        if isinstance(animation, AnimationGroup):
            yield from _leaf_animations(animation.animations)
        else:
            yield animation


def prepare_scene(scene: Scene) -> None:
    """Teach the scene two things it needs for live stages.

    1. AnimationGroup / LaggedStart normally add a *second*, top-level copy of
       their members to the scene; look through groups to the leaf animations
       instead, so nothing is drawn twice.
    2. Cairo freezes a flattened list of moving mobjects when a play starts.
       A stage re-sorts its children by depth every frame, so whenever a stage
       is on screen the scene renders its top-level mobjects each frame and
       the camera walks the current draw tree.
    """
    if getattr(scene, "_prepared_for_stages", False):
        return
    add_from = scene.add_mobjects_from_animations
    moving = scene.get_moving_mobjects
    scene.add_mobjects_from_animations = lambda animations: add_from(list(_leaf_animations(animations)))
    scene.get_moving_mobjects = lambda *animations: moving(*_leaf_animations(animations))
    partition = scene.get_moving_and_static_mobjects

    def live_partition(animations):
        if any(getattr(member, "_live_draw_order", False) for member in scene.mobjects):
            return list(scene.mobjects), []
        return partition(animations)

    scene.get_moving_and_static_mobjects = live_partition
    scene._prepared_for_stages = True


def start(scene: Scene, key: str, title: str | None = None) -> tuple[float, VGroup | None]:
    """Theme the scene, add the quiet background, and show the chapter heading."""
    prepare_scene(scene)
    cfg.apply_project_theme(scene, bubbles=False)
    scene._project_scene_key = key
    add_background(scene)
    started = float(scene.time)
    from utils.voiceover import attach_voiceover

    attach_voiceover(scene, key)
    head = None
    if title:
        head = heading(title)
        scene.play(FadeIn(head, shift=DOWN * 0.18), run_time=0.6)
    return started, head


def dismiss_opening_title(scene: Scene, started_at: float, head: VGroup | None, at: float = 3.4) -> None:
    """Clear an opening title around four seconds into the chapter."""
    if head is None:
        return
    if float(scene.time) - started_at < at:
        cue(scene, started_at, at)
    scene.play(FadeOut(head), run_time=0.6)


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Hold the composition; live stages keep turning."""
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
    cue(scene, started_at, SCRIPT[scene._project_scene_key][index][0])


def end_scene(scene: Scene, started_at: float, target_seconds: float) -> None:
    """Finish on the configured frame boundary and fade everything out."""
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
        for member in mob.get_family():
            member.clear_updaters()
    if visible:
        scene.play(FadeOut(*visible), run_time=fade_frames / fps)
        scene.remove(*visible)
    else:
        scene.wait(fade_frames / fps)


def add_background(scene: Scene) -> VGroup:
    """A faint, static Oceanic bubble layer shared by every chapter."""
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
    return bubbles


def show(scene: Scene, stage: Stage, run_time: float = 1.0, *others: Animation) -> None:
    """Bring a stage in by fading its own presence (never FadeIn a live stage)."""
    stage.presence = 0.0
    stage.refresh()
    scene.add(stage)
    scene.play(stage.fade(stage, 1.0), *others, run_time=run_time)


def hide(scene: Scene, stage: Stage, run_time: float = 0.8, *others: Animation) -> None:
    scene.play(stage.fade(stage, 0.0), *others, run_time=run_time)
    scene.remove(stage)


# ----------------------------------------------------------------------------
# Type
# ----------------------------------------------------------------------------


def txt(body: str, size: int | None = None, color: str = cfg.WHITE, weight=BOLD, font: str | None = None) -> Text:
    """Bold text with a dark outline, so it stays crisp over any glow."""
    kwargs = {"font": font} if font else {}
    result = Text(body, font_size=size or cfg.FONT["body"], color=color, weight=weight, **kwargs)
    result.set_stroke(cfg.BG, width=0.75, opacity=0.85, background=True)
    return result


# Computer Modern sets visibly smaller than Lato at the same nominal size.
MATH_SCALE = 1.35


def eq(latex: str | Sequence[str], size: int | None = None, color: str = cfg.WHITE, **kwargs) -> MathTex:
    """An equation with the same dark outline as the captions, sized like text."""
    parts = [latex] if isinstance(latex, str) else list(latex)
    result = MathTex(*parts, font_size=(size or cfg.FONT["section"]) * MATH_SCALE, color=color, **kwargs)
    result.set_stroke(cfg.BG, width=0.65, opacity=0.85, background=True)
    return result


def decorative(mob: Mobject) -> Mobject:
    """Mark a glow or shadow copy so the layout audit does not read it as text."""
    for member in mob.get_family():
        member._is_decorative = True
    return mob


def heading(title: str, color: str = cfg.GOLD, size: int = 48) -> VGroup:
    """Chapter caption: bold gold type with a soft offset shadow, top of frame."""
    main = txt(title, size, color)
    fit_width(main, 13.6)
    shadow = main.copy().set_color(cfg.BG).set_opacity(0.85).shift(RIGHT * 0.05 + DOWN * 0.05)
    shadow.set_stroke(width=0)
    decorative(shadow)
    group = VGroup(shadow, main)
    group.move_to(UP * 3.86)
    group.main = main
    return group


def caption(body: str, color: str = cfg.WHITE, size: int | None = None, y: float = -3.72) -> Text:
    """A short bottom caption, on a phone-readable size."""
    line = txt(body, size or cfg.FONT["body"], color)
    fit_width(line, 13.4)
    return line.move_to(UP * y)


def top_caption(body: str, color: str = cfg.WHITE, size: int | None = None) -> Text:
    return caption(body, color, size or cfg.FONT["body"], y=3.62)


def swap(scene: Scene, old: Mobject | None, new: Mobject | None, run_time: float = 0.7) -> Mobject | None:
    """Fade one caption out completely before the next fades in (no ghosted words)."""
    anims = []
    if old is not None:
        anims.append(FadeOut(old, rate_func=lambda a: smooth(min(a / 0.45, 1.0))))
    if new is not None:
        anims.append(FadeIn(new, rate_func=lambda a: smooth(max((a - 0.55) / 0.45, 0.0))))
    if anims:
        scene.play(*anims, run_time=run_time)
    if old is not None:
        scene.remove(old)
    return new


def fade_through(old: Mobject, new: Mobject) -> AnimationGroup:
    """Old caption fully out before the new one comes in, as one animation
    that can share a play with other motion. Remove ``old`` afterwards."""
    return AnimationGroup(FadeOut(old, rate_func=lambda a: smooth(min(a / 0.45, 1.0))),
                          FadeIn(new, rate_func=lambda a: smooth(max((a - 0.55) / 0.45, 0.0))))


def chip(body: str, color: str = cfg.CYAN, size: int | None = None, fill: str = cfg.PANEL) -> VGroup:
    """A rounded pill with a label."""
    label = txt(body, size or cfg.FONT["small"], color)
    pill = RoundedRectangle(width=label.width + 0.6, height=label.height + 0.36, corner_radius=0.22,
                            stroke_color=color, stroke_width=3, fill_color=fill, fill_opacity=0.92)
    group = VGroup(pill, label.move_to(pill))
    group.pill, group.label = pill, label
    return group


def eq_chip(latex: str | Sequence[str], color: str = cfg.WHITE, size: int | None = None,
            stroke: str | None = None) -> VGroup:
    """A rounded pill holding an equation."""
    label = eq(latex, size or cfg.FONT["label"], color)
    pill = RoundedRectangle(width=label.width + 0.7, height=label.height + 0.4, corner_radius=0.22,
                            stroke_color=stroke or color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.92)
    group = VGroup(pill, label.move_to(pill))
    group.pill, group.label = pill, label
    return group


def panel(width: float, height: float, color: str = cfg.MUTED, opacity: float = 0.78) -> RoundedRectangle:
    return RoundedRectangle(width=width, height=height, corner_radius=0.22, stroke_color=color, stroke_width=2,
                            stroke_opacity=0.6, fill_color=cfg.PANEL, fill_opacity=opacity)


def glow_frame(mob: Mobject, color: str = cfg.GOLD, buff: float = 0.14, width: float = 4) -> VGroup:
    """A glowing rounded outline around anything — the film's 'look here'."""
    w, h = mob.width + 2 * buff, mob.height + 2 * buff
    group = VGroup()
    for spread, opacity in ((14, 0.10), (8, 0.18), (width, 1.0)):
        group.add(RoundedRectangle(width=w, height=h, corner_radius=min(0.2, h / 3), stroke_color=color,
                                   stroke_width=spread, stroke_opacity=opacity, fill_opacity=0))
    return group.move_to(mob)


def title_card(big: str, small: str, color: str = cfg.GOLD, small_first: bool = False) -> VGroup:
    """The film's title: a big warm line and a smaller cyan one, with an outline,
    an offset shadow and a soft glow."""
    line_one = Text(big, font=cfg.TITLE_FONT, weight=BOLD, font_size=96, color=color)
    line_two = Text(small, font=cfg.TITLE_FONT, weight=BOLD, font_size=56, color=cfg.CYAN)
    title = VGroup(line_two, line_one) if small_first else VGroup(line_one, line_two)
    title.arrange(DOWN, buff=0.3)
    fit_width(title, 13.4)
    line_one.set_stroke("#351F05", width=4, opacity=0.8, background=True)
    line_two.set_stroke("#06131B", width=3, opacity=0.8, background=True)
    shadow = title.copy().set_color(cfg.BG).set_opacity(0.9).shift(RIGHT * 0.09 + DOWN * 0.09)
    shadow.set_stroke(width=0)
    decorative(shadow)
    glow = line_one.copy().set_opacity(0.12).set_stroke(color, width=18, opacity=0.12)
    decorative(glow)
    card = VGroup(shadow, glow, title)
    card.title, card.shadow, card.glow = title, shadow, glow
    return card


def shape_name(name: str, color: str = cfg.RESULT, size: int | None = None) -> VGroup:
    """A revealed shape name: green type with a soft glow behind it."""
    label = txt(name, size or cfg.FONT["section"], color)
    glow = label.copy().set_stroke(color, width=14, opacity=0.16).set_fill(opacity=0)
    decorative(glow)
    group = VGroup(glow, label)
    group.label = label
    return group


def axe_eq(bonds: int, lone: int, size: int | None = None) -> MathTex:
    """The AXmEn code, colour-coded: A white, X cyan (bonded atoms), E purple (lone pairs)."""
    parts = ["A", "X" if bonds == 1 else f"X_{{{bonds}}}"]
    if lone:
        parts.append("E" if lone == 1 else f"E_{{{lone}}}")
    result = eq(parts, size or cfg.FONT["section"])
    result[0].set_color(cfg.WHITE)
    result[1].set_color(cfg.DOMAIN_COLOR)
    if lone:
        result[2].set_color(cfg.LONE_PAIR_COLOR)
    return result


def degrees_label(value: float, size: int | None = None, color: str = cfg.ANGLE_COLOR, digits: int = 1) -> Text:
    """An angle value such as '104.5°' (whole numbers drop the decimal)."""
    text = f"{value:.{digits}f}".rstrip("0").rstrip(".") if digits else f"{value:.0f}"
    return txt(f"{text}°", size or cfg.FONT["label"], color)


def formula(key: str, size: int | None = None, color: str = cfg.WHITE) -> MathTex:
    return eq(ml.molecule(key).formula if key in ml.BUILDERS else key, size or cfg.FONT["body"], color)


# ----------------------------------------------------------------------------
# Marks and glows
# ----------------------------------------------------------------------------


def halo(radius: float, color: str, layers: int = 6, peak_opacity: float = 0.14) -> VGroup:
    group = VGroup()
    for index in range(layers):
        frac = (index + 1) / layers
        group.add(Circle(radius=radius * (0.35 + 0.65 * frac), stroke_width=0, fill_color=color,
                         fill_opacity=peak_opacity * (1.15 - frac)))
    return group


def check_mark(size: float = 0.32, color: str = cfg.GREEN) -> VMobject:
    mark = VMobject(stroke_color=color, stroke_width=9)
    mark.set_points_as_corners([LEFT * size + UP * 0.05, DOWN * size * 0.75 + LEFT * size * 0.15, RIGHT * size + UP * size])
    return mark


def cross_mark(size: float = 0.3, color: str = cfg.RED) -> VGroup:
    return VGroup(Line(UL * size, DR * size, stroke_color=color, stroke_width=10),
                  Line(UR * size, DL * size, stroke_color=color, stroke_width=10))


def glow_arrow(start, end, color: str, width: float = 6, tip: float = 0.28) -> VGroup:
    under = Line(start, end, stroke_color=color, stroke_width=width * 3.2, stroke_opacity=0.16)
    arrow = Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=tip,
                  max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)
    return VGroup(under, arrow)


# ----------------------------------------------------------------------------
# Lewis structures (flat, on purpose)
# ----------------------------------------------------------------------------

LEWIS_DOT = 0.08
LEWIS_GAP = 0.17


def dot_pair(centre, direction_deg: float, distance: float, color: str, radius: float = LEWIS_DOT,
             gap: float = LEWIS_GAP) -> VGroup:
    """Two electron dots side by side, ``distance`` from ``centre`` along an angle."""
    d = np.array([np.cos(np.radians(direction_deg)), np.sin(np.radians(direction_deg)), 0.0])
    side = np.array([-d[1], d[0], 0.0])
    spot = np.asarray(centre, dtype=float) + d * distance
    dots = VGroup(*[Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=1).move_to(spot + side * s * gap / 2 * 2)
                    for s in (-0.5, 0.5)])
    return dots


class Lewis(VGroup):
    """A Lewis structure: ligands at given screen angles around a central symbol.

    ``ligands``: (symbol, angle in degrees, bond order). ``central_lone``:
    angles of the central atom's lone pairs (drawn purple). Outer atoms get
    their lone pairs (muted) unless ``outer=False``.
    """

    def __init__(self, central: str, ligands: Sequence[tuple[str, float, int]], central_lone: Sequence[float] = (),
                 *, at=ORIGIN, bond: float = 2.3, size: int = 100, ligand_size: int = 84, outer: bool = True) -> None:
        super().__init__()
        at = np.asarray(at, dtype=float)

        def clearance(label, direction, padding):
            # Exit the actual glyph bounds along this ray before drawing a
            # bond or lone pair. Fixed radii clipped large O and two-letter Br.
            limits = [half / abs(component) for half, component in
                      ((label.width / 2, direction[0]), (label.height / 2, direction[1]))
                      if abs(component) > 1e-8]
            return min(limits) + padding
        self.anchor_point = at
        self.center_symbol = txt(central, size, cfg.WHITE)
        self.center_symbol.move_to(at)
        self.ligand_symbols, self.bond_lines, self.outer_dots, self.positions = [], [], [], []
        self.add(self.center_symbol)
        for symbol, angle, order in ligands:
            d = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0.0])
            spot = at + d * bond
            label = txt(symbol, ligand_size, cfg.WHITE).move_to(spot)
            self.ligand_symbols.append(label)
            self.positions.append(spot)
            inner = at + d * max(0.56, clearance(self.center_symbol, d, 0.12))
            outer_end = spot - d * max(0.44 if symbol == "H" else 0.5, clearance(label, d, 0.12))
            side = np.array([-d[1], d[0], 0.0])
            offsets = [0.0] if order == 1 else ([-0.11, 0.11] if order == 2 else [-0.18, 0.0, 0.18])
            lines = VGroup(*[Line(inner + side * o, outer_end + side * o, stroke_color=cfg.WHITE, stroke_width=8)
                             for o in offsets])
            self.bond_lines.append(lines)
            self.add(lines, label)
            if outer and symbol != "H":
                pairs = (8 - 2 * order) // 2
                spread = {1: [0.0], 2: [-60.0, 60.0], 3: [-90.0, 0.0, 90.0]}.get(pairs, [])
                dots = VGroup(*[dot_pair(spot, angle + s, max(0.56, clearance(label,
                    np.array([np.cos(np.radians(angle + s)), np.sin(np.radians(angle + s)), 0]), 0.2)), cfg.MUTED) for s in spread])
                self.outer_dots.append(dots)
                self.add(dots)
            else:
                self.outer_dots.append(VGroup())
        self.lone_dots = VGroup(*[dot_pair(at, angle, max(0.68, clearance(self.center_symbol,
            np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0]), 0.24)),
            cfg.LONE_PAIR_COLOR, radius=0.1, gap=0.21)
                                  for angle in central_lone])
        self.add(self.lone_dots)

    def bonds(self) -> VGroup:
        return VGroup(*self.bond_lines)


# ----------------------------------------------------------------------------
# Molecules on a stage
# ----------------------------------------------------------------------------

BOND = 2.5                # display bond length (screen units at zoom 1)
DOMAIN_LENGTH = 2.35       # a bonding region lobe
DOMAIN_WIDTH = 0.44
LONE_LENGTH = 1.75         # a lone-pair lobe: shorter and fatter
LONE_WIDTH = 0.72


def element_ball(symbol: str, pos, *, label: bool = True, scale: float = 1.0) -> Ball:
    return Ball(pos, cfg.ELEMENT_RADII[symbol] * scale, cfg.ELEMENT_COLORS[symbol],
                label=(symbol if label and symbol not in ("H", "A") else None))


def region_lobe(origin, direction, kind: str = "X", grow: float = 1.0, scale: float = 1.0) -> Lobe:
    if kind == "E":
        return Lobe(origin, direction, LONE_LENGTH * scale, LONE_WIDTH * scale, cfg.LONE_PAIR_COLOR,
                    start=0.32 * scale, body_opacity=0.32, rim_opacity=0.9, grow=grow)
    return Lobe(origin, direction, DOMAIN_LENGTH * scale, DOMAIN_WIDTH * scale, cfg.DOMAIN_COLOR,
                start=0.22 * scale, grow=grow)


class MoleculeModel:
    """A Molecule spec, built on a stage, that can morph into its relatives.

    Every site (atom or lone pair) gets a ball, a rod, a bonding-region lobe
    and a lone-pair lobe; only the right ones are visible. Directions live in
    ``self.dirs`` and every body reads them each frame, so tweening one
    direction moves the atom, its rod, its lobe and any angle arc together.
    """

    def __init__(self, stage: Stage, mol: ml.Molecule, *, origin=ORIGIN, bond: float = BOND,
                 true_lengths: bool = False, labels: bool = True, lone_pairs: bool = True, domains: bool = False,
                 guides: bool = False, atom_scale: float = 1.0, lobe_scale: float = 1.0,
                 orient: np.ndarray | None = None) -> None:
        self.stage, self.mol = stage, mol
        self.origin = np.asarray(origin, dtype=float)
        self.bond, self.true_lengths, self.labels, self.atom_scale = bond, true_lengths, labels, atom_scale
        # A fixed rotation applied to every direction from the data, so a
        # chosen pair of bonds can face the camera (see ``bisect_down``).
        self.orient = np.eye(3) if orient is None else np.asarray(orient, dtype=float)
        self.dirs = [self.orient @ s.direction for s in mol.sites]
        self.kinds = [s.kind for s in mol.sites]
        reference = max((s.length_pm for s in mol.bonds), default=100.0)
        self.lengths = [self._length(s, reference) for s in mol.sites]
        self.center = element_ball(mol.central, self.origin, label=labels, scale=atom_scale)
        self.atoms: dict[int, Ball] = {}
        self.rods: dict[int, Rod] = {}
        self.domains: dict[int, Lobe] = {}
        self.lobes: dict[int, Lobe] = {}
        self.guides: dict[int, Segment] = {}
        bodies: list[Body] = [self.center]
        for i, site in enumerate(mol.sites):
            symbol = site.symbol or (mol.bonds[0].symbol if mol.bonds else "H")
            self.atoms[i] = element_ball(symbol, self._site_point(i), label=labels, scale=atom_scale)
            self.rods[i] = Rod(self.center, self.atoms[i], site.order if site.kind == "X" else 1)
            self.domains[i] = region_lobe(self.origin, self._dir(i), "X", scale=lobe_scale)
            self.lobes[i] = region_lobe(self.origin, self._dir(i), "E", scale=lobe_scale)
            self.guides[i] = Segment(self.origin, self._site_point(i, 1.32), cfg.MUTED, 2.6, 0.5, dashed=True)
            is_atom = site.kind == "X"
            self.atoms[i].presence = 1.0 if is_atom else 0.0
            self.rods[i].presence = 1.0 if is_atom else 0.0
            self.domains[i].presence = 1.0 if (domains and is_atom) else 0.0
            self.lobes[i].presence = 1.0 if (lone_pairs and not is_atom) else 0.0
            self.guides[i].presence = 1.0 if guides else 0.0
            bodies += [self.atoms[i], self.rods[i], self.domains[i], self.lobes[i], self.guides[i]]
        stage.add_body(*bodies)

    # --- geometry ---------------------------------------------------------------

    def _length(self, site: ml.Site, reference: float) -> float:
        if self.true_lengths and site.length_pm:
            return self.bond * site.length_pm / reference
        return self.bond

    def _dir(self, i: int) -> Callable[[], np.ndarray]:
        return lambda i=i: self.dirs[i]

    def _site_point(self, i: int, stretch: float = 1.0) -> Callable[[], np.ndarray]:
        return lambda i=i: self.origin + self.dirs[i] * self.lengths[i] * stretch

    def point(self, i: int, stretch: float = 1.0) -> np.ndarray:
        return self._site_point(i, stretch)()

    def bonded(self) -> list[int]:
        return [i for i, k in enumerate(self.kinds) if k == "X"]

    def lone(self) -> list[int]:
        return [i for i, k in enumerate(self.kinds) if k == "E"]

    # --- animations ---------------------------------------------------------------

    def aim(self, i: int, direction, **kwargs) -> Param:
        def setter(v, i=i):
            self.dirs[i] = mu.unit(v)
        return Param(self.stage, lambda i=i: self.dirs[i], setter, mu.unit(direction), mode="direction", **kwargs)

    def stretch(self, i: int, length: float, **kwargs) -> Param:
        def setter(v, i=i):
            self.lengths[i] = v
        return Param(self.stage, lambda i=i: self.lengths[i], setter, length, **kwargs)

    def fade(self, which: str, value: float, indices: Iterable[int] | None = None, **kwargs) -> list[Param]:
        """Fade one family of bodies: 'atoms', 'rods', 'domains', 'lobes', 'guides', 'center'."""
        if which == "center":
            return [self.stage.fade(self.center, value, **kwargs)]
        table = {"atoms": self.atoms, "rods": self.rods, "domains": self.domains, "lobes": self.lobes,
                 "guides": self.guides}[which]
        if indices is None:
            if which in ("atoms", "rods", "domains"):
                indices = self.bonded()
            elif which == "lobes":
                indices = self.lone()
            else:
                indices = range(len(self.dirs))
        return [self.stage.fade(table[i], value, **kwargs) for i in indices]

    def show_lone_pairs(self, value: float = 1.0, **kwargs) -> list[Param]:
        return self.fade("lobes", value, **kwargs)

    def to_lone_pair(self, i: int, *, lobe: bool = True, domain: bool = False, **kwargs) -> list[Param]:
        """Turn site i from a bonded atom into a lone pair."""
        self.kinds[i] = "E"
        anims = [self.stage.fade(self.atoms[i], 0.0, **kwargs), self.stage.fade(self.rods[i], 0.0, **kwargs)]
        if lobe:
            anims.append(self.stage.fade(self.lobes[i], 1.0, **kwargs))
        if not domain:
            anims.append(self.stage.fade(self.domains[i], 0.0, **kwargs))
        return anims

    def become(self, mol: ml.Molecule, *, lone_pairs: bool = True, **kwargs) -> list[Param]:
        """Morph into a relative with index-aligned sites (e.g. PCl5 -> SF4)."""
        anims: list[Param] = []
        reference = max((s.length_pm for s in mol.bonds), default=100.0)
        if mol.central != self.mol.central:
            anims += self.swap_center(mol.central, **kwargs)
        for i, site in enumerate(mol.sites):
            anims.append(self.aim(i, self.orient @ site.direction, **kwargs))
            if self.true_lengths:
                anims.append(self.stretch(i, self._length(site, reference), **kwargs))
            if site.kind == "E" and self.kinds[i] == "X":
                anims += self.to_lone_pair(i, lobe=lone_pairs, **kwargs)
            elif site.kind == "X" and self.kinds[i] == "X" and site.symbol != (self.mol.sites[i].symbol):
                anims += self.swap_atom(i, site.symbol, **kwargs)
        self.mol = mol
        return anims

    def swap_center(self, symbol: str, **kwargs) -> list[Param]:
        old = self.center
        new = element_ball(symbol, self.origin, label=self.labels, scale=self.atom_scale)
        new.presence = 0.0
        self.stage.add_body(new)
        for rod in self.rods.values():
            rod.a = new
        self.center = new
        return [self.stage.fade(old, 0.0, **kwargs), self.stage.fade(new, 1.0, **kwargs)]

    def swap_atom(self, i: int, symbol: str, **kwargs) -> list[Param]:
        old = self.atoms[i]
        new = element_ball(symbol, self._site_point(i), label=self.labels, scale=self.atom_scale)
        new.presence = 0.0
        self.stage.add_body(new)
        self.rods[i].b = new
        self.atoms[i] = new
        return [self.stage.fade(old, 0.0, **kwargs), self.stage.fade(new, 1.0, **kwargs)]

    def arc(self, i: int, j: int, *, radius: float = 0.95, label: Mobject | None = None, live: bool = False,
            label_gap: float = 0.45, label_offset=ORIGIN, color: str = cfg.ANGLE_COLOR,
            size: int | None = None) -> AngleArc:
        """An angle arc between sites i and j. ``live`` shows the drawn angle, updated as it changes."""
        item = AngleArc(self.origin, self._dir(i), self._dir(j), radius, color, label=label,
                        live=(lambda v: degrees_label(v, size)) if live else None,
                        label_gap=label_gap, label_offset=label_offset)
        item.presence = 0.0
        self.stage.add_overlay(item)
        return item

    def angle(self, i: int, j: int) -> float:
        return mu.angle_deg(self.dirs[i], self.dirs[j])


class RegionModel:
    """A bare central atom with n electron-region lobes (chapters 03, 09, 11).

    ``dirs`` holds one direction per lobe; ``play_path`` replays a computed
    relaxation path from ``physics_models``.
    """

    def __init__(self, stage: Stage, directions: np.ndarray, *, origin=ORIGIN, kinds: Sequence[str] | None = None,
                 core_color: str = cfg.WHITE, scale: float = 1.0) -> None:
        self.stage = stage
        self.origin = np.asarray(origin, dtype=float)
        self.scale = scale
        self.dirs = [mu.unit(d) for d in directions]
        self.core = Ball(self.origin, 0.36 * scale, core_color, label="A")
        self.glow = Halo(self.core, cfg.CYAN, reach=2.6, peak=0.12)
        self.lobes: list[Lobe] = []
        stage.add_body(self.glow, self.core)
        for i, kind in enumerate(kinds or ["X"] * len(self.dirs)):
            self._new_lobe(i, kind)

    def _new_lobe(self, i: int, kind: str = "X", grow: float = 1.0) -> Lobe:
        lobe = region_lobe(self.origin, lambda i=i: self.dirs[i], kind, grow=grow, scale=self.scale)
        self.lobes.append(lobe)
        self.stage.add_body(lobe)
        return lobe

    def add_region(self, direction, kind: str = "X") -> Lobe:
        self.dirs.append(mu.unit(direction))
        lobe = self._new_lobe(len(self.dirs) - 1, kind, grow=0.0)
        return lobe

    def grow(self, lobe: Lobe, value: float = 1.0, **kwargs) -> Param:
        def setter(v, l=lobe):
            l.grow = v
        return Param(self.stage, lambda l=lobe: l.grow, setter, value, **kwargs)

    def aim(self, i: int, direction, **kwargs) -> Param:
        def setter(v, i=i):
            self.dirs[i] = mu.unit(v)
        return Param(self.stage, lambda i=i: self.dirs[i], setter, mu.unit(direction), mode="direction", **kwargs)

    def play_path(self, path: np.ndarray, **kwargs) -> Param:
        """Move every region along a relaxation path, frame by frame."""
        def setter(frame):
            for i, d in enumerate(frame):
                self.dirs[i] = d
        return Param(self.stage, lambda: np.array(self.dirs), setter, path, mode="path", **kwargs)

    def rigid_turn(self, rotation: np.ndarray, **kwargs) -> Param:
        """Turn all regions together by a fixed rotation (the arrangement keeps its shape)."""
        start: dict[str, list] = {}
        axis_angle = _axis_angle(rotation)

        def get():
            start["dirs"] = [d.copy() for d in self.dirs]
            return 0.0

        def put(value):
            turn = mu.rotation_about(axis_angle[0], value * axis_angle[1])
            self.dirs[:] = [turn @ d for d in start["dirs"]]

        return Param(self.stage, get, put, 1.0, **kwargs)

    def arc(self, i: int, j: int, *, radius: float = 1.0, label: Mobject | None = None,
            label_gap: float = 0.45) -> AngleArc:
        item = AngleArc(self.origin, lambda i=i: self.dirs[i], lambda j=j: self.dirs[j], radius * self.scale,
                        label=label, label_gap=label_gap)
        item.presence = 0.0
        self.stage.add_overlay(item)
        return item

    def tip(self, i: int, stretch: float = 1.0) -> Callable[[], np.ndarray]:
        return lambda i=i: self.origin + self.dirs[i] * (DOMAIN_LENGTH * self.scale + 0.12) * stretch


def faces(stage: Stage, corners: Sequence[Callable[[], np.ndarray]], triples: Iterable[tuple[int, ...]],
          color: str = cfg.CYAN, opacity: float = 0.08, edge: float = 0.45) -> list[Face]:
    """Translucent polygons through live 3D points, added hidden (fade them in)."""
    made = []
    for triple in triples:
        face = Face([corners[i] for i in triple], color, opacity, edge)
        face.presence = 0.0
        made.append(face)
    stage.add_body(*made)
    return made


def mini_model(key: str, at, *, zoom: float = 0.62, lone_pairs: float = 0.0, yaw: float = 0.5, pitch: float = 0.3,
               spin: float = 0.25, labels: bool = True) -> tuple[Stage, "MoleculeModel"]:
    """A small turning model for side-by-side line-ups, added hidden."""
    stage = Stage(at, zoom=zoom, yaw=yaw, pitch=pitch, spin=spin)
    model = MoleculeModel(stage, ml.molecule(key), labels=labels)
    for i in model.lone():
        model.lobes[i].presence = lone_pairs
    stage.presence = 0.0
    stage.refresh()
    return stage, model


def bisect_down(a, b) -> np.ndarray:
    """Rotation that puts directions a and b in the screen plane, symmetric
    about straight down (a to the right): how a bent molecule is drawn."""
    a, b = mu.unit(a), mu.unit(b)
    ex = mu.unit(a - b)
    ey = -mu.unit(a + b)
    ez = np.cross(ex, ey)
    return np.array([ex, ey, ez])


def _axis_angle(rotation: np.ndarray) -> tuple[np.ndarray, float]:
    angle = float(np.arccos(np.clip((np.trace(rotation) - 1) / 2, -1, 1)))
    if angle < 1e-9:
        return np.array([0.0, 1.0, 0.0]), 0.0
    axis = np.array([rotation[2, 1] - rotation[1, 2], rotation[0, 2] - rotation[2, 0], rotation[1, 0] - rotation[0, 1]])
    return mu.unit(axis), angle


# ----------------------------------------------------------------------------
# Orbitals on a stage
# ----------------------------------------------------------------------------

ORB_UNITS = 0.6         # screen units per unit of the drawn polar plot (an sp3 lobe reaches 4)


class OrbitalLobe(Blob):
    """One lobe of a hybrid or atomic orbital whose mixing angle can change.

    The drawn shape is the polar plot of the angular density (see
    ``utils.orbital_models``); it is lit toward its own tip.
    """

    def __init__(self, origin, axis, alpha: float, sign: int, color: str, *, units: float = ORB_UNITS,
                 opacity: float = 0.8) -> None:
        self.axis_dir, self.alpha, self.sign = axis, float(alpha), sign
        self._cache_key, self._cache = None, None
        super().__init__(self._make, origin, color, units=units, opacity=opacity, focus=self._tip)

    def _tip(self) -> np.ndarray:
        axis = mu.unit(_value(self.axis_dir)) * self.sign
        return _vec3(self.origin) + axis * om.polar_reach(self.alpha, self.sign) * self.units * 0.62

    def _make(self):
        axis = mu.unit(_value(self.axis_dir))
        key = (round(self.alpha, 5), tuple(np.round(axis, 5)))
        if key != self._cache_key:
            self._cache = om.polar_points(self.alpha, axis, self.sign)
            self._cache_key = key
        return self._cache


def _vec3(thing) -> np.ndarray:
    return np.asarray(_value(thing), dtype=float)


def _value(thing):
    return thing() if callable(thing) else thing


class Orbital:
    """A whole orbital: its positive lobe and (when it exists) its negative one."""

    def __init__(self, stage: Stage, origin, axis, alpha: float, *, plus: str = cfg.PHASE_PLUS,
                 minus: str = cfg.PHASE_MINUS, units: float = ORB_UNITS, opacity: float = 0.86) -> None:
        self.stage = stage
        self.axis = axis
        self.plus = OrbitalLobe(origin, axis, alpha, 1, plus, units=units, opacity=opacity)
        self.minus = OrbitalLobe(origin, axis, alpha, -1, minus, units=units, opacity=opacity)
        stage.add_body(self.plus, self.minus)

    @property
    def lobes(self) -> list[OrbitalLobe]:
        return [self.plus, self.minus]

    def mix_to(self, alpha: float, **kwargs) -> Param:
        def setter(v):
            self.plus.alpha = self.minus.alpha = v
        return Param(self.stage, lambda: self.plus.alpha, setter, alpha, **kwargs)

    def fade(self, value: float, **kwargs) -> list[Param]:
        return [self.stage.fade(lobe, value, **kwargs) for lobe in self.lobes]

    def set_presence(self, value: float) -> None:
        for lobe in self.lobes:
            lobe.presence = value


def p_orbital(stage: Stage, origin, axis, color: str = cfg.UNHYBRID, *, units: float = ORB_UNITS,
              opacity: float = 0.82, phased: bool = False) -> Orbital:
    """A p orbital: two equal lobes. Unhybridised p orbitals are one colour."""
    return Orbital(stage, origin, axis, np.pi / 2, plus=cfg.PHASE_PLUS if phased else color,
                   minus=cfg.PHASE_MINUS if phased else mu.shade(color, 0.85), units=units, opacity=opacity)


def hydrogen_orbital(stage: Stage, origin, *, units: float = ORB_UNITS, opacity: float = 0.75) -> Blob:
    """A hydrogen 1s orbital: a sphere of the e^{-r} contour."""
    radius = om.hydrogen_radius()
    sphere = np.array([[np.sin(t) * np.cos(p), np.cos(t), np.sin(t) * np.sin(p)]
                       for t in np.linspace(0, np.pi, 9) for p in np.linspace(0, 2 * np.pi, 14, endpoint=False)])
    blob = Blob(lambda: sphere * radius, origin, cfg.H_ORBITAL, units=units, opacity=opacity)
    stage.add_body(blob)
    return blob


# ----------------------------------------------------------------------------
# Closing card
# ----------------------------------------------------------------------------


def subscribe_card() -> VGroup:
    """The channel's closing card, in the house style."""
    thank_you = txt("THANK YOU FOR WATCHING", 40, cfg.CYAN)
    subscribe = Text("SUBSCRIBE", font_size=96, color=cfg.GOLD, weight=BOLD)
    subscribe.set_stroke("#351F05", width=3, opacity=0.75, background=True)
    rule = Line(LEFT * 3.4, RIGHT * 3.4, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(txt("Stay curious.", 44, cfg.WHITE),
                     txt("Next: molecular orbital theory", 36, cfg.CYAN)).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "ml", "om", "gd", "np"]
