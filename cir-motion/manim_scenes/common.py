"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing synthesis reads as a conclusion rather than a new picture:

* a **vector** is a glowing filled arrow (``VecArrow`` in 2D, ``Vector`` on a
  3D ``Stage``) that *grows* out of its tail and follows live values, at its
  true length (k screen units per m/s, or per m/s^2);
* **position** and the radius are teal, **velocity** gold (always along the
  tangent), **acceleration toward the centre** and every **delta v** orange,
  **tangential acceleration** purple, **net force** green, and **angles and
  angular quantities** (theta, omega, alpha, arcs) cyan; x and y components
  are blue and rose, as in Episode 01; the total of radial and tangential
  acceleration is white;
* a particle on a circle is one ``CircleView`` (flat) or ``Circuit`` (on a
  turning 3D ground), driven by a single clock ``t`` that the ball, its
  arrows, its trail and any ghost images read, so every frame is the model's
  numbers;
* a confirmed result is gold in a glowing box; a trap is red.

Scene files compose these pieces and choreograph them against the beats in
``narration.py``; nothing in a scene file should invent a second way to draw
one of these ideas, or type a number that ``utils.physics_models`` supplies.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from manim import *

import config as cfg
from manim_scenes.stage3d import (Ball, Band, Block, Curve, Disc, Face, Grid, Halo, Param, Rod, Segment, Stage, Tag,
                                  Vector, _LiveMixin, _polished_parts)
from narration import SCRIPT
from utils import circle_data as cd
from utils import math_utils as mu
from utils import physics_models as pm
from utils.render_helpers import fit_inside, fit_to_safe_frame, fit_width

P = pm.REFERENCE


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
    add = scene.add

    def add_with_title_clock(*mobjects):
        # Start the lifetime when a heading first enters the scene. Using the
        # scene clock also works through long waits and the full-film render.
        for root in mobjects:
            for member in root.get_family():
                if getattr(member, "_is_scene_heading", False) and member._title_started is None:
                    member._title_started = float(scene.time)
                    member.add_updater(lambda mob, dt: mob.update_title(float(scene.time)))
        return add(*mobjects)

    scene.add = add_with_title_clock

    def live_partition(animations):
        if any(getattr(member, "_live_draw_order", False) for member in scene.mobjects):
            return list(scene.mobjects), []
        return partition(animations)

    scene.get_moving_and_static_mobjects = live_partition
    scene._prepared_for_stages = True


def start(scene: Scene, key: str, title: str | None = None) -> tuple[float, VGroup | None]:
    """Theme the scene, add the quiet background, and show the scene heading."""
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


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Hold the composition; live stages keep moving."""
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


def clear(scene: Scene, *keep: Mobject, run_time: float = 0.8, others: Sequence[Animation] = ()) -> None:
    """Fade out everything on screen except the background and ``keep``; stop their updaters first."""
    gone = [m for m in scene.mobjects if not getattr(m, "_is_project_background", False) and m not in keep]
    for mob in gone:
        for member in mob.get_family():
            member.clear_updaters()
    if gone:
        scene.play(*[FadeOut(m) for m in gone], *others, run_time=run_time)
        scene.remove(*gone)
    elif others:
        scene.play(*others, run_time=run_time)


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


class Knob:
    """A plain number that animations can tween and updaters can read."""

    def __init__(self, value: float) -> None:
        self.value = float(value)

    def to(self, holder: Mobject, value: float, **kwargs) -> Param:
        return Param(holder, lambda: self.value, lambda v: setattr(self, "value", v), value, **kwargs)

    def __call__(self) -> float:
        return self.value


def set_attr(holder: Mobject, obj, name: str, value: float, **kwargs) -> Param:
    """Tween ``obj.name`` (any attribute a live object reads every frame)."""
    return Param(holder, lambda: getattr(obj, name), lambda v: setattr(obj, name, v), value, **kwargs)


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


def paint(tex: MathTex, colors: dict[int, str]) -> MathTex:
    """Colour parts of a multi-part MathTex by index: horizontal blue, vertical rose, ..."""
    for index, color in colors.items():
        tex[index].set_color(color)
    return tex


def decorative(mob: Mobject) -> Mobject:
    """Mark a glow or shadow copy so the layout audit does not read it as text."""
    for member in mob.get_family():
        member._is_decorative = True
    return mob


class IntroHeading(_LiveMixin, VGroup):
    """A scene heading that fades without extending any narration cue."""

    def __init__(self, *parts: Mobject) -> None:
        super().__init__(*parts)
        self._is_scene_heading = True
        self._title_started = None
        self._title_alpha = None
        self._title_parts = self.family_members_with_points()
        self._title_base = [(part.fill_rgbas[:, 3].copy(), part.stroke_rgbas[:, 3].copy(),
                             part.background_stroke_rgbas[:, 3].copy()) for part in self._title_parts]

    def update_title(self, now: float) -> None:
        # FadeIn/FadeOut own their copied opacity. A copied title's updater
        # must not repaint that hidden animation template while it fades.
        if not self._live:
            return
        elapsed = now - self._title_started
        progress = np.clip((elapsed - cfg.TIMING["title_hold"]) / cfg.TIMING["title_fade"], 0, 1)
        alpha = 1.0 - smooth(float(progress))
        if alpha == self._title_alpha:
            return
        for part, (fill, stroke, outline) in zip(self._title_parts, self._title_base):
            part.fill_rgbas[:, 3] = fill * alpha
            part.stroke_rgbas[:, 3] = stroke * alpha
            part.background_stroke_rgbas[:, 3] = outline * alpha
        self._title_alpha = alpha


def heading(title: str, color: str = cfg.GOLD, size: int = 48) -> VGroup:
    """Gold scene title, held for three seconds and faded over 0.7 seconds."""
    main = txt(title, size, color)
    fit_width(main, 13.6)
    shadow = main.copy().set_color(cfg.BG).set_opacity(0.85).shift(RIGHT * 0.05 + DOWN * 0.05)
    shadow.set_stroke(width=0)
    decorative(shadow)
    glow = main.copy().set_fill(opacity=0).set_stroke(color, width=12, opacity=0.14)
    decorative(glow)
    group = IntroHeading(shadow, glow, main)
    group.move_to(UP * 3.86)
    group.main = main
    return group


def caption(body: str, color: str = cfg.WHITE, size: int | None = None, y: float = -3.72) -> Text:
    """A short bottom caption, on a phone-readable size."""
    line = txt(body, size or cfg.FONT["body"], color)
    fit_width(line, 13.4)
    return line.move_to(UP * y)


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
    """Old fully out before the new one comes in, as one animation that can
    share a play with other motion (no ghosted, overlapping words)."""
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
    label = eq(latex, size or cfg.FONT["body"], color)
    pill = RoundedRectangle(width=label.width + 0.7, height=label.height + 0.4, corner_radius=0.22,
                            stroke_color=stroke or color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.92)
    group = VGroup(pill, label.move_to(pill))
    group.pill, group.label = pill, label
    return group


def panel(width: float, height: float, color: str = cfg.MUTED, opacity: float = 0.82) -> RoundedRectangle:
    return RoundedRectangle(width=width, height=height, corner_radius=0.22, stroke_color=color, stroke_width=2,
                            stroke_opacity=0.6, fill_color=cfg.PANEL, fill_opacity=opacity)


def on_panel(mob: Mobject, color: str = cfg.MUTED, pad: float = 0.35, opacity: float = 0.82) -> VGroup:
    """Put a block of equations on a rounded panel sized to fit it."""
    back = panel(mob.width + 2 * pad, mob.height + 2 * pad, color, opacity).move_to(mob)
    group = VGroup(back, mob)
    group.back, group.body = back, mob
    return group


def glow_frame(mob: Mobject, color: str = cfg.GOLD, buff: float = 0.14, width: float = 4) -> VGroup:
    """A glowing rounded outline around anything — the film's 'look here'."""
    w, h = mob.width + 2 * buff, mob.height + 2 * buff
    group = VGroup()
    for spread, opacity in ((14, 0.10), (8, 0.18), (width, 1.0)):
        group.add(RoundedRectangle(width=w, height=h, corner_radius=min(0.2, h / 3), stroke_color=color,
                                   stroke_width=spread, stroke_opacity=opacity, fill_opacity=0))
    return group.move_to(mob)


def boxed(mob: Mobject, color: str = cfg.RESULT, buff: float = 0.22) -> VGroup:
    """A result in a glowing box (the film's \\boxed{})."""
    return VGroup(glow_frame(mob, color, buff=buff), mob)


def title_card(big: str, small: str, color: str = cfg.GOLD) -> VGroup:
    """The film's title: a big warm line and a smaller cyan one, with an outline,
    an offset shadow and a soft glow."""
    line_one = Text(big, font=cfg.TITLE_FONT, weight=BOLD, font_size=92, color=color)
    line_two = Text(small, font=cfg.TITLE_FONT, weight=BOLD, font_size=54, color=cfg.CYAN)
    title = VGroup(line_one, line_two).arrange(DOWN, buff=0.3)
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


def chapter_card(number: int, title: str) -> VGroup:
    """A chapter opener: a big glowing number in a ring, and the chapter's name."""
    ring = VGroup(*[Circle(radius=0.95, stroke_color=cfg.GOLD, stroke_width=w, stroke_opacity=o, fill_opacity=0)
                    for w, o in ((22, 0.08), (12, 0.16), (5, 1.0))])
    digits = Text(f"{number:02d}", font=cfg.TITLE_FONT, weight=BOLD, font_size=88, color=cfg.GOLD)
    digits.set_stroke("#351F05", width=3, opacity=0.8, background=True).move_to(ring)
    label = txt("CHAPTER", cfg.FONT["small"], cfg.CYAN)
    name = txt(title, cfg.FONT["title"], cfg.WHITE)
    fit_width(name, 12.4)
    words = VGroup(label, name).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    card = VGroup(VGroup(ring, digits), words).arrange(RIGHT, buff=0.6).move_to(ORIGIN)
    card.ring, card.digits, card.words = ring, digits, words
    return card


def show_chapter(scene: Scene, number: int, title: str, hold: float = 1.6) -> None:
    """A brief title-only opener; chapter numbering belongs in the video index."""
    card = txt(title, cfg.FONT["title"], cfg.WHITE)
    fit_width(card, 12.4)
    card.move_to(ORIGIN)
    scene.play(FadeIn(card, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(hold)
    scene.play(FadeOut(card, shift=UP * 0.3), run_time=0.6)


def result_label(name: str, color: str = cfg.RESULT, size: int | None = None) -> VGroup:
    """A revealed result: coloured type with a soft glow behind it."""
    label = txt(name, size or cfg.FONT["section"], color)
    glow = label.copy().set_stroke(color, width=14, opacity=0.16).set_fill(opacity=0)
    decorative(glow)
    group = VGroup(glow, label)
    group.label = label
    return group


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


def bead(point, color: str, radius: float = 0.14, glow: float = 0.0) -> VGroup:
    """A side-view sphere with the same lighting as the projected 3D balls."""
    parts = _polished_parts(color, 14)
    for part in parts:
        part.scale(radius, about_point=ORIGIN)
    if glow:
        parts.insert(0, halo(radius * 2.8, color, layers=4, peak_opacity=0.2 * glow))
    return VGroup(*parts).move_to(point)


def check_mark(size: float = 0.32, color: str = cfg.GREEN) -> VMobject:
    mark = VMobject(stroke_color=color, stroke_width=9)
    mark.set_points_as_corners([LEFT * size + UP * 0.05, DOWN * size * 0.75 + LEFT * size * 0.15, RIGHT * size + UP * size])
    return mark


def cross_mark(size: float = 0.3, color: str = cfg.RED) -> VGroup:
    return VGroup(Line(UL * size, DR * size, stroke_color=color, stroke_width=10),
                  Line(UR * size, DL * size, stroke_color=color, stroke_width=10))


def strike(mob: Mobject, color: str = cfg.RED, width: float = 8) -> Line:
    """A red line through a wrong term."""
    return Line(mob.get_corner(DL) + LEFT * 0.08, mob.get_corner(UR) + RIGHT * 0.08, stroke_color=color,
                stroke_width=width)


def dashed_path(a, b, color: str = cfg.MUTED, width: float = 2.4, opacity: float = 0.55, dash: float = 0.13,
                count: int | None = None) -> VMobject:
    """A dashed segment. Pass a fixed ``count`` for a live (updater-rebuilt) line, so its
    point count never changes mid-animation."""
    line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    count = count or max(int(float(np.linalg.norm(b - a)) / (2 * dash)), 1)
    for k in range(count):
        line.start_new_path(a + (b - a) * k / count)
        line.add_line_to(a + (b - a) * (k + 0.55) / count)
    return line


def angle_arc(centre, start_deg: float, sweep_deg: float, radius: float = 0.7, color: str = cfg.WHITE,
              width: float = 4) -> Arc:
    return Arc(radius=radius, start_angle=start_deg * DEGREES, angle=sweep_deg * DEGREES, arc_center=centre,
               stroke_color=color, stroke_width=width)


def right_angle_mark(corner, along, up, size: float = 0.26, color: str = cfg.MUTED) -> VMobject:
    corner, along, up = (np.asarray(v, dtype=float) for v in (corner, along, up))
    mark = VMobject(stroke_color=color, stroke_width=3, fill_opacity=0)
    mark.set_points_as_corners([corner + along * size, corner + (along + up) * size, corner + up * size])
    return mark


def countdown(scene: Scene, at, seconds: int = 3, color: str = cfg.GOLD) -> None:
    """A shrinking ring with 3, 2, 1 — the challenges' thinking time."""
    for k in range(seconds, 0, -1):
        digit = txt(str(k), 80, color).move_to(at)
        ring = Circle(radius=0.62, stroke_color=color, stroke_width=7, fill_opacity=0).move_to(at)
        scene.add(digit, ring)
        scene.play(Uncreate(ring), digit.animate.set_opacity(0.15), run_time=1.0, rate_func=linear)
        scene.remove(digit, ring)


# ----------------------------------------------------------------------------
# 2D vectors
# ----------------------------------------------------------------------------


def arrow_outline(p: np.ndarray, q: np.ndarray, width: float, tip: float) -> list[np.ndarray] | None:
    """Polygon of a filled arrow from p to q (the same shape as a stage ``Vector``)."""
    span = q - p
    n = np.linalg.norm(span[:2])
    if n < 1e-4:
        return None
    d = span / n
    side = np.array([-d[1], d[0], 0.0])
    tip = min(tip, 0.6 * n)
    neck = q - d * tip
    return [p + side * width / 2, neck + side * width / 2, neck + side * width * 1.6, q, neck - side * width * 1.6,
            neck - side * width / 2, p - side * width / 2, p + side * width / 2]


class VecArrow(_LiveMixin, VGroup):
    """A glowing filled arrow whose tail and tip may be points or live functions.

    ``grow`` (0..1) draws it out of its tail; tween it with ``grow_in`` rather
    than GrowArrow, so a live arrow is never copied by a Transform."""

    def __init__(self, tail, tip, color: str, *, width: float = 0.1, tip_len: float = 0.32, glow: bool = True,
                 grow: float = 1.0, live: bool = True) -> None:
        super().__init__()
        self.tail_src, self.tip_src = tail, tip
        # Never self.width: that is Mobject's bounding-box width, and setting it rescales.
        self.thickness, self.tip_len, self.grow, self.alpha = width, tip_len, float(grow), 1.0
        self.halo = VMobject(stroke_width=0, fill_color=color, fill_opacity=0.18 if glow else 0)
        self.body = VMobject(stroke_color=mu.shade(color, 0.55), stroke_width=1.5, fill_color=color, fill_opacity=1)
        self.glow = glow
        self.add(self.halo, self.body)
        self.refresh()
        if live:   # a static arrow (an icon) can be arranged and shifted like any shape
            self.add_updater(lambda m: m.refresh() if m._live else None)

    def tail(self) -> np.ndarray:
        return np.asarray(self.tail_src() if callable(self.tail_src) else self.tail_src, dtype=float)

    def tip(self) -> np.ndarray:
        return np.asarray(self.tip_src() if callable(self.tip_src) else self.tip_src, dtype=float)

    def head(self) -> np.ndarray:
        """Where the drawn tip currently is (allowing for ``grow``)."""
        p = self.tail()
        return p + (self.tip() - p) * self.grow

    def refresh(self) -> "VecArrow":
        p, q = self.tail(), self.head()
        outline = arrow_outline(p, q, self.thickness, self.tip_len)
        if outline is None or self.alpha <= 0.004:
            self.body.points = np.zeros((0, 3))
            self.halo.points = np.zeros((0, 3))
            return self
        self.body.set_points_as_corners(outline)
        self.halo.set_points_as_corners(arrow_outline(p, q, self.thickness * 1.8, self.tip_len * 1.08))
        self.body.set_fill(opacity=self.alpha).set_stroke(opacity=self.alpha)
        self.halo.set_fill(opacity=(0.10 if self.glow else 0) * self.alpha)
        return self

    def put(self, tail=None, tip=None) -> "VecArrow":
        if tail is not None:
            self.tail_src = tail
        if tip is not None:
            self.tip_src = tip
        return self.refresh()

    def grow_in(self, **kwargs) -> Param:
        self.grow = 0.0
        self.refresh()
        return Param(self, lambda: self.grow, lambda v: setattr(self, "grow", v), 1.0, **kwargs)

    def fade_to(self, value: float, **kwargs) -> Param:
        return Param(self, lambda: self.alpha, lambda v: setattr(self, "alpha", v), value, **kwargs)


def plane(x_range=(-1, 7), y_range=(-1, 5), unit: float = 0.8, at=ORIGIN, labels: bool = True,
          faint: float = 0.45, step: float = 1) -> NumberPlane:
    """A coordinate grid in the film's style: faint blue lines, blue x-axis, rose y-axis.

    ``plane.c2p(x, y)`` maps coordinates to the screen; ``at`` is where (0, 0) lands."""
    grid = NumberPlane(x_range=(x_range[0], x_range[1], step), y_range=(y_range[0], y_range[1], step),
                       x_length=(x_range[1] - x_range[0]) * unit, y_length=(y_range[1] - y_range[0]) * unit,
                       background_line_style={"stroke_color": cfg.GRID, "stroke_width": 1.6, "stroke_opacity": faint},
                       axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3, "include_tip": False},
                       faded_line_ratio=1)
    grid.x_axis.set_stroke(cfg.X_COLOR, width=3.5, opacity=0.85)
    grid.y_axis.set_stroke(cfg.Y_COLOR, width=3.5, opacity=0.85)
    grid.shift(np.asarray(at, dtype=float) - grid.c2p(0, 0))
    grid.unit = unit
    if labels:
        x_label = eq("x", cfg.FONT["small"], cfg.X_COLOR).next_to(grid.c2p(x_range[1], 0), UR, buff=0.12)
        y_label = eq("y", cfg.FONT["small"], cfg.Y_COLOR).next_to(grid.c2p(0, y_range[1]), UR, buff=0.12)
        grid.add(x_label, y_label)
        grid.labels = VGroup(x_label, y_label)
    return grid


def vec_on(grid: NumberPlane, tail, tip, color: str, **kwargs) -> VecArrow:
    """A vector between two coordinate points on a plane (tuples or live functions)."""

    def pt(spec):
        if callable(spec):
            return lambda: grid.c2p(*spec())
        return grid.c2p(*spec)

    return VecArrow(pt(tail), pt(tip), color, **kwargs)


def label_at(mob: Mobject, arrow: VecArrow, side=UP, buff: float = 0.18, along: float = 0.55) -> Mobject:
    """Place a label beside the middle of an arrow, on the given side of its direction."""
    p, q = arrow.tail(), arrow.tip()
    d = q - p
    n = np.linalg.norm(d[:2])
    normal = np.array([-d[1], d[0], 0.0]) / n if n > 1e-6 else UP
    if np.dot(normal, side) < 0:
        normal = -normal
    point = p + d * along + normal * (buff + 0.5 * max(mob.width * abs(normal[0]), mob.height * abs(normal[1])))
    return mob.move_to(point)


# ----------------------------------------------------------------------------
# Real-world props (2D)
# ----------------------------------------------------------------------------


class Car(VGroup):
    """A top-down car pointing along +x; ``set_pose`` moves and turns it without Transforms."""

    def __init__(self, color: str = cfg.CYAN, length: float = 1.1) -> None:
        super().__init__()
        w = length * 0.52
        body = RoundedRectangle(width=length, height=w, corner_radius=w * 0.32, stroke_color=mu.shade(color, 0.6),
                                stroke_width=2, fill_color=color, fill_opacity=1)
        roof = RoundedRectangle(width=length * 0.46, height=w * 0.72, corner_radius=w * 0.2, stroke_width=0,
                                fill_color=mu.shade(color, 0.72), fill_opacity=1).shift(LEFT * length * 0.04)
        glass = RoundedRectangle(width=length * 0.14, height=w * 0.66, corner_radius=0.04, stroke_width=0,
                                 fill_color="#CFE8F7", fill_opacity=0.85).shift(RIGHT * length * 0.22)
        wheels = VGroup(*[RoundedRectangle(width=length * 0.2, height=w * 0.14, corner_radius=0.03, stroke_width=0,
                                           fill_color="#14212C", fill_opacity=1)
                          .move_to([sx * length * 0.3, sy * w * 0.53, 0]) for sx in (-1, 1) for sy in (-1, 1)])
        lights = VGroup(*[Circle(radius=w * 0.08, stroke_width=0, fill_color="#FFF3C4", fill_opacity=1)
                          .move_to([length * 0.47, sy * w * 0.28, 0]) for sy in (-1, 1)])
        self.add(wheels, body, roof, glass, lights)
        self.parts = [m for m in self.get_family() if len(m.points)]
        self.templates = [m.points.copy() for m in self.parts]
        self.pose = (np.zeros(3), 0.0)

    def set_pose(self, point, heading: float) -> "Car":
        c, s = np.cos(heading), np.sin(heading)
        rot = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        point = np.asarray(point, dtype=float)
        for m, t in zip(self.parts, self.templates):
            m.points = t @ rot.T + point
        self.pose = (point, heading)
        return self


class Speedometer(VGroup):
    """A round gauge reading ``value`` (m/s, a Knob) with a needle and a digital readout."""

    def __init__(self, at=ORIGIN, *, top: float = 40.0, radius: float = 1.25, color: str = cfg.CYAN,
                 value: float = 0.0, unit_gap: float = 0.26, unit: str = "m/s", step: int = 5) -> None:
        super().__init__()
        self.top, self.r = top, radius
        self.unit_gap = unit_gap
        self.value = Knob(value)
        face = Circle(radius=radius, stroke_color=cfg.MUTED, stroke_width=4, fill_color=cfg.PANEL, fill_opacity=0.95)
        arc = Arc(radius=radius * 0.86, start_angle=-40 * DEGREES, angle=260 * DEGREES, stroke_color=color,
                  stroke_width=6)
        ticks = VGroup()
        for k in range(0, int(top) + 1, step):
            a = self._angle(k)
            inner = radius * (0.68 if k % (2 * step) == 0 else 0.75)
            ticks.add(Line([np.cos(a) * inner, np.sin(a) * inner, 0], [np.cos(a) * radius * 0.84, np.sin(a) * radius * 0.84, 0],
                           stroke_color=cfg.WHITE, stroke_width=3 if k % (2 * step) == 0 else 2))
        self.needle = VMobject(stroke_width=0, fill_color=cfg.ORANGE, fill_opacity=1)
        hub = Circle(radius=0.09, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=1)
        self.readout = DecimalNumber(value, num_decimal_places=0, font_size=40, color=cfg.WHITE)
        self.unit = txt(unit, 24, cfg.MUTED)
        self.add(face, arc, ticks, self.needle, hub, self.readout, self.unit)
        self.face = face
        self.move_to(at)
        self.needle.add_updater(lambda m: self._draw())
        self._draw()

    def _angle(self, v: float) -> float:
        return (220 - 260 * v / self.top) * DEGREES

    def _draw(self) -> None:
        c = self.face.get_center()
        a = self._angle(self.value.value)
        d = np.array([np.cos(a), np.sin(a), 0.0])
        side = np.array([-d[1], d[0], 0.0])
        self.needle.set_points_as_corners([c + side * 0.06, c + d * self.r * 0.8, c - side * 0.06, c + side * 0.06])
        self.readout.set_value(self.value.value)
        self.readout.move_to(c + DOWN * self.r * 0.42)
        self.unit.next_to(self.readout, DOWN, buff=self.unit_gap)


class Thermometer(VGroup):
    """A glowing thermometer whose column follows ``celsius`` (a Knob)."""

    def __init__(self, at=ORIGIN, *, low: float = -20.0, high: float = 40.0, height: float = 4.0,
                 color: str = cfg.RED) -> None:
        super().__init__()
        self.low, self.high = low, high
        self.celsius = Knob(20.0)
        self.color = color
        tube = RoundedRectangle(width=0.36, height=height, corner_radius=0.18, stroke_color=cfg.MUTED, stroke_width=3,
                                fill_color=cfg.PANEL, fill_opacity=0.9)
        bulb = Circle(radius=0.32, stroke_color=cfg.MUTED, stroke_width=3, fill_color=color, fill_opacity=1)
        bulb.next_to(tube, DOWN, buff=-0.12)
        self.tube, self.bulb = tube, bulb
        self.column = Rectangle(width=0.18, height=0.1, stroke_width=0, fill_color=color, fill_opacity=1)
        zero = Line(LEFT * 0.3, RIGHT * 0.3, stroke_color=cfg.WHITE, stroke_width=3)
        self.zero = zero
        self.add(tube, bulb, self.column, zero)
        self.move_to(at)
        zero.move_to([tube.get_center()[0], self.y_for(0.0), 0])
        self.column.add_updater(lambda m: self._fit_column())
        self._fit_column()

    def y_for(self, celsius: float) -> float:
        bottom = self.tube.get_bottom()[1] + 0.2
        return bottom + (celsius - self.low) / (self.high - self.low) * (self.tube.height - 0.4)

    def _fit_column(self) -> None:
        bottom = self.tube.get_bottom()[1] + 0.05
        top = self.y_for(self.celsius.value)
        self.column.stretch_to_fit_height(max(top - bottom, 0.02))
        self.column.move_to([self.tube.get_center()[0], (top + bottom) / 2, 0])
        self.column.set_fill(cfg.BLUE if self.celsius.value < 0 else self.color)
        self.bulb.set_fill(cfg.BLUE if self.celsius.value < 0 else self.color)


def stopwatch(at=ORIGIN, radius: float = 0.9, color: str = cfg.CYAN) -> VGroup:
    """A stopwatch face; its ``hand`` can be rotated about ``centre``."""
    face = Circle(radius=radius, stroke_color=color, stroke_width=5, fill_color=cfg.PANEL, fill_opacity=0.95)
    crown = RoundedRectangle(width=0.3, height=0.22, corner_radius=0.05, stroke_width=0, fill_color=color,
                             fill_opacity=1).next_to(face, UP, buff=0.02)
    ticks = VGroup(*[Line(UP * radius * 0.78, UP * radius * 0.9, stroke_color=cfg.WHITE, stroke_width=3)
                     .rotate(-k * TAU / 12, about_point=ORIGIN) for k in range(12)])
    hand = Line(ORIGIN, UP * radius * 0.72, stroke_color=cfg.ORANGE, stroke_width=6)
    group = VGroup(face, crown, ticks, hand).move_to(at)
    ticks.move_to(face)
    hand.put_start_and_end_on(face.get_center(), face.get_center() + UP * radius * 0.72)
    group.face, group.hand = face, hand
    return group


def compass(at=ORIGIN, size: float = 0.9, color: str = cfg.MUTED) -> VGroup:
    """N / E / S / W around a small cross: map directions for the walks."""
    cross = VGroup(Line(UP * size, DOWN * size, stroke_color=color, stroke_width=3),
                   Line(LEFT * size, RIGHT * size, stroke_color=color, stroke_width=3))
    letters = VGroup(*[txt(s, cfg.FONT["tiny"], color).move_to(d * (size + 0.3))
                       for s, d in (("N", UP), ("E", RIGHT), ("S", DOWN), ("W", LEFT))])
    return VGroup(cross, letters).move_to(at)




# ----------------------------------------------------------------------------
# Numbers: always from the model, formatted the way they are spoken
# ----------------------------------------------------------------------------


def fx(value: float, decimals: int) -> str:
    """On-screen number with exactly the digits the narrator says."""
    return cd.fixed(value, decimals)


def wh(value: float) -> str:
    """A whole number from the model, refused if it is not whole."""
    return cd.whole(value)


V = wh(P.v)                      # 4
R_M = wh(P.r)                    # 2
MASS = wh(P.m)                   # 2
OMEGA = wh(P.angular_speed)      # 2
AC = wh(P.accel)                 # 8
FC = wh(P.force)                 # 16
PERIOD = fx(P.period, 2)         # 3.14
FREQ = fx(P.frequency, 3)        # 0.318


def chapter_open(scene: Scene, number: int, title: str, hold: float = 1.3) -> None:
    """A chapter opener held briefly while the narration starts."""
    show_chapter(scene, number, title, hold)


def legend(*items: tuple[str, str], size: int | None = None) -> VGroup:
    """A row of little arrows with their symbols: legend((r"\\vec v", cfg.VELOCITY), ...)."""
    row = VGroup()
    for symbol, color in items:
        icon = VecArrow(LEFT * 0.32, RIGHT * 0.32, color, width=0.07, tip_len=0.2, live=False)
        row.add(VGroup(icon, eq(symbol, size or cfg.FONT["small"], color)).arrange(RIGHT, buff=0.14))
    return row.arrange(RIGHT, buff=0.55)


def number_line(value: Callable[[], float], decimals: int, unit: str, color: str = cfg.WHITE,
                size: int = 56, label: str | None = None, label_color: str = cfg.MUTED) -> VGroup:
    """A live readout: optional label, a DecimalNumber that follows ``value()``, a unit."""
    number = DecimalNumber(value(), num_decimal_places=decimals, font_size=size, color=color)
    number.set_stroke(cfg.BG, width=0.65, opacity=0.85, background=True)
    unit_mob = txt(unit, int(size * 0.62), cfg.MUTED)
    parts = [number, unit_mob]
    head = None
    if label:
        head = txt(label, int(size * 0.62), label_color)
        parts.insert(0, head)
    row = VGroup(*parts)

    def follow(m):
        number.set_value(value())
        if head is not None:
            number.next_to(head, RIGHT, buff=0.25)
        unit_mob.next_to(number, RIGHT, buff=0.18, aligned_edge=DOWN)

    row.arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
    row.add_updater(follow)
    row.number = number
    return row


# ----------------------------------------------------------------------------
# A particle on a circle, flat on screen: one clock drives every part
# ----------------------------------------------------------------------------


class CircleView:
    """A particle on a circle drawn on screen, driven by ``clock`` (seconds, a Knob).

    ``model`` is a ``pm.Circular`` (constant omega) or a ``pm.SpeedingUp``
    (omega grows); ``phase`` rotates the start. ``R`` is the screen radius;
    ``kv`` and ``ka`` convert m/s and m/s^2 to screen units, so every arrow
    keeps its true magnitude. ``arrow(kind)`` gives a live VecArrow:
    'r' (centre to particle), 'v', 'vx', 'vy', 'a' (centripetal), 'at'
    (tangential), 'atot' (total). Pass ``when=`` to freeze an arrow at an
    instant instead of following the clock."""

    def __init__(self, centre=ORIGIN, R: float = 2.0, model=P, *, kv: float | None = None, ka: float | None = None,
                 phase: float = 0.0, ball_color: str = cfg.BALL, ball_radius: float = 0.17,
                 ring_color: str = cfg.MUTED, ring_opacity: float = 0.75) -> None:
        self.c = np.asarray(centre, dtype=float)
        self.R, self.model, self.phase = float(R), model, float(phase)
        self.clock = Knob(0.0)
        speed0 = float(self.r_m * abs(self.omega(0.0)))
        accel0 = float(self.r_m * self.omega(0.0) ** 2)
        self.kv = kv if kv is not None else 0.55 * R / max(speed0, 1e-9)
        self.ka = ka if ka is not None else 0.42 * R / max(accel0, 1e-9)
        self.ring = Circle(radius=R, stroke_color=ring_color, stroke_width=4, stroke_opacity=ring_opacity,
                           fill_opacity=0).move_to(self.c)
        self.hub = Dot(self.c, radius=0.06, color=cfg.MUTED)
        self.ball = bead(self.point(), ball_color, ball_radius)
        self.ball.keep_in_frame = True
        self.ball.add_updater(lambda m: m.move_to(self.point()))

    # --- the model, read at the clock (or at a given instant) ------------------------------------
    @property
    def r_m(self) -> float:
        return float(self.model.r)

    def _t(self, when) -> float:
        return self.clock.value if when is None else float(when)

    def theta(self, when=None) -> float:
        return float(self.model.theta(self._t(when))) + self.phase

    def omega(self, when=None) -> float:
        w = self.model.omega
        return float(w(self._t(when))) if callable(w) else float(w)

    def alpha(self) -> float:
        return float(getattr(self.model, "alpha", 0.0))

    def unit_r(self, when=None) -> np.ndarray:
        th = self.theta(when)
        return np.array([np.cos(th), np.sin(th), 0.0])

    def unit_t(self, when=None) -> np.ndarray:
        th = self.theta(when)
        return np.array([-np.sin(th), np.cos(th), 0.0])

    def point(self, when=None) -> np.ndarray:
        return self.c + self.R * self.unit_r(when)

    def at_angle(self, theta: float, scale: float = 1.0) -> np.ndarray:
        return self.c + self.R * scale * np.array([np.cos(theta), np.sin(theta), 0.0])

    def vel(self, when=None) -> np.ndarray:
        """Velocity in m/s, as a screen-direction vector."""
        return self.r_m * self.omega(when) * self.unit_t(when)

    def acc_radial(self, when=None) -> np.ndarray:
        return -self.r_m * self.omega(when) ** 2 * self.unit_r(when)

    def acc_tangential(self, when=None) -> np.ndarray:
        return self.r_m * self.alpha() * self.unit_t(when)

    # --- drawing ---------------------------------------------------------------------------------------
    def arrow(self, kind: str, color: str | None = None, *, when=None, from_centre: bool = False, **kwargs) -> VecArrow:
        here = (lambda: self.point(when))
        ends = {
            "r": (lambda: self.c, here, cfg.POSITION),
            "v": (here, lambda: here() + self.vel(when) * self.kv, cfg.VELOCITY),
            "vx": (here, lambda: here() + np.array([self.vel(when)[0], 0, 0]) * self.kv, cfg.X_COLOR),
            "vy": (here, lambda: here() + np.array([0, self.vel(when)[1], 0]) * self.kv, cfg.Y_COLOR),
            "a": (here, lambda: here() + self.acc_radial(when) * self.ka, cfg.ACCEL),
            "at": (here, lambda: here() + self.acc_tangential(when) * self.ka, cfg.TANGENTIAL),
            "atot": (here, lambda: here() + (self.acc_radial(when) + self.acc_tangential(when)) * self.ka, cfg.WHITE),
        }
        tail, tip, default = ends[kind]
        if from_centre:   # the same vector, moved to a shared tail at the centre (the velocity circle)
            span = lambda: tip() - tail()  # noqa: E731
            tail, tip = (lambda: self.c), (lambda: self.c + span())
        live = kwargs.pop("live", True) and when is None
        return VecArrow(tail, tip, color or default, live=live, **kwargs)

    def trail(self, color: str = cfg.GOLD, start: float = 0.0, width: float = 5.0) -> VMobject:
        path = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)

        def draw(m):
            ts = np.linspace(start, max(self.clock.value, start + 1e-3), 90)
            m.set_points_as_corners([self.point(t) for t in ts])

        path.add_updater(draw)
        draw(path)
        return path

    def run(self, until: float, run_time: float | None = None, **kwargs) -> Param:
        """Advance the clock to ``until`` seconds (at real time unless ``run_time`` is given)."""
        kwargs.setdefault("rate_func", linear)
        return self.clock.to(self.ball, until, run_time=run_time or max(abs(until - self.clock.value), 0.1), **kwargs)

    def turns(self, laps: float, run_time: float, **kwargs) -> Param:
        """Advance by ``laps`` revolutions of the (constant-omega) model."""
        return self.run(self.clock.value + laps * 2 * np.pi / abs(self.omega()), run_time, **kwargs)

    def parts(self) -> VGroup:
        return VGroup(self.ring, self.hub, self.ball)


def arc_mark(centre, radius: float, start: float, stop: float, color: str = cfg.ANGLE, width: float = 5) -> VMobject:
    """An angle arc between two directions (radians), drawn counterclockwise."""
    if stop < start:
        start, stop = stop, start
    angles = np.linspace(start, stop, 48)   # fixed count: live arcs keep their point layout
    arc = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
    c = np.asarray(centre, dtype=float)
    arc.set_points_as_corners([c + radius * np.array([np.cos(a), np.sin(a), 0]) for a in angles])
    return arc


def live(mob: Mobject, build: Callable[[], Mobject]) -> Mobject:
    """Rebuild ``mob`` from ``build()`` every frame, primed once so it can fade in at once."""
    mob.add_updater(lambda m: m.become(build()))
    mob.become(build())
    return mob


def tangent_line(view: CircleView, when=None, half: float = 2.2, color: str = cfg.MUTED) -> VMobject:
    p, d = view.point(when), view.unit_t(when)
    return dashed_path(p - d * half, p + d * half, color, width=3, opacity=0.7)


# ----------------------------------------------------------------------------
# 3D: the ground, a particle (or car) on a circle on it, tracks, a globe
# ----------------------------------------------------------------------------


def ground(x: float, y: float, h: float = 0.0, origin=(0.0, 0.0, 0.0)) -> np.ndarray:
    """Plane coordinates (x east, y north, seen from above) -> a stage point; h is height."""
    return np.asarray(origin, dtype=float) + np.array([x, h, -y])


def ground_vec(v2) -> np.ndarray:
    """A screen-plane direction (x, y[, 0]) -> the matching direction on the ground."""
    return np.array([v2[0], 0.0, -v2[1]])


def field_stage(at=(0, -0.8, 0), *, zoom: float = 1.0, yaw: float = 0.0, pitch: float = 0.9, spin: float = 0.0,
                sway: float = 0.03, half: float = 4.0, step: float = 0.5, grid_opacity: float = 0.36) -> Stage:
    """A turning stage with a ruled ground square (y = 0) of half-size ``half``."""
    stage = Stage(at, zoom=zoom, yaw=yaw, pitch=pitch, spin=spin, sway=sway)
    floor = Grid((0, 0, 0), (1, 0, 0), (0, 0, 1), (-half, half), (-half, half), step=step, major=2, color=cfg.GRID,
                 opacity=grid_opacity, fill=cfg.GROUND, fill_opacity=0.12)
    stage.add_body(floor)
    stage.ground = floor
    return stage


def ring_points(centre, radius: float, n: int = 120, start: float = 0.0, stop: float = 2 * np.pi,
                h: float = 0.0, closed: bool = True) -> np.ndarray:
    a = np.linspace(start, stop, n, endpoint=not closed)
    c = np.asarray(centre, dtype=float)
    return np.array([c + ground(radius * np.cos(t), radius * np.sin(t), h) for t in a])


def ring_curve(centre, radius: float, n: int = 160, h: float = 0.0) -> np.ndarray:
    """A closed ring for a Curve (the first point repeated at the end)."""
    pts = ring_points(centre, radius, n, h=h)
    return np.vstack([pts, pts[:1]])


def car3d(stage: Stage, where: Callable[[], np.ndarray], heading: Callable[[], float], color: str = cfg.CAR,
          length: float = 0.9) -> list[Block]:
    """A small car whose ground point follows ``where()`` and nose follows ``heading()``."""
    width, wheel = length * 0.5, length * 0.13
    body_h, cabin_h = length * 0.2, length * 0.17

    def fwd() -> np.ndarray:
        h = heading()
        return np.array([np.cos(h), 0.0, -np.sin(h)])

    def side() -> np.ndarray:
        h = heading()
        return np.array([np.sin(h), 0.0, np.cos(h)])

    up = np.array([0.0, 1.0, 0.0])
    body = Block(lambda: where() + up * (wheel + body_h / 2), (length, body_h, width), color, heading)
    cabin = Block(lambda: where() + up * (wheel + body_h + cabin_h / 2) - fwd() * length * 0.06,
                  (length * 0.5, cabin_h, width * 0.84), "#BFDDF0", heading)
    parts: list[Block] = [body, cabin]
    for a in (-1, 1):
        for b in (-1, 1):
            parts.append(Block(lambda a=a, b=b: where() + fwd() * a * length * 0.3 + side() * b * width * 0.46 + up * wheel,
                               (wheel * 2, wheel * 2, width * 0.18), "#1B2733", heading))
    for part in parts:
        part.keep_in_frame = True
    stage.add_body(*parts)
    return parts


class Circuit:
    """A particle (or a car) on a circle on a stage's ground, driven by its own clock ``t``.

    Plane angle theta runs counterclockwise seen from above; ``R`` is the
    radius in stage units and ``s`` stage units per metre of the model.
    Arrows read the model at ``t``: 'r', 'v', 'a' (centripetal), 'at'
    (tangential), 'atot' (total), with ``kv`` / ``ka`` stage units per m/s
    and per m/s^2, so their lengths are the model's magnitudes."""

    def __init__(self, stage: Stage, model=P, *, centre=(0.0, 0.0, 0.0), R: float = 2.0, height: float = 0.2,
                 phase: float = 0.0, body: str = "ball", color: str = cfg.BALL, radius: float = 0.2,
                 kv: float | None = None, ka: float | None = None, car_length: float = 0.9) -> None:
        self.stage, self.model, self.R, self.height, self.phase = stage, model, float(R), float(height), float(phase)
        self.centre = np.asarray(centre, dtype=float)
        self.t = 0.0
        self.view = CircleView(ORIGIN, 1.0, model, phase=phase)   # the model's maths, reused
        speed0 = self.view.r_m * abs(self.view.omega(0.0))
        accel0 = self.view.r_m * self.view.omega(0.0) ** 2
        self.kv = kv if kv is not None else 0.5 * R / max(speed0, 1e-9)
        self.ka = ka if ka is not None else 0.42 * R / max(accel0, 1e-9)
        if body == "car":
            self.parts = car3d(stage, lambda: self.floor_point(), lambda: self.view.theta(self.t) + np.pi / 2,
                               color, car_length)
            self.ball = self.parts[0]
        else:
            self.ball = Ball(lambda: self.world(), radius, color)
            self.ball.keep_in_frame = True
            self.parts = [self.ball]
            stage.add_body(self.ball)
        self.arrows: dict[str, Vector] = {}

    def floor_point(self, t: float | None = None) -> np.ndarray:
        u = self.view.unit_r(self.t if t is None else t)
        return self.centre + ground(self.R * u[0], self.R * u[1])

    def world(self, t: float | None = None) -> np.ndarray:
        return self.floor_point(t) + np.array([0.0, self.height, 0.0])

    def ground_dir(self, v2) -> np.ndarray:
        return ground_vec(v2)

    def add_arrow(self, kind: str, color: str | None = None, *, width: float = 0.08, tip: float = 0.26,
                  presence: float = 0.0, lift: float = 0.0) -> Vector:
        def start():
            return self.world() + np.array([0.0, lift, 0.0])

        def end():
            t = self.t
            vec = {"r": None,
                   "v": self.view.vel(t) * self.kv,
                   "a": self.view.acc_radial(t) * self.ka,
                   "at": self.view.acc_tangential(t) * self.ka,
                   "atot": (self.view.acc_radial(t) + self.view.acc_tangential(t)) * self.ka}[kind]
            if vec is None:
                return start()
            return start() + ground_vec(vec)

        colors = {"r": cfg.POSITION, "v": cfg.VELOCITY, "a": cfg.ACCEL, "at": cfg.TANGENTIAL, "atot": cfg.WHITE}
        if kind == "r":
            arrow = Vector(lambda: self.centre + np.array([0.0, self.height + lift, 0.0]), start, color or colors[kind],
                           width=width, tip=tip)
        else:
            arrow = Vector(start, end, color or colors[kind], width=width, tip=tip)
        arrow.keep_in_frame = True
        arrow.presence = presence
        self.stage.add_overlay(arrow)
        self.arrows[kind] = arrow
        return arrow

    def run(self, until: float, run_time: float | None = None, **kwargs) -> Param:
        kwargs.setdefault("rate_func", linear)
        kwargs.setdefault("run_time", run_time or max(abs(until - self.t), 0.1))
        return Param(self.stage, lambda: self.t, lambda v: setattr(self, "t", v), until, **kwargs)

    def turns(self, laps: float, run_time: float, **kwargs) -> Param:
        return self.run(self.t + laps * 2 * np.pi / abs(self.view.omega()), run_time, **kwargs)


def run_together(holder: Mobject, circuits: Sequence, seconds: float, run_time: float) -> Param:
    """Advance several circuits by the same physical time on one shared clock."""
    elapsed = Knob(0.0)
    starts = [c.t if hasattr(c, "t") else c.clock.value for c in circuits]

    def put(value: float) -> None:
        elapsed.value = value
        for c, s in zip(circuits, starts):
            if hasattr(c, "t"):
                c.t = s + value
            else:
                c.clock.value = s + value

    return Param(holder, lambda: elapsed.value, put, seconds, run_time=run_time, rate_func=linear)


def chunked_curve(points: np.ndarray, color: str, chunks: int = 16, **kwargs) -> list[Curve]:
    """A long curve split into pieces, so each piece sorts by depth on its own
    (an orbit passes behind a planet and in front of it)."""
    points = np.asarray(points, dtype=float)
    edges = np.linspace(0, len(points) - 1, chunks + 1).astype(int)
    return [Curve(points[a:b + 1], color, **kwargs) for a, b in zip(edges[:-1], edges[1:]) if b > a]


def globe(stage: Stage, centre, radius: float, spin: Knob, color: str = cfg.EARTH, tilt: float = 0.35) -> list:
    """A planet: a polished ball, a thin atmosphere glow, and a turning grid of
    meridians and parallels cut into short pieces that hide behind it."""
    c = np.asarray(centre, dtype=float)
    axis_tilt = mu.rotation_z(tilt)
    core = Ball(c, radius, color, layers=44)
    air = Halo(core, cfg.CYAN, reach=1.12, layers=8, peak=0.12)
    bodies: list = [air, core]

    def on_sphere(lat: float, lon: float, lift: float = 1.006):
        def point():
            a = lon + spin.value
            local = np.array([np.cos(lat) * np.cos(a), np.sin(lat), -np.cos(lat) * np.sin(a)]) * radius * lift
            return c + axis_tilt @ local
        return point

    pieces = 28
    for lon in np.linspace(0, np.pi, 6, endpoint=False):
        for k in range(pieces):
            a0, a1 = -np.pi / 2 + np.pi * k / pieces * 2, -np.pi / 2 + np.pi * (k + 1) / pieces * 2
            for side in (0.0, np.pi):
                bodies.append(Segment(on_sphere(a0, lon + side), on_sphere(a1, lon + side), cfg.CYAN, width=1.6,
                                      opacity=0.32))
    for lat in (-np.pi / 3, -np.pi / 6, 0.0, np.pi / 6, np.pi / 3):
        for k in range(pieces):
            l0, l1 = 2 * np.pi * k / pieces, 2 * np.pi * (k + 1) / pieces
            bodies.append(Segment(on_sphere(lat, l0), on_sphere(lat, l1), cfg.CYAN, width=1.6,
                                  opacity=0.42 if lat == 0 else 0.3))
    stage.add_body(*bodies)
    return bodies


# ----------------------------------------------------------------------------
# Closing card
# ----------------------------------------------------------------------------


def scalar_tile(name: str, latex: str, color: str = cfg.WHITE, width: float = 3.3) -> VGroup:
    """One quantity on a panel: its name above a value set as an equation."""
    title = txt(name, cfg.FONT["tiny"], cfg.MUTED)
    value = eq(latex, cfg.FONT["body"], color)
    body = VGroup(title, value).arrange(DOWN, buff=0.18)
    back = panel(max(width, body.width + 0.5), body.height + 0.5).move_to(body)
    tile = VGroup(back, body)
    tile.title, tile.value = title, value
    return tile


def subscribe_card() -> VGroup:
    """The channel's closing card, in the house style."""
    thank_you = txt("THANK YOU FOR WATCHING", 40, cfg.CYAN)
    subscribe = Text("SUBSCRIBE", font_size=96, color=cfg.GOLD, weight=BOLD)
    subscribe.set_stroke("#351F05", width=3, opacity=0.75, background=True)
    rule = Line(LEFT * 3.4, RIGHT * 3.4, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(txt("Stay curious", 44, cfg.WHITE),
                     txt("Visualized Physics", 36, cfg.CYAN)).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "cd", "np", "P"]
