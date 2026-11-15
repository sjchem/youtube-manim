"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing synthesis reads as a conclusion rather than a new picture:

* a **centre of mass** is always the same glowing checkered target
  (``com_target``), white on the stage and in every diagram;
* **position / lever arm** is teal, **velocity and momentum** gold, **force**
  green, (radial) **acceleration** orange, tangential acceleration blue;
* the **turning world** is cyan (theta, omega, alpha, spin arrows), **torque**
  purple and **angular momentum** rose; **mass and moment of inertia**
  periwinkle; **energy and work** coral;
* rigid bodies live on a turning 3D ``Stage``: solid discs and cylinders are
  ``Drum``s whose caps carry a turning sector pattern, thin rings are copper
  ``Hoop``s with bright stripes, so a spin is always visible;
* a confirmed result is gold in a glowing box; balance and conservation are
  green; a trap or a broken balance is red.

Scene files compose these pieces and choreograph them against the beats in
``narration.py``; nothing in a scene file should invent a second way to draw
one of these ideas, or type a number that ``utils.physics_models`` supplies.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from types import SimpleNamespace

import numpy as np
from manim import *

import config as cfg
from manim_scenes.stage3d import (Ball, Block, Curve, Disc, Dots, Drum, Face, Grid, Halo, Hoop, Param, Rod,
                                  Segment, Solid, Stage, Tag, Vector, _LiveMixin, _polished_parts, prism)
from narration import SCRIPT
from utils import math_utils as mu
from utils import physics_models as pm
from utils import rotation_data as rd
from utils.render_helpers import fit_inside, fit_to_safe_frame, fit_width


# ----------------------------------------------------------------------------
# Scene lifecycle
# ----------------------------------------------------------------------------


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
# Animations squeezed by ``play_in`` to fit a beat are recorded here, so the
# timing audit can name any beat whose motion had to be compressed hard.
SQUEEZED: list[tuple[str, int, float, float]] = []


def cue(scene: Scene, started_at: float, seconds: float) -> None:
    """Hold until a named second inside the chapter, and refuse to run past it."""
    import manim_scenes.common as common

    remaining = seconds - (float(scene.time) - started_at)
    key = getattr(scene, "_project_scene_key", "unknown")
    if remaining < -common.CUE_TOLERANCE:
        raise ValueError(f"Scene {key} cue {seconds}s overrun by {-remaining:.2f}s")
    if remaining > 1e-6:
        narration_wait(scene, remaining)


def beat_time(scene: Scene, index: int) -> float:
    """Start of beat ``index`` (or the closing fade when ``index`` is past the last beat)."""
    key = scene._project_scene_key
    beats = SCRIPT[key]
    if index < len(beats):
        return beats[index][0]
    return cfg.SCENE_DURATIONS[key] - cfg.TIMING["transition"]


def beat(scene: Scene, started_at: float, index: int) -> None:
    """Hold until narration beat ``index`` of this chapter begins."""
    cue(scene, started_at, beat_time(scene, index))


def time_left(scene: Scene, started_at: float, upto: int) -> float:
    """Seconds left before beat ``upto`` begins."""
    return beat_time(scene, upto) - (float(scene.time) - started_at)


def play_in(scene: Scene, started_at: float, upto: int, *animations, run_time: float = 1.0, **kwargs) -> None:
    """Play, but finish before beat ``upto``: the run time shrinks to fit if it must."""
    left = time_left(scene, started_at, upto) - 0.04
    fps = float(scene.camera.frame_rate)
    fitted = max(min(run_time, left), 2.0 / fps)
    if fitted < run_time * 0.7 and run_time - fitted > 0.3:
        SQUEEZED.append((getattr(scene, "_project_scene_key", "?"), upto, run_time, fitted))
    scene.play(*animations, run_time=fitted, **kwargs)


def finish(scene: Scene, started_at: float, stage: Stage | None = None, drift: float = 0.22,
           fill: Callable[[float], Sequence[Animation]] | None = None) -> None:
    """Close the scene without a frozen frame: a slow camera drift (``stage``)
    and/or ``fill(seconds)`` animations run over the last seconds, then
    everything fades on the configured frame boundary."""
    key = scene._project_scene_key
    end = cfg.SCENE_DURATIONS[key] - cfg.TIMING["transition"]
    left = end - (float(scene.time) - started_at) - 0.05
    anims = list(fill(left)) if fill is not None and left > 0.4 else []
    if stage is not None and left > 0.4:
        anims += stage.turn(yaw=stage.yaw + float(np.clip(drift * left / 4, -0.24, 0.24)), rate_func=smooth)
    if anims:
        scene.play(*anims, run_time=left)
    end_scene(scene, started_at, cfg.SCENE_DURATIONS[key])


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
    for member in stage.get_family():
        member.clear_updaters()
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
    """Colour parts of a multi-part MathTex by index."""
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


def heading(title: str, color: str = cfg.GOLD, size: int = 50) -> VGroup:
    """Gold scene title with shadow and glow, held three seconds then faded."""
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
    """Old fully out before the new one comes in, as one animation."""
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
    group = VGroup(glow_frame(mob, color, buff=buff), mob)
    group.frame, group.body = group[0], mob
    return group


def title_card(big: str, small: str, color: str = cfg.GOLD) -> VGroup:
    """The film's title: a big warm line and a smaller cyan one, with an outline,
    an offset shadow and a soft glow."""
    line_one = Text(big, font=cfg.TITLE_FONT, weight=BOLD, font_size=96, color=color)
    line_two = Text(small, font=cfg.TITLE_FONT, weight=BOLD, font_size=50, color=cfg.CYAN)
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


def result_label(name: str, color: str = cfg.RESULT, size: int | None = None) -> VGroup:
    """A revealed result: coloured type with a soft glow behind it."""
    label = txt(name, size or cfg.FONT["section"], color)
    glow = label.copy().set_stroke(color, width=14, opacity=0.16).set_fill(opacity=0)
    decorative(glow)
    group = VGroup(glow, label)
    group.label = label
    return group


def stacked(*lines: Mobject, buff: float = 0.3, aligned=LEFT) -> VGroup:
    return VGroup(*lines).arrange(DOWN, buff=buff, aligned_edge=aligned)


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
    """A flat sphere with the same lighting as the projected 3D balls."""
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


def cancel(mob: Mobject, color: str = cfg.RED, width: float = 6) -> Line:
    """A diagonal slash through a term that cancels."""
    return Line(mob.get_corner(DL) + DL * 0.04, mob.get_corner(UR) + UR * 0.04, stroke_color=color, stroke_width=width)


def dashed_path(a, b, color: str = cfg.MUTED, width: float = 2.4, opacity: float = 0.55, dash: float = 0.13,
                count: int | None = None) -> VMobject:
    """A dashed segment. Pass a fixed ``count`` for a live (updater-rebuilt) line."""
    line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    count = count or max(int(float(np.linalg.norm(b - a)) / (2 * dash)), 1)
    for k in range(count):
        line.start_new_path(a + (b - a) * k / count)
        line.add_line_to(a + (b - a) * (k + 0.55) / count)
    return line


def countdown(scene: Scene, at, seconds: int = 3, color: str = cfg.GOLD) -> None:
    """A shrinking ring with 3, 2, 1 — the viewer's thinking time."""
    for k in range(seconds, 0, -1):
        digit = txt(str(k), 80, color).move_to(at)
        ring = Circle(radius=0.62, stroke_color=color, stroke_width=7, fill_opacity=0).move_to(at)
        scene.add(digit, ring)
        scene.play(Uncreate(ring), digit.animate.set_opacity(0.15), run_time=1.0, rate_func=linear)
        scene.remove(digit, ring)


def live(mob: Mobject, build: Callable[[], Mobject]) -> Mobject:
    """Rebuild ``mob`` from ``build()`` every frame, primed once so it can fade in at once."""
    mob.add_updater(lambda m: m.become(build()))
    mob.become(build())
    return mob


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
        if live:
            self.add_updater(lambda m: m.refresh() if m._live else None)

    def tail(self) -> np.ndarray:
        return np.asarray(self.tail_src() if callable(self.tail_src) else self.tail_src, dtype=float)

    def tip(self) -> np.ndarray:
        return np.asarray(self.tip_src() if callable(self.tip_src) else self.tip_src, dtype=float)

    def head(self) -> np.ndarray:
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

    def grow_in(self, **kwargs) -> Param:
        self.grow = 0.0
        self.refresh()
        return Param(self, lambda: self.grow, lambda v: setattr(self, "grow", v), 1.0, **kwargs)

    def fade_to(self, value: float, **kwargs) -> Param:
        return Param(self, lambda: self.alpha, lambda v: setattr(self, "alpha", v), value, **kwargs)


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



def readout(label: str, value: Callable[[], float], decimals: int, unit: str, color: str = cfg.WHITE,
            size: int = 44, label_color: str | None = None) -> VGroup:
    """A live line such as 'V = 2.00 L': an equation label, a DecimalNumber, a unit."""
    head = eq(label, int(size / MATH_SCALE * 1.05), label_color or color)
    number = DecimalNumber(value(), num_decimal_places=decimals, font_size=size * 1.08, color=color)
    number.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
    unit_mob = txt(unit, int(size * 0.72), cfg.MUTED)
    row = VGroup(head, number, unit_mob)

    def follow(m):
        number.set_value(value())
        number.next_to(head, RIGHT, buff=0.2)
        unit_mob.next_to(number, RIGHT, buff=0.2, aligned_edge=DOWN)

    row.arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
    row.add_updater(follow)
    row.number = number
    return row

# ----------------------------------------------------------------------------
# Plots
# ----------------------------------------------------------------------------


def plot_axes(x_range, y_range, *, x_length: float, y_length: float, at=ORIGIN, x_label: str = "x",
              y_label: str = "y", x_color: str = cfg.MUTED, y_color: str = cfg.MUTED, x_ticks: Sequence = (),
              y_ticks: Sequence = (), tick_size: int = 28, label_size: int | None = None) -> Axes:
    """Axes in the film's style: thick muted lines, big coloured symbols, few ticks.

    ``axes.c2p(x, y)`` maps data to the screen; ``axes.labels`` holds the axis
    symbols and ``axes.ticks`` the tick numbers (decorative: read with the curve)."""
    axes = Axes(x_range=list(x_range), y_range=list(y_range), x_length=x_length, y_length=y_length,
                axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3.2, "include_ticks": False,
                             "tip_width": 0.22, "tip_height": 0.22},
                tips=True)
    axes.move_to(at)
    # Labels sit beyond the arrow tips, so they never meet a tick number.
    xl = eq(x_label, label_size or cfg.FONT["label"], x_color).next_to(axes.x_axis.get_end(), RIGHT, buff=0.14)
    yl = eq(y_label, label_size or cfg.FONT["label"], y_color).next_to(axes.y_axis.get_end(), UP, buff=0.12)
    axes.labels = VGroup(xl, yl)
    ticks = VGroup()
    for value in x_ticks:
        mark = Line(axes.c2p(value, y_range[0]) + DOWN * 0.08, axes.c2p(value, y_range[0]) + UP * 0.08,
                    stroke_color=cfg.MUTED, stroke_width=2.5)
        ticks.add(mark, txt(f"{value:g}", tick_size, cfg.MUTED).next_to(mark, DOWN, buff=0.1))
    for value in y_ticks:
        mark = Line(axes.c2p(x_range[0], value) + LEFT * 0.08, axes.c2p(x_range[0], value) + RIGHT * 0.08,
                    stroke_color=cfg.MUTED, stroke_width=2.5)
        ticks.add(mark, txt(f"{value:g}", tick_size, cfg.MUTED).next_to(mark, LEFT, buff=0.1))
    decorative(ticks)
    axes.ticks = ticks
    axes.add(axes.labels, ticks)
    return axes


def curve_on(axes: Axes, f: Callable[[float], float], x_from: float, x_to: float, color: str, width: float = 6,
             samples: int = 120, glow: bool = True) -> VGroup:
    """A glowing curve y = f(x) on axes, as plain VMobjects (no ParametricFunction quirks)."""
    xs = np.linspace(x_from, x_to, samples)
    pts = [axes.c2p(x, f(x)) for x in xs]
    core = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0).set_points_smoothly(pts)
    group = VGroup()
    if glow:
        group.add(core.copy().set_stroke(color, width=width * 3.2, opacity=0.14))
    group.add(core)
    group.core = core
    return group


def polyline(points: Sequence, color: str, width: float = 4, opacity: float = 1.0) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity,
                    fill_opacity=0).set_points_as_corners([np.asarray(p, dtype=float) for p in points])


def bar_chart(values: Sequence[float], names: Sequence[str], colors: Sequence[str], *, at=ORIGIN, width: float = 7.0,
              height: float = 3.2, top: float | None = None, value_labels: Sequence[str] | None = None,
              bar_width: float = 0.8, name_size: int = 34) -> VGroup:
    """Vertical bars on a baseline, names below, optional value labels above."""
    top = top or max(values)
    n = len(values)
    xs = np.linspace(-width / 2 + width / (2 * n), width / 2 - width / (2 * n), n)
    base = Line(LEFT * width / 2, RIGHT * width / 2, stroke_color=cfg.MUTED, stroke_width=3)
    bars, labels, tops = VGroup(), VGroup(), VGroup()
    for x, v, name, color in zip(xs, values, names, colors):
        h = max(height * v / top, 0.04)
        bar = Rectangle(width=bar_width, height=h, stroke_color=color, stroke_width=2, fill_color=color,
                        fill_opacity=0.85).move_to([x, h / 2, 0])
        bars.add(bar)
        labels.add(txt(name, name_size, cfg.WHITE).next_to([x, 0, 0], DOWN, buff=0.22))
    if value_labels:
        for bar, label, color in zip(bars, value_labels, colors):
            tops.add(txt(label, cfg.FONT["tiny"], color).next_to(bar, UP, buff=0.14))
    chart = VGroup(base, bars, labels, tops).move_to(at)
    chart.base, chart.bars, chart.names, chart.tops = base, bars, labels, tops
    return chart


def bar_meter(value: Callable[[], float], top: float, *, at=ORIGIN, height: float = 3.0, width: float = 0.7,
              color: str = cfg.ENERGY, label: str | None = None, label_color: str | None = None) -> VGroup:
    """A live vertical bar filling to ``value() / top`` of its height, with an outline."""
    frame = RoundedRectangle(width=width + 0.16, height=height + 0.16, corner_radius=0.1, stroke_color=cfg.MUTED,
                             stroke_width=2.5, stroke_opacity=0.7, fill_color=cfg.PANEL, fill_opacity=0.85).move_to(at)
    fill = Rectangle(width=width, height=0.01, stroke_width=0, fill_color=color, fill_opacity=0.95)
    glow = Rectangle(width=width + 0.2, height=0.01, stroke_width=0, fill_color=color, fill_opacity=0.18)
    bottom = frame.get_bottom()[1] + 0.08

    def fit(_m=None):
        h = max(height * float(np.clip(value() / top, 0, 1)), 0.01)
        for rect in (fill, glow):
            rect.stretch_to_fit_height(h)
            rect.move_to([frame.get_center()[0], bottom + h / 2, 0])

    fit()
    fill.add_updater(fit)
    group = VGroup(frame, glow, fill)
    if label:
        tag = eq(label, cfg.FONT["label"], label_color or color).next_to(frame, DOWN, buff=0.18)
        group.add(tag)
        group.tag = tag
    group.frame, group.fill = frame, fill
    return group


# ----------------------------------------------------------------------------
# The centre-of-mass target
# ----------------------------------------------------------------------------


def com_target(radius: float = 0.2, glow: bool = True) -> VGroup:
    """The engineering centre-of-mass symbol: a disc in four checkered quadrants,
    ringed and haloed, so the eye can find it in any crowd of moving parts."""
    parts = VGroup()
    if glow:
        parts.add(halo(radius * 3.0, cfg.COM_GLOW, layers=6, peak_opacity=0.22))
    for k in range(4):
        parts.add(Sector(radius=radius, start_angle=k * PI / 2, angle=PI / 2, stroke_width=0,
                         fill_color=cfg.WHITE if k % 2 == 0 else "#10283F", fill_opacity=1))
    parts.add(Circle(radius=radius, stroke_color=cfg.WHITE, stroke_width=3, fill_opacity=0))
    decorative(parts)
    return parts


def com_tag(point, radius: float = 0.2) -> Tag:
    """A centre-of-mass target pinned to a (live) 3D point on a stage."""
    return Tag(com_target(radius), point)


# ----------------------------------------------------------------------------
# Rotation arrows
# ----------------------------------------------------------------------------


def turn_arrow(centre, radius: float, start: float, sweep: float, color: str = cfg.ANGLE, width: float = 6,
               tip: float = 0.3) -> VGroup:
    """A curved arrow around ``centre`` (2D): counterclockwise for positive sweep."""
    centre = np.asarray(centre, dtype=float)
    arc = Arc(radius=radius, start_angle=start, angle=sweep * 0.86, arc_center=centre, stroke_color=color,
              stroke_width=width)
    end_angle = start + sweep
    q = centre + radius * np.array([np.cos(end_angle), np.sin(end_angle), 0.0])
    back = start + sweep * 0.8
    p = centre + radius * np.array([np.cos(back), np.sin(back), 0.0])
    d = mu.unit(q - p)
    side = np.array([-d[1], d[0], 0.0])
    head = Polygon(q, q - d * tip + side * tip * 0.55, q - d * tip - side * tip * 0.55, stroke_width=0,
                   fill_color=color, fill_opacity=1)
    glow = arc.copy().set_stroke(color, width=width * 3, opacity=0.15)
    return VGroup(glow, arc, head)


def turn_arrow_3d(stage: Stage, centre, axis, radius: float, start: float, sweep: float, color: str = cfg.ANGLE,
                  width: float = 5.0, samples: int = 40) -> SimpleNamespace:
    """A curved arrow around ``axis`` through ``centre`` on a stage (right-handed for positive sweep)."""
    F = mu.frame_from_axis(axis)

    def point(a: float) -> np.ndarray:
        c = np.asarray(centre() if callable(centre) else centre, dtype=float)
        return c + F @ np.array([radius * np.cos(a), radius * np.sin(a), 0.0])

    angles = np.linspace(start, start + sweep * 0.9, samples)
    arc = Curve(lambda: np.array([point(a) for a in angles]), color, width=width)
    head = Vector(lambda: point(start + sweep * 0.86), lambda: point(start + sweep), color, width=0.02, tip=0.26)
    stage.add_body(arc)
    stage.add_overlay(head)
    return SimpleNamespace(arc=arc, head=head, parts=[arc, head])


def drive(holder: Mobject, knob: "Knob", rate) -> Callable:
    """A motor: advance ``knob`` by ``rate * dt`` every frame (``rate`` may be a
    number, a function or another Knob, so a spin can itself be tweened).
    Returns the updater so it can be removed with ``holder.remove_updater``."""
    def step(mob, dt):
        if getattr(mob, "_live", True):
            knob.value += float(rate() if callable(rate) else rate) * dt
    holder.add_updater(step)
    return step


def stage_swap(stage: Stage, old, new) -> list[Param]:
    """Replace a live stage label without temporarily superimposing the two."""
    return [stage.fade(old, 0.0, rate_func=lambda a: smooth(min(a / 0.45, 1.0))),
            stage.fade(new, 1.0, rate_func=lambda a: smooth(max((a - 0.55) / 0.45, 0.0)))]


def stage_fade(stage: Stage, items, value: float, **kwargs) -> list[Param]:
    return [stage.fade(item, value, **kwargs) for item in items]


def hidden(*items):
    """Mark stage bodies / overlays invisible before they are faded in."""
    for item in items:
        item.presence = 0.0
    return items[0] if len(items) == 1 else items


# ----------------------------------------------------------------------------
# Props on a stage
# ----------------------------------------------------------------------------


def floor(stage: Stage, y: float = 0.0, reach: float = 6.0, step: float = 0.5, color: str = cfg.GRID,
          opacity: float = 0.3, centre=(0.0, 0.0)) -> Grid:
    grid = Grid((centre[0], y, centre[1]), (1, 0, 0), (0, 0, 1), (-reach, reach), (-reach, reach), step=step,
                major=4, color=color, opacity=opacity)
    stage.add_body(grid)
    return grid


def axis_line(stage: Stage, a, b, color: str = cfg.MUTED, opacity: float = 0.75, width: float = 3.0) -> Segment:
    line = Segment(a, b, color, width=width, opacity=opacity, dashed=True)
    stage.add_body(line)
    return line


def wheel(stage: Stage, centre, radius: float, spin, *, half_length: float = 0.12, axis=(0.0, 0.0, 1.0),
          color: str = cfg.DISC_BODY, stripe: str = cfg.DISC_STRIPE, sectors: int = 6, hub: bool = True,
          pose=None) -> SimpleNamespace:
    """A solid disc (or wheel) on a stage, with an optional polished hub."""
    drum = Drum(centre, radius, half_length, color, axis=axis, spin=spin, stripe=stripe, sectors=sectors, pose=pose)
    parts = [drum]
    if hub:
        cap = Ball(lambda: drum.axes()[:, 2] * (half_length + 0.02) + np.asarray(centre() if callable(centre) else centre),
                   min(0.12, radius * 0.18), cfg.STEEL, layers=12)
        cap.bias = 0.5
        parts.append(cap)
    stage.add_body(*parts)
    return SimpleNamespace(drum=drum, parts=parts)


def rim_marker(stage: Stage, drum: Drum, angle: float, color: str = cfg.GOLD, fraction: float = 1.0,
               radius: float = 0.09) -> Ball:
    """A bright bead fixed to a turning drum (on its front cap, at ``fraction`` of the radius)."""
    def where():
        F = drum.axes()
        eye_side = 1.0 if (stage.rotation() @ F[:, 2])[2] > 0 else -1.0
        return drum.rim_point(angle, end=eye_side * 1.05, fraction=fraction)

    bead = Ball(where, radius, color, layers=14)
    bead.bias = 50.0          # sits on the visible cap: always in front of its own drum
    stage.add_body(bead)
    return bead


class SkaterModel:
    """A stylised skater turning about the vertical axis on a stage.

    The torso is a short ``Drum``, the head a ``Ball``; each arm is a ``Rod``
    from the shoulder to a hand ``Ball`` at horizontal distance ``reach()``
    (in model metres, mapped by ``scale``) from the spin axis. ``angle()`` is
    the current turn. Moment of inertia and spin come from ``physics_models``."""

    def __init__(self, stage: Stage, base, angle: Callable[[], float], reach: Callable[[], float],
                 scale: float = 1.6) -> None:
        self.stage, self.base, self.angle, self.reach, self.scale = stage, np.asarray(base, dtype=float), angle, reach, scale
        b = self.base
        up = np.array([0.0, 1.0, 0.0])
        R = lambda: mu.rotation_y(-angle())  # noqa: E731  (counterclockwise seen from above)
        self.R = R
        self.legs = Drum(b + up * 0.75, 0.16, 0.75, cfg.SUIT, axis=(0, 1, 0), spin=lambda: -angle(), sectors=2,
                         stripe=mu.mix(cfg.SUIT, cfg.WHITE, 0.2))
        self.torso = Drum(b + up * 1.95, 0.3, 0.5, cfg.SUIT, axis=(0, 1, 0), spin=lambda: -angle(), sectors=2,
                          stripe=mu.mix(cfg.SUIT, cfg.WHITE, 0.35))
        self.head = Ball(b + up * 2.75, 0.24, cfg.SKIN, layers=18)
        shoulder_y = 2.32
        self.shoulders, self.hands, self.arms = [], [], []
        for side in (1.0, -1.0):
            sh = Ball(lambda s=side: b + up * shoulder_y + R() @ np.array([s * 0.3, 0.0, 0.0]), 0.1, cfg.SUIT, layers=10)
            hand = Ball(lambda s=side: b + up * (shoulder_y - 0.05) + R() @ np.array([s * self.reach() * scale, 0.0, 0.0]),
                        0.14, cfg.SKIN, layers=14)
            arm = Rod(sh, hand, width=16, dark=mu.shade(cfg.SUIT, 0.5), light=mu.mix(cfg.SUIT, cfg.WHITE, 0.4))
            self.shoulders.append(sh)
            self.hands.append(hand)
            self.arms.append(arm)
        self.blade = Block(b + up * 0.02, (0.9, 0.04, 0.12), cfg.STEEL, heading=lambda: -angle())
        self.parts = [self.blade, self.legs, self.torso, *self.shoulders, *self.arms, *self.hands, self.head]
        stage.add_body(*self.parts)

    def hand_point(self, side: int = 0) -> np.ndarray:
        return self.hands[side].where()


# ----------------------------------------------------------------------------
# Numbers: always from the model, formatted the way they are spoken
# ----------------------------------------------------------------------------


def fx(value: float, decimals: int = 0) -> str:
    """On-screen number with exactly the digits the narrator says."""
    return rd.fixed(value, decimals)


def ftex(f) -> str:
    """LaTeX coefficient for a Fraction (empty for 1)."""
    return rd.frac_tex(f)


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
                     txt("Keep following the physics and mathematics.", 36, cfg.CYAN)).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.set_stroke("#06131B", width=4, opacity=0.9, background=True)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "rd", "np", "SimpleNamespace"]
