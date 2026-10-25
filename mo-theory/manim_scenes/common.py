"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing synthesis reads as a conclusion rather than a new picture:

* a **wave function** is blue where it is positive and rose where it is
  negative — phase, never charge — whether it is a curve, a 2D map
  (``PhaseMap``) or a 3D orbital (``MOCloud``); electron **density**
  (|psi|^2) is cyan;
* an **orbital surface** is a computed |psi| = level surface on a turning 3D
  ``Stage`` (``stage3d.py``), split into lobes by sign;
* an **energy diagram** (``MODiagram``) has atomic levels on the sides,
  molecular levels in the middle, **cyan** bonding levels and **orange**
  antibonding levels, and its arrows are placed by ``utils.mo_models``
  (Aufbau, Pauli, Hund) — never by hand;
* an **electron** is a spin arrow: cyan when paired, **gold** and glowing when
  unpaired — the film's quarry;
* **bond order** is the balance of bonding against antibonding electrons, and
  a confirmed result is green;
* a **Lewis structure** is flat type: letters, white bond lines, white dots.

Scene files compose these pieces and choreograph them against the beats in
``narration.py``; nothing in a scene file should invent a second way to draw
one of these ideas, or type a number that the models can supply.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from manim import *

import config as cfg
from manim_scenes.stage3d import (Ball, Blob, Body, Face, Fog, Halo, Overlay, Param, Rod, Segment, Stage, Tag,
                                  Vector)
from narration import SCRIPT
from utils import math_utils as mu
from utils import mo_data as md
from utils import mo_models as mo
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
    """Hold the composition; live stages and pours keep moving."""
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


def tween(mob: Mobject, getter: Callable, setter: Callable, target, mode: str = "scalar", **kwargs) -> Param:
    """Animate any live value (a map's coefficient, a pour's clock) without copying ``mob``."""
    return Param(mob, getter, setter, target, mode=mode, **kwargs)


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


def result_label(name: str, color: str = cfg.RESULT, size: int | None = None) -> VGroup:
    """A revealed result: coloured type with a soft glow behind it."""
    label = txt(name, size or cfg.FONT["section"], color)
    glow = label.copy().set_stroke(color, width=14, opacity=0.16).set_fill(opacity=0)
    decorative(glow)
    group = VGroup(glow, label)
    group.label = label
    return group


def formula(key: str, size: int | None = None, color: str = cfg.WHITE) -> MathTex:
    """A species' formula, e.g. formula('O2-') -> O2^-; from the model's own TeX."""
    return eq(mo.species(key).tex, size or cfg.FONT["section"], color)


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


def glow_dot(point, color: str = cfg.CYAN, radius: float = 0.09, reach: float = 3.2) -> VGroup:
    core = Circle(radius=radius, stroke_width=0, fill_color=mu.mix(color, cfg.WHITE, 0.35), fill_opacity=1)
    group = VGroup(halo(radius * reach, color, layers=5, peak_opacity=0.22), core)
    return group.move_to(point)


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


def dashed_path(a, b, color: str = cfg.MUTED, width: float = 2.4, opacity: float = 0.55, dash: float = 0.13) -> VMobject:
    """A dashed line as one VMobject of many sub-paths (cheap to move every frame)."""
    line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    set_dashes(line, a, b, dash)
    return line


def set_dashes(line: VMobject, a, b, dash: float = 0.13) -> VMobject:
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    length = float(np.linalg.norm(b - a))
    count = max(int(length / (2 * dash)), 1)
    line.clear_points()
    for k in range(count):
        t0, t1 = k / count, (k + 0.55) / count
        line.start_new_path(a + (b - a) * t0)
        line.add_line_to(a + (b - a) * t1)
    return line


# ----------------------------------------------------------------------------
# Electrons: spin arrows
# ----------------------------------------------------------------------------

ARROW_HEIGHT = 0.5


def spin_arrow(spin: int = 1, color: str = cfg.ELECTRON, height: float = ARROW_HEIGHT, glow: bool = True) -> VGroup:
    """An electron on an energy level: an arrow pointing up (spin up) or down."""
    direction = UP if spin > 0 else DOWN
    tail, head = -direction * height / 2, direction * height / 2
    tip = Triangle(stroke_width=0, fill_color=color, fill_opacity=1).scale(0.115)
    if spin < 0:
        tip.rotate(PI)
    tip.move_to(head - direction * 0.075)
    shaft = Line(tail, head - direction * 0.12, stroke_color=color, stroke_width=6.5)
    parts = [shaft, tip]
    if glow:
        under = Line(tail, head, stroke_color=color, stroke_width=20, stroke_opacity=0.16)
        parts.insert(0, under)
    group = VGroup(*parts)
    group.spin, group.color_key = spin, color
    return group


def recolor_arrow(arrow: VGroup, color: str) -> VGroup:
    """Recolour a spin arrow in place (the glow keeps its own low opacity)."""
    for part in arrow:
        if isinstance(part, Triangle):
            part.set_fill(color)
        else:
            part.set_stroke(color)
    return arrow


def compare_bars(rows: Sequence[tuple[str, float, str, str]], *, max_value: float, length: float = 4.2,
                 title: str | None = None, label_width: float = 1.6) -> VGroup:
    """Horizontal bars for measured values: (TeX label, value, value text, colour)."""
    group = VGroup()
    bars = VGroup()
    for i, (label, value, shown, color) in enumerate(rows):
        name = eq(label, cfg.FONT["label"], cfg.WHITE)
        fit_width(name, label_width)
        bar = Rectangle(width=max(length * value / max_value, 0.05), height=0.42, stroke_width=0, fill_color=color,
                        fill_opacity=0.9)
        reading = txt(shown, cfg.FONT["small"], color)
        row = VGroup(name, bar, reading)
        name.move_to([0, -0.75 * i, 0], aligned_edge=RIGHT)
        bar.move_to([0.25, -0.75 * i, 0], aligned_edge=LEFT)
        reading.next_to(bar, RIGHT, buff=0.2)
        bars.add(row)
    group.add(bars)
    if title:
        head = txt(title, cfg.FONT["small"], cfg.MUTED).next_to(bars, UP, buff=0.3)
        head.align_to(bars, LEFT)
        group.add(head)
    group.bars = bars
    return group


# ----------------------------------------------------------------------------
# The molecular orbital energy diagram
# ----------------------------------------------------------------------------


class MODiagram(VGroup):
    """An MO energy diagram drawn from a ``mo_models.Diagram``.

    Atomic levels sit at ``x = +-ao_x``, molecular levels in the middle; a
    degenerate set is drawn as side-by-side lines. Every part is reachable by
    key, so scenes can build the diagram piece by piece, and every electron
    slot (``slot``) is computed from the layout.
    """

    def __init__(self, dia: mo.Diagram, *, center=ORIGIN, height: float = 6.2, ao_x: float = 4.7,
                 mo_width: float = 1.05, ao_width: float = 0.78, gap: float = 0.3, window: tuple[float, float] | None = None,
                 atoms: tuple[str, str] = ("A", "B"), molecule: str | None = None, label_size: int | None = None,
                 axis: bool = True, aos: bool = True) -> None:
        super().__init__()
        self.dia = dia
        self.mixing = 1.0 if dia.kind == "mixed" else 0.0
        self.show_aos = aos
        # Never store a size as self.height / self.width: those are Mobject
        # properties that rescale the group.
        self.anchor = np.asarray(center, dtype=float)
        self.span, self.ao_x, self.mo_width, self.ao_width, self.gap = height, ao_x, mo_width, ao_width, gap
        self.window = window or (mo.ONE_S_WINDOW if dia.kind == "1s" else mo.VALENCE_WINDOW)
        self.label_size = label_size or cfg.FONT["body"]
        self.levels: dict[str, VGroup] = {}
        self.labels: dict[str, MathTex] = {}
        self.ao_left: dict[str, VGroup] = {}
        self.ao_right: dict[str, VGroup] = {}
        self.ao_labels: dict[str, VGroup] = {}
        self.links: dict[str, VGroup] = {}
        for level in dia.mo:
            color = cfg.BONDING if level.bonding else cfg.ANTIBONDING
            self.levels[level.key] = self._lines(0.0, self.y(level.energy), level.degeneracy, mo_width, color, 7)
            label = eq(level.tex, self.label_size, color)
            self.labels[level.key] = label
            self._place_label(level.key)
        for level in dia.ao:
            y = self.y(level.energy)
            self.ao_left[level.key] = self._lines(-ao_x, y, level.degeneracy, ao_width, cfg.AO_LEVEL, 6)
            self.ao_right[level.key] = self._lines(ao_x, y, level.degeneracy, ao_width, cfg.AO_LEVEL, 6)
            left_label = eq(level.tex, self.label_size, cfg.MUTED)
            right_label = eq(level.tex, self.label_size, cfg.MUTED)
            self.ao_labels[level.key] = VGroup(left_label, right_label)
            self._place_ao_labels(level.key)
        for level in dia.mo:
            self.links[level.key] = VGroup(dashed_path(ORIGIN, RIGHT), dashed_path(ORIGIN, RIGHT))
            self._place_links(level.key)
        self.atom_names = VGroup(txt(atoms[0], cfg.FONT["body"], cfg.WHITE), txt(atoms[1], cfg.FONT["body"], cfg.WHITE))
        top = self.anchor[1] + height / 2 + 0.42
        self.atom_names[0].move_to([self.anchor[0] - ao_x, top, 0])
        self.atom_names[1].move_to([self.anchor[0] + ao_x, top, 0])
        self.molecule = formula(molecule, cfg.FONT["body"]) if molecule else VGroup()
        if molecule:
            self.molecule.move_to([self.anchor[0], top, 0])
        self.axis = VGroup()
        if axis:
            bottom = self.anchor + DOWN * height / 2 + LEFT * (ao_x + 1.45)
            arrow = Arrow(bottom, bottom + UP * height, buff=0, color=cfg.MUTED, stroke_width=5, tip_length=0.26)
            label = eq("E", cfg.FONT["label"], cfg.MUTED).next_to(arrow.get_end(), RIGHT, buff=0.12).shift(DOWN * 0.18)
            self.axis = VGroup(arrow, label)
        if aos:
            self.add(self.axis, *self.links.values(), *self.ao_left.values(), *self.ao_right.values(),
                     *self.ao_labels.values(), *self.levels.values(), *self.labels.values(), self.atom_names, self.molecule)
        else:   # molecular levels only (chapter 13 compares orderings)
            self.add(self.axis, *self.levels.values(), *self.labels.values(), self.molecule)

    # --- layout -----------------------------------------------------------------------

    def y(self, energy: float) -> float:
        low, high = self.window
        return float(self.anchor[1] - self.span / 2 + (energy - low) / (high - low) * self.span)

    def _xs(self, x0: float, count: int, width: float, gap: float | None = None) -> list[float]:
        gap = self.gap if gap is None else gap
        total = count * width + (count - 1) * gap
        return [x0 - total / 2 + width / 2 + i * (width + gap) for i in range(count)]

    def _lines(self, x0: float, y: float, count: int, width: float, color: str, stroke: float) -> VGroup:
        group = VGroup()
        for x in self._xs(x0, count, width, 0.22 if count == 3 else None):
            centre = self.anchor + np.array([x, y - self.anchor[1], 0])
            group.add(Line(centre + LEFT * width / 2, centre + RIGHT * width / 2, stroke_color=color,
                           stroke_width=stroke))
        return group

    def _place_label(self, key: str) -> None:
        """Sigma labels to the right of their level, pi labels to the left, so
        neighbouring sigma and pi levels never stack their labels."""
        line = self.levels[key]
        self.labels[key].next_to(line, LEFT if key.startswith("p") else RIGHT, buff=0.3)
        self.labels[key].set_y(line.get_y())

    def _place_ao_labels(self, key: str) -> None:
        left, right = self.ao_labels[key]
        left.next_to(self.ao_left[key], DOWN, buff=0.34)
        right.next_to(self.ao_right[key], DOWN, buff=0.34)

    def _place_links(self, key: str) -> None:
        level = self.dia.level(key)
        lines = self.levels[key]
        left_ao, right_ao = self.ao_left[level.parent], self.ao_right[level.parent]
        set_dashes(self.links[key][0], left_ao.get_right(), lines.get_left())
        set_dashes(self.links[key][1], lines.get_right(), right_ao.get_left())

    def mix_to(self, mixing: float, **kwargs) -> Param:
        """Tween the s-p mixing strength of a valence diagram (0 = O2/F2 order, 1 = B2-N2 order)."""
        def put(v):
            self.mixing = v
            self.set_energies(mo.diagram("unmixed", mixing=v))

        return Param(self, lambda: self.mixing, put, mixing, **kwargs)

    def set_energies(self, dia: mo.Diagram) -> None:
        """Move every molecular level to a new diagram's energies (same keys)."""
        self.dia = dia
        for level in dia.mo:
            self.levels[level.key].set_y(self.y(level.energy))
            self._place_label(level.key)
            self._place_links(level.key)

    # --- electrons ------------------------------------------------------------------------

    def slot(self, key: str, orbital: int = 0, spin: int = 1, side: str = "mo") -> np.ndarray:
        """Where an electron arrow sits: on a molecular level ('mo') or on the
        left/right atom's level ('L' / 'R')."""
        line = {"mo": self.levels, "L": self.ao_left, "R": self.ao_right}[side][key][orbital]
        return line.get_center() + LEFT * 0.17 * spin

    def electron(self, key: str, orbital: int = 0, spin: int = 1, side: str = "mo", color: str | None = None) -> VGroup:
        if color is None:
            bonding = side != "mo" or self.dia.level(key).bonding
            color = cfg.ELECTRON if bonding else cfg.ANTIBONDING
        return spin_arrow(spin, color).move_to(self.slot(key, orbital, spin, side))

    def electrons_for(self, filling: mo.Filling, unpaired_gold: bool = True) -> list[VGroup]:
        """Arrows for a whole filling, in placement (Aufbau) order."""
        lonely = set(filling.unpaired_placements()) if unpaired_gold else set()
        arrows = []
        for p in filling.electrons:
            color = cfg.UNPAIRED if p in lonely else None
            arrows.append(self.electron(p.level, p.orbital, p.spin, color=color))
        return arrows

    def atom_electrons(self, count: int, side: str) -> list[VGroup]:
        """Arrows on one isolated atom's levels (valence electrons before bonding)."""
        return [spin_arrow(spin, cfg.ELECTRON).move_to(self.slot(key, orbital, spin, side))
                for key, orbital, spin in mo.atomic_placements(self.dia, count)]

    # --- pieces ---------------------------------------------------------------------------

    def level_group(self, key: str, links: bool = True) -> VGroup:
        parts = [self.levels[key], self.labels[key]]
        if links:
            parts.append(self.links[key])
        return VGroup(*parts)

    def ao_group(self, key: str) -> VGroup:
        return VGroup(self.ao_left[key], self.ao_right[key], self.ao_labels[key])

    def frame(self) -> VGroup:
        return VGroup(self.axis, self.atom_names, self.molecule)

    def highlight(self, key: str, color: str = cfg.GOLD, buff: float = 0.2) -> VGroup:
        return glow_frame(VGroup(self.levels[key], self.labels[key]), color, buff=buff)


def mini_split(center, *, drop: float, rise: float, bonding_tex: str, antibonding_tex: str, count: int = 1,
               half_width: float = 2.3, line: float = 0.75, size: int | None = None) -> VGroup:
    """A small two-level splitting picture: one AO level each side, a bonding
    level ``drop`` below and an antibonding level ``rise`` above (``count``
    degenerate copies of each)."""
    c = np.asarray(center, dtype=float)
    group = VGroup()
    ao = VGroup(*[Line(c + np.array([side * half_width - line / 2, 0, 0]), c + np.array([side * half_width + line / 2, 0, 0]),
                       stroke_color=cfg.AO_LEVEL, stroke_width=6) for side in (-1, 1)])

    def level(dy, color):
        total = count * line + (count - 1) * 0.22
        xs = [-total / 2 + line / 2 + i * (line + 0.22) for i in range(count)]
        return VGroup(*[Line(c + np.array([x - line / 2, dy, 0]), c + np.array([x + line / 2, dy, 0]), stroke_color=color,
                             stroke_width=7) for x in xs])

    bond, anti = level(-drop, cfg.BONDING), level(rise, cfg.ANTIBONDING)
    links = VGroup()
    for target in (bond, anti):
        links.add(dashed_path(ao[0].get_right(), target.get_left()), dashed_path(target.get_right(), ao[1].get_left()))
    labels = VGroup(eq(bonding_tex, size or cfg.FONT["label"], cfg.BONDING).next_to(bond, DOWN, buff=0.18),
                    eq(antibonding_tex, size or cfg.FONT["label"], cfg.ANTIBONDING).next_to(anti, UP, buff=0.18))
    group.add(links, ao, bond, anti, labels)
    group.ao, group.bond, group.anti, group.labels, group.links = ao, bond, anti, labels, links
    return group


def fly_electrons(diagram: MODiagram, sources: Sequence[Mobject], filling: mo.Filling, *,
                  arc: float = -0.6, unpaired_gold: bool = True) -> tuple[list[Animation], list[VGroup]]:
    """Animations carrying each source mobject (a Lewis dot, an atom's arrow)
    to its computed slot, in Aufbau order; returns (animations, arrows)."""
    arrows = diagram.electrons_for(filling, unpaired_gold)
    anims = [ReplacementTransform(src, arrow, path_arc=arc) for src, arrow in zip(sources, arrows)]
    return anims, arrows


# ----------------------------------------------------------------------------
# Bond order
# ----------------------------------------------------------------------------


def bond_order_formula(size: int | None = None) -> MathTex:
    """Bond order = (N_b - N_a) / 2, with N_b cyan and N_a orange."""
    result = eq([r"\text{Bond order}", "=", r"{N_b", "-", r"N_a", r"\over", "2}"], size or cfg.FONT["section"])
    result[2].set_color(cfg.BONDING)
    result[4].set_color(cfg.ANTIBONDING)
    return result


def bond_order_numbers(nb: int, na: int, size: int | None = None, show_result: bool = True) -> MathTex:
    """(nb - na) / 2 = result, the result green; numbers from a filling."""
    value = (nb - na) / 2
    result_tex = md.display_number(value)
    parts = [rf"{{{nb}", "-", rf"{na}", r"\over", "2}"]
    if show_result:
        parts += ["=", result_tex]
    result = eq(parts, size or cfg.FONT["section"])
    result[0].set_color(cfg.BONDING)
    result[2].set_color(cfg.ANTIBONDING)
    if show_result:
        result[-1].set_color(cfg.RESULT)
    return result


class BondOrderMeter(VGroup):
    """A horizontal track from 0 to ``top`` with a glowing marker for one value."""

    def __init__(self, *, width: float = 6.0, top: float = 3.0, center=ORIGIN, value: float = 0.0,
                 label: bool = True) -> None:
        super().__init__()
        self.track_width, self.top = width, top
        self.center_point = np.asarray(center, dtype=float)
        left = self.center_point + LEFT * width / 2
        self.track = Line(left, left + RIGHT * width, stroke_color=cfg.MUTED, stroke_width=6, stroke_opacity=0.7)
        self.ticks = VGroup()
        self.numbers = VGroup()
        steps = int(round(top * 2))
        for i in range(steps + 1):
            v = i / 2
            x = self.x(v)
            major = i % 2 == 0
            self.ticks.add(Line([x, self.center_point[1] - (0.16 if major else 0.09), 0],
                                [x, self.center_point[1] + (0.16 if major else 0.09), 0],
                                stroke_color=cfg.MUTED, stroke_width=4 if major else 3))
            if major:
                self.numbers.add(txt(str(int(v)), cfg.FONT["small"], cfg.MUTED)
                                 .move_to([x, self.center_point[1] - 0.5, 0]))
        self.value = value
        self.marker = glow_dot(self._spot(), cfg.RESULT, radius=0.13, reach=3.0)
        self.readout = VGroup()
        self.title = txt("Bond order", cfg.FONT["small"], cfg.MUTED).next_to(self.track, LEFT, buff=0.4) if label else VGroup()
        self.add(self.track, self.ticks, self.numbers, self.title, self.marker, self.readout)
        self._update_readout()

    def x(self, v: float) -> float:
        return float(self.center_point[0] - self.track_width / 2 + self.track_width * v / self.top)

    def _spot(self) -> np.ndarray:
        return np.array([self.x(self.value), self.center_point[1], 0.0])

    def _update_readout(self) -> None:
        new = txt(md.display_number(self.value), cfg.FONT["label"], cfg.RESULT)
        new.move_to(self._spot() + UP * 0.55)
        self.readout.submobjects = [new]

    def set_value(self, v: float) -> None:
        self.value = float(v)
        self.marker.move_to(self._spot())
        self._update_readout()

    def to(self, v: float, **kwargs) -> Param:
        return Param(self, lambda: self.value, self.set_value, v, **kwargs)


# ----------------------------------------------------------------------------
# Lewis structure of a diatomic molecule (flat, on purpose)
# ----------------------------------------------------------------------------


class LewisDiatomic(VGroup):
    """X=X with lone pairs: big letters, white bond lines, white electron dots.

    ``electron_dots()`` returns every valence electron as a dot (the bond
    lines become pairs of dots), in a fixed order, so a scene can send each
    one to its computed slot in an MO diagram.
    """

    def __init__(self, symbol: str, order: int, lone_pairs: int, *, at=ORIGIN, size: int = 190,
                 spacing: float = 3.0, dot_color: str = cfg.WHITE) -> None:
        super().__init__()
        at = np.asarray(at, dtype=float)
        self.at, self.spacing = at, spacing
        self.letters = VGroup(txt(symbol, size, cfg.WHITE).move_to(at + LEFT * spacing / 2),
                              txt(symbol, size, cfg.WHITE).move_to(at + RIGHT * spacing / 2))
        half = self.letters[0].width / 2
        inner, outer = at + LEFT * (spacing / 2 - half - 0.2), at + RIGHT * (spacing / 2 - half - 0.2)
        offsets = {1: [0.0], 2: [-0.15, 0.15], 3: [-0.24, 0.0, 0.24]}[order]
        self.bonds = VGroup(*[Line(inner + UP * o, outer + UP * o, stroke_color=cfg.WHITE, stroke_width=9)
                              for o in offsets])
        self.lone = VGroup()
        angles = {1: [180], 2: [135, 225], 3: [90, 180, 270]}[lone_pairs] if lone_pairs else []
        for side, letter in ((-1, self.letters[0]), (1, self.letters[1])):
            for angle in angles:
                a = np.radians(angle if side < 0 else 180 - angle)
                d = np.array([np.cos(a), np.sin(a), 0.0])
                spot = letter.get_center() + d * (max(letter.width, letter.height) / 2 + 0.36)
                perp = np.array([-d[1], d[0], 0.0])
                pair = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=dot_color, fill_opacity=1)
                                .move_to(spot + perp * s * 0.14) for s in (-1, 1)])
                self.lone.add(pair)
        self.dot_color = dot_color
        self.add(self.bonds, self.letters, self.lone)

    def bond_dots(self) -> VGroup:
        """Two dots per bond line, sitting where the line was."""
        dots = VGroup()
        for line in self.bonds:
            for t in (0.38, 0.62):
                dots.add(Circle(radius=0.1, stroke_width=0, fill_color=self.dot_color, fill_opacity=1)
                         .move_to(line.point_from_proportion(t)))
        return dots

    def electron_dots(self, bond_dots: VGroup) -> list[Mobject]:
        """Every valence electron: bond electrons first, then lone pairs left to right."""
        singles = [d for d in bond_dots]
        for pair in self.lone:
            singles.extend(pair)
        return singles


# ----------------------------------------------------------------------------
# The magnet and the pour
# ----------------------------------------------------------------------------


class Electromagnet(VGroup):
    """A U-shaped magnet opening upward; its two pole tips face across a gap.

    ``gap_center`` is where the field is strongest. The geometry matches
    ``physics_models.MagnetGeometry`` so the droplets meet the poles where the
    picture says they should.
    """

    def __init__(self, center=ORIGIN, scale: float = 1.0) -> None:
        super().__init__()
        geo = pm.MagnetGeometry()
        c = np.asarray(center, dtype=float)
        self.geo, self.scale_factor = geo, scale
        self.gap_center = c + UP * geo.gap_y * scale
        steel_dark, steel_light = "#30414F", "#9DB2C2"

        def shaded_block(width, height, at, tone_a, tone_b):
            depth = np.array([0.18, 0.12, 0.0]) * scale
            left, right = at + LEFT * width / 2, at + RIGHT * width / 2
            top, bottom = UP * height / 2, DOWN * height / 2
            side = Polygon(right + bottom, right + top, right + top + depth, right + bottom + depth,
                           stroke_width=0, fill_color=mu.mix(tone_a, tone_b, 0.25), fill_opacity=1)
            cap = Polygon(left + top, right + top, right + top + depth, left + top + depth,
                          stroke_width=0, fill_color=mu.mix(tone_a, tone_b, 0.72), fill_opacity=1)
            block = VGroup(side, cap)
            for k, f in enumerate(np.linspace(1.0, 0.15, 16)):
                tone = mu.mix(tone_a, tone_b, k / 15)
                block.add(RoundedRectangle(width=width * (0.6 + 0.4 * f), height=height * (0.75 + 0.25 * f),
                                           corner_radius=0.12, stroke_width=0, fill_color=tone, fill_opacity=1)
                          .move_to(at + UL * 0.04 * (1 - f)))
            return block

        gy = self.gap_center[1]
        leg_w, leg_h = 1.1 * scale, 2.6 * scale
        legs = VGroup()
        for side in (-1, 1):
            legs.add(shaded_block(leg_w, leg_h, np.array([c[0] + side * 1.35 * scale, gy - 1.05 * scale, 0]),
                                  steel_dark, steel_light))
        base = shaded_block(3.8 * scale, 0.9 * scale, np.array([c[0], gy - 2.3 * scale, 0]), steel_dark, steel_light)
        coils = VGroup()
        for side in (-1, 1):
            for k in range(7):
                y = gy - 0.4 * scale - k * 0.24 * scale
                coils.add(RoundedRectangle(width=1.35 * scale, height=0.17 * scale, corner_radius=0.07,
                                           stroke_width=0, fill_color=mu.mix("#B86B2B", "#F2B36B", (k % 2) * 0.6),
                                           fill_opacity=1).move_to([c[0] + side * 1.35 * scale, y - 0.35 * scale, 0]))
        poles = VGroup()
        for side, color, letter in ((-1, cfg.RED, "N"), (1, cfg.BLUE, "S")):
            tip = Polygon([c[0] + side * 0.72 * scale, gy + 0.45 * scale, 0],
                          [c[0] + side * 1.9 * scale, gy + 0.62 * scale, 0],
                          [c[0] + side * 1.9 * scale, gy - 0.62 * scale, 0],
                          [c[0] + side * 0.72 * scale, gy - 0.45 * scale, 0],
                          stroke_width=0, fill_color=mu.mix(color, steel_dark, 0.35), fill_opacity=1)
            face = Line([c[0] + side * 0.72 * scale, gy + 0.45 * scale, 0], [c[0] + side * 0.72 * scale, gy - 0.45 * scale, 0],
                        stroke_color=color, stroke_width=7)
            label = txt(letter, cfg.FONT["label"], cfg.WHITE).move_to([c[0] + side * 1.38 * scale, gy, 0])
            decorative(label)
            poles.add(VGroup(tip, face, label))
        self.field = VGroup()
        for k, dy in enumerate(np.linspace(-0.32, 0.32, 5)):
            self.field.add(dashed_path([c[0] - 0.62 * scale, gy + dy * scale, 0], [c[0] + 0.62 * scale, gy + dy * scale, 0],
                                       cfg.CYAN, 2.5, 0.0, dash=0.07))
        highlights = VGroup()
        for coil in coils:
            highlights.add(Line(coil.get_left() + RIGHT * 0.10 * scale + UP * 0.045 * scale,
                                coil.get_right() + LEFT * 0.18 * scale + UP * 0.045 * scale,
                                stroke_color="#FFE0AA", stroke_width=1.6, stroke_opacity=0.45))
        self.body = VGroup(base, legs, coils, highlights, poles)
        self.add(self.body, self.field)

    def field_on(self, opacity: float = 0.45) -> Animation:
        return self.field.animate.set_stroke(opacity=opacity)


class PourStream(VGroup):
    """Droplets of a liquid poured past an ``Electromagnet``, from a precomputed
    ``physics_models.pour``. ``clock`` advances in an updater while ``running``."""

    def __init__(self, magnet: Electromagnet, paramagnetic: bool, *, color: str | None = None, drops: int = 70,
                 seed: int = 0, duration: float = 6.0) -> None:
        super().__init__()
        self.magnet = magnet
        self.sim = pm.pour(paramagnetic, drops=drops, seed=seed, duration=duration, geo=magnet.geo)
        self.color = color or (cfg.LIQUID_O2 if paramagnetic else cfg.LIQUID_N2)
        self.clock, self.running = 0.0, False
        self.origin = magnet.gap_center - UP * magnet.geo.gap_y * magnet.scale_factor
        self.drops = VGroup()
        for _ in range(len(self.sim.paths)):
            glow = Circle(radius=0.14, stroke_width=0, fill_color=self.color, fill_opacity=0.16)
            core = Circle(radius=0.065, stroke_width=0, fill_color=self.color, fill_opacity=0.95)
            self.drops.add(VGroup(glow, core))
        self.bridge = VGroup(*[Ellipse(width=1.36 * f, height=0.86 * f, stroke_width=0, fill_color=self.color,
                                       fill_opacity=0.0) for f in np.linspace(1.0, 0.45, 5)]).move_to(magnet.gap_center)
        self.flask = self._flask()
        self.add(self.bridge, self.drops, self.flask)
        self.apply_clock()
        self.add_updater(lambda m, dt: m._advance(dt))

    def _flask(self) -> VGroup:
        top = self.origin + UP * self.magnet.geo.nozzle_y * self.magnet.scale_factor
        body = Polygon(top + np.array([-0.95, 0.95, 0]), top + np.array([0.35, 0.95, 0]), top + np.array([0.25, 0.1, 0]),
                       top + np.array([0.05, -0.02, 0]), top + np.array([-0.85, 0.1, 0]),
                       stroke_color=cfg.MUTED, stroke_width=4, fill_color=cfg.PANEL_2, fill_opacity=0.9)
        liquid = Polygon(top + np.array([-0.8, 0.5, 0]), top + np.array([0.22, 0.5, 0]), top + np.array([0.18, 0.15, 0]),
                         top + np.array([0.04, 0.05, 0]), top + np.array([-0.72, 0.15, 0]),
                         stroke_width=0, fill_color=self.color, fill_opacity=0.7)
        return VGroup(body, liquid).rotate(-0.35, about_point=top)

    def _advance(self, dt: float) -> None:
        if self.running:
            self.clock += dt
            self.apply_clock()

    def apply_clock(self) -> None:
        pts, seen = self.sim.positions(self.clock)
        s = self.magnet.scale_factor
        for drop, p, v in zip(self.drops, pts, seen):
            drop.move_to(self.origin + np.array([p[0] * s, p[1] * s, 0]))
            drop[0].set_fill(opacity=0.16 * v)
            drop[1].set_fill(opacity=0.95 * v)
        caught = self.sim.captured_by(self.clock) / max(len(self.sim.paths), 1)
        for k, layer in enumerate(self.bridge):
            layer.set_fill(opacity=0.12 * min(1.0, caught * 1.4) * (1 + 0.4 * k))

    def run(self, on: bool = True) -> None:
        self.running = on


# ----------------------------------------------------------------------------
# 2D maps of a wave function
# ----------------------------------------------------------------------------


def phase_rgba(values: np.ndarray, vmax: float, *, mode: str = "phase", gamma: float = 0.75,
               presence: float = 1.0) -> np.ndarray:
    """Colour a sampled wave function: blue (+) / rose (-) for phase, cyan to
    white for density; brightness and alpha follow |psi| (or psi^2)."""
    if mode == "density":
        level = np.clip(values ** 2 / (vmax ** 2), 0, 1) ** gamma
        low = np.array(ManimColor(cfg.DENSITY).to_rgb())
        high = np.array(ManimColor(cfg.WHITE).to_rgb())
        rgb = low[None, None, :] * (1 - level[..., None] * 0.6) + high[None, None, :] * level[..., None] * 0.6
    else:
        level = np.clip(np.abs(values) / vmax, 0, 1) ** gamma
        plus = np.array(ManimColor(cfg.PHASE_PLUS).to_rgb())
        minus = np.array(ManimColor(cfg.PHASE_MINUS).to_rgb())
        rgb = np.where(values[..., None] >= 0, plus, minus) * (0.55 + 0.45 * level[..., None])
    alpha = np.clip(level * 1.15, 0, 1) * presence
    out = np.zeros(values.shape + (4,), dtype=np.uint8)
    out[..., :3] = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)
    return out


class PhaseMap(ImageMobject):
    """A wave function on a plane, drawn as an image that can be redrawn live.

    ``func(X, Y)`` returns psi on a grid in *map units*; ``extent`` gives the
    half-width and half-height in map units, and the image is scaled to
    ``width`` screen units. ``set_func`` swaps the function (and redraws), so a
    ``Param`` can morph it frame by frame.
    """

    def __init__(self, func: Callable[[np.ndarray, np.ndarray], np.ndarray], *, extent: tuple[float, float] = (8.0, 4.5),
                 width: float = 8.0, pixels: int = 360, mode: str = "phase", vmax: float | None = None,
                 gamma: float = 0.75) -> None:
        self.func, self.extent, self.mode, self.gamma = func, extent, mode, gamma
        aspect = extent[1] / extent[0]
        self.px = (pixels, max(int(pixels * aspect), 2))
        self.xs = np.linspace(-extent[0], extent[0], self.px[0])
        self.ys = np.linspace(extent[1], -extent[1], self.px[1])
        self.vmax = vmax
        self.presence = 1.0
        super().__init__(self._render(), scale_to_resolution=1080)
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        self.width = width
        self.map_width = width

    def _grid(self):
        return np.meshgrid(self.xs, self.ys)

    def _render(self) -> np.ndarray:
        X, Y = self._grid()
        values = self.func(X, Y)
        vmax = self.vmax or float(np.max(np.abs(values))) or 1.0
        rgba = phase_rgba(values, vmax, mode=self.mode, gamma=self.gamma, presence=self.presence)
        rgba[..., 3] = (rgba[..., 3] * self._edge_mask()).astype(np.uint8)
        return rgba

    def _edge_mask(self) -> np.ndarray:
        """Feather the image edges so a map never shows as a rectangle."""
        def ramp(n):
            u = np.linspace(0, 1, n)
            edge = np.clip(np.minimum(u, 1 - u) / 0.14, 0, 1)
            return edge * edge * (3 - 2 * edge)
        return np.outer(ramp(self.px[1]), ramp(self.px[0]))

    def redraw(self) -> "PhaseMap":
        self.pixel_array = self._render()
        self.orig_alpha_pixel_array = self.pixel_array[:, :, 3].copy()
        return self

    def set_func(self, func) -> "PhaseMap":
        self.func = func
        return self.redraw()

    def to_screen(self, x: float, y: float) -> np.ndarray:
        """Screen point of a map coordinate."""
        scale = self.map_width / (2 * self.extent[0])
        return self.get_center() + np.array([x * scale, y * scale, 0.0])

    @property
    def unit(self) -> float:
        return self.map_width / (2 * self.extent[0])


def spec_func(spec: om.MOSpec, plane: str = "xy") -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    """psi of an MOSpec on the plane through the nuclei, for a PhaseMap."""
    def func(X, Y, spec=spec):
        zero = np.zeros_like(X)
        return om.psi(spec, X, Y, zero) if plane == "xy" else om.psi(spec, X, zero, Y)
    return func


def nucleus_dot(point, color: str = cfg.WHITE, radius: float = 0.08) -> VGroup:
    return glow_dot(point, color, radius=radius, reach=2.6)


# ----------------------------------------------------------------------------
# Curves of a wave function along a line
# ----------------------------------------------------------------------------


class PlotFrame:
    """Map plot coordinates (x, y) to the screen: origin plus scaled offsets."""

    def __init__(self, origin, xscale: float, yscale: float) -> None:
        self.origin = np.asarray(origin, dtype=float)
        self.xscale, self.yscale = float(xscale), float(yscale)

    def __call__(self, x, y) -> np.ndarray:
        x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
        return np.column_stack([self.origin[0] + x * self.xscale, self.origin[1] + y * self.yscale,
                                np.zeros_like(x)])

    def point(self, x: float, y: float) -> np.ndarray:
        return self(np.array([x]), np.array([y]))[0]

    def axis(self, x0: float, x1: float, color: str = cfg.MUTED, width: float = 3.0) -> Line:
        return Line(self.point(x0, 0), self.point(x1, 0), stroke_color=color, stroke_width=width, stroke_opacity=0.7)


def _runs(xs: np.ndarray, ys: np.ndarray):
    """Split a sampled curve into runs of one sign, with interpolated zero crossings."""
    runs, current, sign = [], [], 0
    for i, (x, y) in enumerate(zip(xs, ys)):
        s = 1 if y > 0 else (-1 if y < 0 else 0)
        if current and s != 0 and sign != 0 and s != sign:
            xp, yp = xs[i - 1], ys[i - 1]
            xz = xp + (x - xp) * (0 - yp) / (y - yp)
            current.append((xz, 0.0))
            runs.append((sign, current))
            current = [(xz, 0.0)]
        if s != 0:
            sign = s
        current.append((x, y))
    if current:
        runs.append((sign, current))
    return runs


def signed_curve(func: Callable[[np.ndarray], np.ndarray], x_range: tuple[float, float], frame: PlotFrame, *,
                 width: float = 6.0, samples: int = 360, plus: str = cfg.PHASE_PLUS, minus: str = cfg.PHASE_MINUS,
                 glow: bool = True) -> VGroup:
    """A curve coloured by its sign: blue where positive, rose where negative."""
    xs = np.linspace(x_range[0], x_range[1], samples)
    ys = np.asarray(func(xs), dtype=float)
    layers = {1: [], -1: []}
    for sign, run in _runs(xs, ys):
        if len(run) < 2 or sign == 0:
            continue
        arr = np.array(run)
        layers[sign].append(frame(arr[:, 0], arr[:, 1]))
    group = VGroup()
    for sign, color in ((1, plus), (-1, minus)):
        for spread, opacity in (((width * 3.2, 0.14), (width, 1.0)) if glow else ((width, 1.0),)):
            line = VMobject(stroke_color=color, stroke_width=spread, stroke_opacity=opacity, fill_opacity=0)
            for pts in layers[sign]:
                line.start_new_path(pts[0])
                line.add_points_as_corners(pts[1:])
            group.add(line)
    return group


def plain_curve(func, x_range, frame: PlotFrame, color: str, width: float = 6.0, samples: int = 360,
                glow: bool = True) -> VGroup:
    """A curve in one colour (densities, energies), with an optional soft glow."""
    xs = np.linspace(x_range[0], x_range[1], samples)
    pts = frame(xs, np.asarray(func(xs), dtype=float))
    group = VGroup()
    for spread, opacity in (((width * 3.2, 0.14), (width, 1.0)) if glow else ((width, 1.0),)):
        line = VMobject(stroke_color=color, stroke_width=spread, stroke_opacity=opacity, fill_opacity=0)
        line.set_points_as_corners(pts)
        group.add(line)
    return group


def dim_curve(curve: VGroup, factor: float) -> list[Animation]:
    """Fade every layer of a curve by the same factor (a glow stays a glow)."""
    return [part.animate.set_stroke(opacity=float(part.get_stroke_opacity()) * factor) for part in curve]


def live(builder: Callable[[], Mobject]) -> Mobject:
    """A mobject rebuilt from ``builder`` every frame (curves driven by trackers)."""
    mob = builder()
    mob.add_updater(lambda m: m.become(builder()))
    return mob


# ----------------------------------------------------------------------------
# Orbitals on a stage
# ----------------------------------------------------------------------------

S_UNITS = 1.25       # screen units per bohr for 1s pictures
P_UNITS = 0.5        # ... and for the larger 2p pictures


class MOCloud:
    """A molecular (or atomic) orbital on a stage: every lobe of |psi| = level,
    blue where psi > 0 and rose where psi < 0, recomputed when the spec changes.

    ``spec`` can be morphed with ``morph(c=..., R=...)``: the phase
    coefficient and the separation are tweened and the surface recomputed
    (quantised, and cached in ``orbital_models``) frame by frame.
    """

    def __init__(self, stage: Stage, spec: om.MOSpec, *, origin=ORIGIN, units: float | None = None, slots: int = 3,
                 opacity: float = 0.72, plus: str = cfg.PHASE_PLUS, minus: str = cfg.PHASE_MINUS,
                 step: float | None = None, presence: float = 1.0) -> None:
        self.stage, self.spec, self.origin = stage, spec, origin
        self.units = units or (S_UNITS if spec.kind == "s" else P_UNITS)
        self.step = step
        self._key, self._cache = None, {1: [], -1: []}
        self.plus = [Blob(self._maker(1, k), origin, plus, units=self.units, opacity=opacity) for k in range(slots)]
        self.minus = [Blob(self._maker(-1, k), origin, minus, units=self.units, opacity=opacity) for k in range(slots)]
        for blob in self.blobs:
            blob.presence = presence
        stage.add_body(*self.blobs)

    @property
    def blobs(self) -> list[Blob]:
        return self.plus + self.minus

    def _quantised(self) -> om.MOSpec:
        s = self.spec
        return om.MOSpec(s.kind, round(s.c * 40) / 40, round(s.R * 20) / 20, s.level, s.single)

    def _lobes(self) -> dict[int, list[np.ndarray]]:
        key = self._quantised()
        if key != self._key:
            step = self.step or (0.16 if key.kind == "s" else 0.34)
            table = {1: [], -1: []}
            for sign, verts in om.lobes(key, step=step):
                table[sign].append(verts)
            self._key, self._cache = key, table
        return self._cache

    def _maker(self, sign: int, k: int):
        def make():
            found = self._lobes()[sign]
            return found[k] if k < len(found) else None
        return make

    def morph(self, c: float | None = None, R: float | None = None, **kwargs) -> Param:
        start: dict[str, om.MOSpec] = {}
        target = {"c": c, "R": R}

        def get():
            start["spec"] = self.spec
            return 0.0

        def put(t):
            s = start["spec"]
            new_c = s.c if target["c"] is None else s.c + (target["c"] - s.c) * t
            new_r = s.R if target["R"] is None else s.R + (target["R"] - s.R) * t
            self.spec = om.MOSpec(s.kind, new_c, new_r, s.level, s.single)

        return Param(self.stage, get, put, 1.0, **kwargs)

    def fade(self, value: float, **kwargs) -> list[Param]:
        return [self.stage.fade(blob, value, **kwargs) for blob in self.blobs]

    def set_presence(self, value: float) -> None:
        for blob in self.blobs:
            blob.presence = value

    def nucleus_points(self) -> tuple[np.ndarray, np.ndarray]:
        o = np.asarray(self.origin, dtype=float)
        half = self.spec.R / 2 * self.units
        return o + LEFT * half, o + RIGHT * half


def stage_nuclei(stage: Stage, cloud: MOCloud, color: str = cfg.WHITE, radius: float = 0.12) -> list[Ball]:
    """Two small glowing nuclei that follow a cloud's separation."""
    balls = []
    for side in (-1, 1):
        def where(side=side):
            return np.asarray(cloud.origin, dtype=float) + RIGHT * side * cloud.spec.R / 2 * cloud.units
        ball = Ball(where, radius, color)
        glow = Halo(ball, cfg.GOLD, reach=2.8, peak=0.2)
        balls += [glow, ball]
    stage.add_body(*balls)
    return balls


def nodal_plane(stage: Stage, origin, normal: str = "x", size: float = 2.4, color: str = cfg.NODE,
                opacity: float = 0.1) -> Face:
    """A translucent square plane through ``origin`` (where psi = 0), added hidden."""
    o = np.asarray(origin, dtype=float)
    a, b = {"x": (UP, OUT), "y": (RIGHT, OUT), "z": (RIGHT, UP)}[normal]
    corners = [o + (a * sa + b * sb) * size / 2 for sa, sb in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
    face = Face(corners, color, opacity, 0.85)
    face.presence = 0.0
    stage.add_body(face)
    return face


def diatomic_model(stage: Stage, symbol: str, order: int, *, length: float = 2.4, origin=ORIGIN,
                   label: bool = True) -> tuple[Ball, Ball, Rod]:
    """A ball-and-stick X-X on a stage; ``length`` can change via ``stretch_bond``."""
    o = np.asarray(origin, dtype=float)
    state = {"length": length}
    left = Ball(lambda: o + LEFT * state["length"] / 2, cfg.ELEMENT_RADII[symbol], cfg.ELEMENT_COLORS[symbol],
                label=symbol if label else None)
    right = Ball(lambda: o + RIGHT * state["length"] / 2, cfg.ELEMENT_RADII[symbol], cfg.ELEMENT_COLORS[symbol],
                 label=symbol if label else None)
    rod = Rod(left, right, order)
    stage.add_body(left, right, rod)
    rod.state = state
    return left, right, rod


def stretch_bond(stage: Stage, rod: Rod, length: float, **kwargs) -> Param:
    return Param(stage, lambda: rod.state["length"], lambda v: rod.state.__setitem__("length", v), length, **kwargs)


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
                     txt("Keep following the electrons.", 36, cfg.CYAN)).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "mo", "om", "md", "np"]
