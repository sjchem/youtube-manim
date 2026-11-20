"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing synthesis reads as a conclusion rather than a new picture:

* a **gas** is one ``GasBox``: a glass chamber on a turning 3D ``Stage``
  holding an ``IdealGas`` (or a ``HardSphereGas``) from
  ``utils.physics_models``. Molecules are cyan; the one we follow is gold;
  every wall hit throws an orange spark (momentum handed to the wall);
* a **liquid with its vapour** is a ``TwoPhaseBox``: the same chamber with a
  deep-blue pool whose jittering molecules sit below a translucent surface;
  vapour molecules bounce off the pool, condense into it (blue flash) or
  evaporate from it (gold flash);
* **speeds** are drawn from slow (blue) to fast (orange); Maxwell-Boltzmann
  curves are gold; histograms cyan;
* **pressure** is teal, **volume** blue, **temperature** coral, **amount** rose;
* **attraction** (the van der Waals ``a``) is green and **size / repulsion**
  (``b``) red; a hard sphere's forbidden zone is a red ``glass_sphere``;
* **limits and extremes** (the critical point, supercritical fluid, idealised
  assumptions) are purple; a confirmed result is gold in a glowing box.

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
from manim_scenes.stage3d import (Ball, Block, Body, Chamber, Curve, Disc, Dots, Face, Flashes, GasCloud, Grid, Halo,
                                  Param, Rod, Segment, SphereHalf, Stage, Tag, Vector, _LiveMixin, _polished_parts)
from narration import SCRIPT, TITLES
from utils import spoken_numbers as gd
from utils import math_utils as mu
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
        anims += stage.turn(yaw=stage.yaw + drift * min(left / 4, 1.0), rate_func=smooth)
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


# ----------------------------------------------------------------------------
# Instruments: gauges, thermometers, readouts (they read live functions)
# ----------------------------------------------------------------------------


class Gauge(VGroup):
    """A round pressure gauge reading ``value()`` (bar), with a needle and a readout."""

    def __init__(self, value: Callable[[], float], at=ORIGIN, *, top: float = 3.0, radius: float = 1.1,
                 color: str = cfg.PRESSURE, symbol: str = "P", unit: str = "bar", decimals: int = 2,
                 step: float = 0.5, label_every: float = 1.0) -> None:
        super().__init__()
        self.value_fn, self.top, self.r = value, float(top), radius
        face = Circle(radius=radius, stroke_color=color, stroke_width=5, fill_color=cfg.PANEL, fill_opacity=0.95)
        rim = Circle(radius=radius * 1.06, stroke_color=color, stroke_width=12, stroke_opacity=0.14, fill_opacity=0)
        arc = Arc(radius=radius * 0.84, start_angle=-40 * DEGREES, angle=260 * DEGREES, stroke_color=color,
                  stroke_width=5, stroke_opacity=0.7)
        ticks = VGroup()
        numbers = VGroup()
        k = 0.0
        while k <= self.top + 1e-9:
            a = self._angle(k)
            major = abs(k / label_every - round(k / label_every)) < 1e-6
            inner = radius * (0.64 if major else 0.72)
            ticks.add(Line([np.cos(a) * inner, np.sin(a) * inner, 0], [np.cos(a) * radius * 0.82, np.sin(a) * radius * 0.82, 0],
                           stroke_color=cfg.WHITE, stroke_width=3 if major else 1.8))
            if major:
                numbers.add(txt(f"{k:g}", 24, cfg.MUTED).move_to([np.cos(a) * radius * 0.48, np.sin(a) * radius * 0.48, 0]))
            k += step
        decorative(numbers)   # dial numbers are part of the drawing, read with the needle
        self.needle = VMobject(stroke_width=0, fill_color=cfg.ORANGE, fill_opacity=1)
        hub = Circle(radius=0.08, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=1)
        self.readout = DecimalNumber(value(), num_decimal_places=decimals, font_size=46, color=cfg.WHITE)
        self.readout.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
        self.unit = txt(unit, 30, cfg.MUTED)
        self.symbol = eq(symbol, cfg.FONT["label"], color)
        self.face = face
        self.add(rim, face, arc, ticks, numbers, self.needle, hub, self.readout, self.unit, self.symbol)
        self.move_to(at)
        self.needle.add_updater(lambda m: self._draw())
        self._draw()

    def _angle(self, v: float) -> float:
        return (220 - 260 * np.clip(v, 0, self.top) / self.top) * DEGREES

    def _draw(self) -> None:
        c = self.face.get_center()
        value = float(self.value_fn())
        a = self._angle(value)
        d = np.array([np.cos(a), np.sin(a), 0.0])
        side = np.array([-d[1], d[0], 0.0])
        self.needle.set_points_as_corners([c + side * 0.055, c + d * self.r * 0.78, c - side * 0.055, c + side * 0.055])
        self.readout.set_value(value)
        self.readout.next_to(self.face, DOWN, buff=0.18).shift(LEFT * 0.3)
        self.unit.next_to(self.readout, RIGHT, buff=0.2, aligned_edge=DOWN)
        self.symbol.next_to(self.face, UP, buff=0.14)


class Thermo(VGroup):
    """A glowing thermometer whose column and kelvin readout follow ``kelvin()``."""

    def __init__(self, kelvin: Callable[[], float], at=ORIGIN, *, low: float = 200.0, high: float = 700.0,
                 height: float = 3.0, color: str = cfg.TEMPERATURE, unit: str = "K") -> None:
        super().__init__()
        self.fn, self.low, self.high = kelvin, float(low), float(high)
        tube = RoundedRectangle(width=0.34, height=height, corner_radius=0.17, stroke_color=cfg.MUTED, stroke_width=3,
                                fill_color=cfg.PANEL, fill_opacity=0.9)
        bulb = Circle(radius=0.3, stroke_color=cfg.MUTED, stroke_width=3, fill_color=color, fill_opacity=1)
        bulb.next_to(tube, DOWN, buff=-0.12)
        glow = halo(0.75, color, layers=5, peak_opacity=0.2).move_to(bulb)
        self.tube, self.bulb = tube, bulb
        self.column = Rectangle(width=0.17, height=0.1, stroke_width=0, fill_color=color, fill_opacity=1)
        self.readout = DecimalNumber(kelvin(), num_decimal_places=0, font_size=40, color=cfg.WHITE)
        self.readout.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
        self.unit = txt(unit, 30, cfg.MUTED)
        self.symbol = eq("T", cfg.FONT["label"], color)
        self.add(glow, tube, bulb, self.column, self.readout, self.unit, self.symbol)
        self.move_to(at)
        self.column.add_updater(lambda m: self._fit())
        self._fit()

    def _fit(self) -> None:
        value = float(self.fn())
        bottom = self.tube.get_bottom()[1] + 0.05
        frac = np.clip((value - self.low) / (self.high - self.low), 0.02, 1.0)
        top = bottom + frac * (self.tube.height - 0.15)
        self.column.stretch_to_fit_height(max(top - bottom, 0.02))
        self.column.move_to([self.tube.get_center()[0], (top + bottom) / 2, 0])
        self.readout.set_value(value)
        self.readout.next_to(self.bulb, DOWN, buff=0.16)
        self.unit.next_to(self.readout, RIGHT, buff=0.2, aligned_edge=DOWN)
        self.symbol.next_to(self.tube, UP, buff=0.14)


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


# ----------------------------------------------------------------------------
# The gas in a box: a glass chamber on a stage, with lids, pistons and heaters
# ----------------------------------------------------------------------------


class GlassWall(Face):
    """A wall of the chamber. It draws behind the gas when it faces away from the
    viewer and in front when it faces toward the viewer, at any camera angle."""

    def __init__(self, corners, normal, color: str = cfg.GLASS, opacity: float = 0.07,
                 edge_opacity: float = 0.6) -> None:
        super().__init__(corners, color, opacity=opacity, edge_opacity=edge_opacity)
        self.normal = np.asarray(normal, dtype=float)
        self.poly.set_stroke(width=2.8)

    def place(self, stage, R, visibility):
        super().place(stage, R, visibility)
        self.depth_key = 1e3 if float((R @ self.normal)[2]) > 0 else -1e3


class GasBox:
    """A box of ideal gas: a stage, a chamber, glass walls, the gas and its fittings.

    ``lid``: "glass" (a closed glass box), "piston" (a steel piston with a rod),
    "weight" (a free piston loaded with a weight: constant pressure) or
    "rigid" (a bolted steel lid: constant volume). ``heater`` adds a hot plate
    whose glow follows ``self.heater_glow``; ``inlet`` adds a pipe on the left.

    ``pressure()`` is the model's ideal-gas pressure in bar, relative to the
    reference state the box starts in (``p_ref`` bar): it follows the active
    molecule count, the temperature (``heat`` squared) and the volume.

    ``model`` replaces the default ``IdealGas`` with any gas of the same
    interface (``pm.HardSphereGas`` for molecules with real size; give it the
    chamber's extent ``(2 half_x, height, 2 half_z)``). The gas lives in the
    chamber returned by ``_gas_region()`` (the whole vessel here; the space
    above the liquid in a ``TwoPhaseBox``)."""

    def __init__(self, at=(0.0, -0.4, 0.0), *, count: int = 90, seed: int = cfg.SEED, half_x: float = 1.5,
                 half_z: float = 1.1, height: float = 2.6, floor: float = -1.3, lid: str = "glass",
                 heater: bool = False, inlet: bool = False, species=None, masses=(1.0, 1.0),
                 colors=(cfg.MOLECULE, cfg.ROSE), radius: float = 0.075, speed: float = 1.5,
                 follow: int | None = None, trail: float = 0.0, active: int | None = None, zoom: float = 1.0,
                 yaw: float = -0.55, pitch: float = 0.34, sway: float = 0.04, p_ref: float = 1.0,
                 t_ref: float = pm.ROOM_T, spark_axes=(0, 1, 2), spark_sides=(0, 1), spark_size: float = 1.0,
                 floor_grid: bool = True, model=None) -> None:
        self.stage = Stage(at, zoom=zoom, yaw=yaw, pitch=pitch, sway=sway)
        self.chamber = Chamber((0.0, 0.0, 0.0), half_x=half_x, half_z=half_z, floor=floor, height=height)
        self.gas = model if model is not None else pm.IdealGas(count, seed, species=species, masses=masses)
        if active is not None:
            self.gas.active[:] = False
            self.gas.active[:active] = True
        self.n_ref = int(self.gas.active.sum())
        self.p_ref, self.t_ref = float(p_ref), float(t_ref)
        self.heater_glow = 0.0
        ch = self.chamber
        c = ch.corner
        walls = [
            GlassWall(lambda: [c(-1, 0, -1), c(1, 0, -1), c(1, 1, -1), c(-1, 1, -1)], (0, 0, -1)),
            GlassWall(lambda: [c(-1, 0, 1), c(1, 0, 1), c(1, 1, 1), c(-1, 1, 1)], (0, 0, 1)),
            GlassWall(lambda: [c(-1, 0, -1), c(-1, 0, 1), c(-1, 1, 1), c(-1, 1, -1)], (-1, 0, 0)),
            GlassWall(lambda: [c(1, 0, -1), c(1, 0, 1), c(1, 1, 1), c(1, 1, -1)], (1, 0, 0)),
            GlassWall(lambda: [c(-1, 0, -1), c(1, 0, -1), c(1, 0, 1), c(-1, 0, 1)], (0, -1, 0), opacity=0.12),
        ]
        if lid == "glass":
            walls.append(GlassWall(lambda: [c(-1, 1, -1), c(1, 1, -1), c(1, 1, 1), c(-1, 1, 1)], (0, 1, 0)))
        for wall in walls:
            wall.keep_in_frame = True
        self.walls = walls
        if floor_grid:
            reach = max(half_x, half_z) + 1.4
            self.floor_grid = Grid((0, ch.floor - (0.32 if heater else 0.02), 0), (1, 0, 0), (0, 0, 1), (-reach, reach),
                                   (-reach, reach), step=0.4, major=0, color=cfg.GRID, opacity=0.22)
            self.shadow = Disc(np.array([ch.cx, ch.floor - 0.01, ch.cz]), 1.1 * max(half_x, half_z), "#000000",
                               normal=(0, 1, 0), opacity=0.35, soft=True, bias=-9e3)
            self.stage.add_body(self.floor_grid, self.shadow)
        self.stage.add_body(*walls)
        self.parts: list = []
        self.piston = self.weight = self.rod = self.knob = None
        thick = 0.16
        if lid in {"piston", "weight", "rigid"}:
            color = "#566B7D" if lid == "rigid" else cfg.STEEL
            self.piston = Block(lambda: np.array([ch.cx, ch.top() + thick / 2, ch.cz]),
                                (2 * ch.half_x + (0.12 if lid == "rigid" else -0.02), thick,
                                 2 * ch.half_z + (0.12 if lid == "rigid" else -0.02)), color)
            self.parts.append(self.piston)
        if lid == "piston":
            self.knob = Ball(lambda: np.array([ch.cx, ch.top() + thick + 1.1, ch.cz]), 0.14, cfg.STEEL, layers=12)
            base = Ball(lambda: np.array([ch.cx, ch.top() + thick, ch.cz]), 0.06, cfg.STEEL, layers=8)
            self.rod = Rod(base, self.knob, width=14, dark="#33475A", light="#C9D7E2")
            self.parts += [base, self.rod, self.knob]
        if lid == "weight":
            wh = 0.42
            self.weight = Block(lambda: np.array([ch.cx, ch.top() + thick + wh / 2, ch.cz]),
                                (1.1 * ch.half_x, wh, 1.1 * ch.half_z), "#B98B3E")
            self.parts.append(self.weight)
        if lid == "rigid":
            for sx in (-1, 1):
                for sz in (-1, 1):
                    self.parts.append(Ball(lambda sx=sx, sz=sz: np.array([ch.cx + sx * (ch.half_x - 0.12),
                                                                          ch.top() + thick + 0.03,
                                                                          ch.cz + sz * (ch.half_z - 0.12)]),
                                           0.07, "#C9D7E2", layers=10))
        if heater:
            plate = Block(np.array([ch.cx, ch.floor - 0.12, ch.cz]), (2 * ch.half_x + 0.3, 0.18, 2 * ch.half_z + 0.3),
                          "#3A2A2A")
            self.glow = Disc(np.array([ch.cx, ch.floor - 0.22, ch.cz]), 1.25 * max(ch.half_x, ch.half_z),
                             cfg.HOT_COLOR, normal=(0, 1, 0), opacity=0.5, soft=True, bias=-50)
            self.glow.presence = 0.0
            self.coil = Curve(np.array([[ch.cx - ch.half_x + 0.25 + k * (2 * ch.half_x - 0.5) / 12,
                                         ch.floor - 0.02,
                                         ch.cz + (0.6 if k % 2 else -0.6) * ch.half_z] for k in range(13)]),
                              cfg.HOT_COLOR, width=4)
            self.coil.presence = 0.0
            self.parts += [plate, self.glow, self.coil]
        if inlet:
            y = ch.floor + 0.55 * ch.height
            self.pipe_in = np.array([ch.cx - ch.half_x, y, ch.cz])
            pipe = Curve(np.array([self.pipe_in, self.pipe_in + np.array([-1.0, 0.0, 0.0]),
                                   self.pipe_in + np.array([-1.0, 1.0, 0.0])]), cfg.STEEL, width=11, glow=False)
            valve = Ball(self.pipe_in + np.array([-1.0, 0.45, 0.0]), 0.13, cfg.GOLD, layers=12)
            self.parts += [pipe, valve]
        if self.parts:
            for part in self.parts:
                if part is not getattr(self, "glow", None):
                    part.keep_in_frame = True
            self.stage.add_body(*self.parts)
        self.region = self._gas_region()
        self.cloud = GasCloud(self.stage, self.gas, self.region, colors=colors, radius=radius, speed=speed, follow=follow,
                              trail=trail, spark_axes=spark_axes, spark_sides=spark_sides, spark_size=spark_size)

    def _gas_region(self) -> Chamber:
        return self.chamber

    # --- the model's state ----------------------------------------------------------------------
    def kelvin(self) -> float:
        return self.t_ref * self.cloud.heat ** 2

    def pressure(self) -> float:
        n = self.cloud.active_count() / max(self.n_ref, 1)
        return self.p_ref * pm.pressure_ratio(n, self.cloud.heat ** 2, self.region.volume_ratio())

    def partial(self, species: int) -> float:
        mask = self.gas.active & (self.gas.species == species)
        return self.p_ref * pm.pressure_ratio(mask.sum() / max(self.n_ref, 1), self.cloud.heat ** 2,
                                              self.chamber.volume_ratio())

    # --- animations ---------------------------------------------------------------------------
    def heat_to(self, kelvin: float, **kwargs) -> Param:
        """Tween the temperature (the cloud's speed scale is sqrt(T / T_ref))."""
        return self.cloud.tween("heat", float(np.sqrt(kelvin / self.t_ref)), **kwargs)

    def height_to(self, height: float, **kwargs) -> Param:
        return set_attr(self.stage, self.chamber, "height", height, **kwargs)

    def volume_to(self, ratio: float, **kwargs) -> Param:
        """Move the lid until the volume is ``ratio`` times the reference volume."""
        base = self.chamber.ref_volume / (4 * self.chamber.half_x * self.chamber.half_z)
        return self.height_to(base * ratio, **kwargs)

    def heater_on(self, level: float = 1.0, **kwargs) -> list[Param]:
        return [self.stage.fade(self.glow, level, **kwargs), self.stage.fade(self.coil, level, **kwargs)]

    def lid_point(self, lift: float = 0.0) -> np.ndarray:
        ch = self.chamber
        return np.array([ch.cx, ch.top() + lift, ch.cz])


# ----------------------------------------------------------------------------
# Atoms and molecules
# ----------------------------------------------------------------------------

ATOM_RADIUS = {"H": 0.2, "C": 0.36, "O": 0.33, "N": 0.32, "Cl": 0.42, "He": 0.3}


def molecule(stage: Stage, atoms: Sequence[tuple[str, Sequence[float]]], bonds: Sequence[tuple[int, int]],
             centre=ORIGIN, pose: Callable[[], np.ndarray] | None = None, scale: float = 1.0,
             label: bool = True) -> SimpleNamespace:
    """Balls and rods for a molecule whose atom offsets turn with ``pose()`` (a 3x3 rotation)
    about a (possibly live) ``centre``."""
    balls = []
    for element, offset in atoms:
        local = np.asarray(offset, dtype=float) * scale

        def where(local=local):
            R = pose() if pose is not None else np.eye(3)
            c = centre() if callable(centre) else np.asarray(centre, dtype=float)
            return c + R @ local

        balls.append(Ball(where, ATOM_RADIUS.get(element, 0.35) * (0.85 + 0.15 * scale), cfg.ATOM.get(element, cfg.MUTED),
                          label=element if label else None))
    rods = [Rod(balls[i], balls[j], width=14) for i, j in bonds]
    stage.add_body(*rods, *balls)
    return SimpleNamespace(balls=balls, rods=rods, parts=[*rods, *balls])


def water_atoms(bond: float = 0.96, angle_deg: float = 104.5, scale: float = 0.62) -> list[tuple[str, np.ndarray]]:
    """O at the origin, both H below it, in the xy plane (Angstrom times ``scale``)."""
    half = np.radians(angle_deg / 2)
    h1 = np.array([np.sin(half), -np.cos(half), 0.0]) * bond * scale
    h2 = np.array([-np.sin(half), -np.cos(half), 0.0]) * bond * scale
    return [("O", np.zeros(3)), ("H", h1), ("H", h2)]


def ammonia_atoms(scale: float = 0.62) -> list[tuple[str, np.ndarray]]:
    """N above three H in a trigonal pyramid (H-N-H 107 degrees, N-H 1.01 A)."""
    nh, tilt = 1.01 * scale, np.radians(112)    # angle from the +y axis (lone pair) to each N-H
    atoms = [("N", np.zeros(3))]
    for k in range(3):
        a = 2 * np.pi * k / 3
        atoms.append(("H", nh * np.array([np.sin(tilt) * np.cos(a), np.cos(tilt), np.sin(tilt) * np.sin(a)])))
    return atoms




# ----------------------------------------------------------------------------
# Numbers: always from the model, formatted the way they are spoken
# ----------------------------------------------------------------------------


def fx(value: float, decimals: int) -> str:
    """On-screen number with exactly the digits the narrator says."""
    return gd.fixed(value, decimals)


def sci(value: float, digits: int = 1) -> str:
    """LaTeX scientific notation: 4.8 x 10^{-23}."""
    exponent = int(np.floor(np.log10(abs(value))))
    mantissa = value / 10 ** exponent
    return rf"{mantissa:.{digits}f}\times10^{{{exponent}}}"


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
                     txt("Keep following the molecules.", 36, cfg.CYAN)).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.set_stroke("#06131B", width=4, opacity=0.9, background=True)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card




# ----------------------------------------------------------------------------
# A liquid and its vapour: one vessel, a pool, a gas region above it
# ----------------------------------------------------------------------------


class GasRegion(Chamber):
    """The part of a vessel above its liquid pool: a ``Chamber`` whose floor rides on the liquid."""

    def __init__(self, vessel: Chamber, box) -> None:  # deliberately not Chamber.__init__: every size is live
        self.vessel, self.box = vessel, box
        self.ref_volume = vessel.ref_volume

    cx = property(lambda self: self.vessel.cx)
    cz = property(lambda self: self.vessel.cz)
    half_x = property(lambda self: self.vessel.half_x)
    half_z = property(lambda self: self.vessel.half_z)

    def _level(self) -> float:
        return float(np.clip(self.box.level, 0.0, self.vessel.height - 0.05))

    @property
    def floor(self) -> float:
        return self.vessel.floor + self._level()

    @property
    def height(self) -> float:
        return max(self.vessel.height - self._level(), 0.05)


class LiquidFace(Face):
    """A face of the liquid pool. Assumes the camera looks down on the vessel
    (pitch > 0): the far sides sit behind everything inside, the surface sits
    behind the vapour above it, the near sides in front of the pool."""

    def __init__(self, corners, normal, color: str, opacity: float, edge_opacity: float, kind: str,
                 depth: Callable[[], float] = lambda: 1.0) -> None:
        super().__init__(corners, color, opacity=opacity, edge_opacity=edge_opacity)
        self.normal, self.kind, self.depth = np.asarray(normal, dtype=float), kind, depth
        self.poly.set_stroke(width=2.0)

    def place(self, stage, R, visibility):
        # An empty pool shows nothing; the faces fade in over the first few hundredths of depth.
        super().place(stage, R, visibility * float(np.clip(self.depth() / 0.06, 0.0, 1.0)))
        if self.kind == "top":
            self.depth_key = -600.0
        else:
            self.depth_key = 500.0 if float((R @ self.normal)[2]) > 0 else -800.0


class LiquidDots(Dots):
    """Dots of the liquid's molecules, drawn between the far walls and the surface."""

    def place(self, stage, R, visibility):
        super().place(stage, R, visibility)
        self.depth_key = -700.0


class TimedFlashes(Flashes):
    """Flashes that age by the stage clock on their own (for events a scene triggers)."""

    def __init__(self, color: str, size: float = 1.0) -> None:
        super().__init__(color=color, size=size)
        self._last = None

    def place(self, stage, R, visibility):
        now = stage.clock
        if self._last is not None and now > self._last:
            self.age(min(now - self._last, 0.3))
        self._last = now
        super().place(stage, R, visibility)


class Ticker(Body):
    """An invisible body that calls ``fn()`` every time its stage redraws (a per-frame hook)."""

    def __init__(self, fn: Callable[[], None]) -> None:
        super().__init__()
        self.fn = fn

    def place(self, stage, R, visibility):
        self.fn()
        self.depth_key = -1e9


class TwoPhaseBox(GasBox):
    """A vessel holding a liquid pool with its vapour (or gas) above it.

    ``level`` (stage units, tween with ``level_to``) is the depth of the
    liquid. The gas cloud lives in ``self.region``, whose floor rides on the
    liquid surface, so vapour molecules bounce off the liquid; molecules not
    ``active`` are not in the vapour. Liquid molecules are a jittering dense
    packing below the surface (``liquid_spacing`` apart).

    ``condense(k)`` / ``evaporate(k)`` move molecules between vapour and pool
    with a flash (blue down, gold up); ``set_vapour(n)`` does either;
    ``exchange(rate)`` turns on stochastic evaporation (``rate`` molecules per
    second of gas time) and capture of vapour molecules striking the surface
    (a dynamic equilibrium). Only for ``IdealGas`` vapour. Assumes the camera
    looks down on the vessel (pitch > 0)."""

    def __init__(self, at=(0.0, -0.4, 0.0), *, level: float = 0.0, liquid_color: str = cfg.LIQUID,
                 liquid_spacing: float = 0.24, liquid_opacity: float = 0.22, seed: int = cfg.SEED, **kwargs) -> None:
        self.level = float(level)
        super().__init__(at, seed=seed, **kwargs)
        ch = self.chamber
        c = ch.corner

        def lc(sx, sy, sz):
            p = c(sx, 0, sz)
            p[1] = ch.floor + sy * float(np.clip(self.level, 0.0, ch.height))
            return p

        edge = cfg.LIQUID_EDGE

        def depth() -> float:
            return float(self.level)

        sides = [
            LiquidFace(lambda: [lc(-1, 0, -1), lc(1, 0, -1), lc(1, 1, -1), lc(-1, 1, -1)], (0, 0, -1), liquid_color,
                       liquid_opacity, 0.3, "side", depth),
            LiquidFace(lambda: [lc(-1, 0, 1), lc(1, 0, 1), lc(1, 1, 1), lc(-1, 1, 1)], (0, 0, 1), liquid_color,
                       liquid_opacity, 0.3, "side", depth),
            LiquidFace(lambda: [lc(-1, 0, -1), lc(-1, 0, 1), lc(-1, 1, 1), lc(-1, 1, -1)], (-1, 0, 0), liquid_color,
                       liquid_opacity, 0.3, "side", depth),
            LiquidFace(lambda: [lc(1, 0, -1), lc(1, 0, 1), lc(1, 1, 1), lc(1, 1, -1)], (1, 0, 0), liquid_color,
                       liquid_opacity, 0.3, "side", depth),
        ]
        self.surface = LiquidFace(lambda: [lc(-1, 1, -1), lc(1, 1, -1), lc(1, 1, 1), lc(-1, 1, 1)], (0, 1, 0), edge,
                                  liquid_opacity * 0.9, 0.85, "top", depth)
        self.liquid_faces = [*sides, self.surface]
        rng = np.random.default_rng(seed + 1)
        sp = float(liquid_spacing)
        fx = (np.arange(0.5, max(int(2 * ch.half_x / sp), 1)) * sp) / (2 * ch.half_x)
        fz = (np.arange(0.5, max(int(2 * ch.half_z / sp), 1)) * sp) / (2 * ch.half_z)
        ys = np.arange(0.5 * sp, ch.height + 1e-9, 0.9 * sp)
        grid = np.array([(a, y, b) for y in ys for b in fz for a in fx])
        grid[:, 0] += rng.uniform(-0.15, 0.15, len(grid)) * sp / (2 * ch.half_x)
        grid[:, 2] += rng.uniform(-0.15, 0.15, len(grid)) * sp / (2 * ch.half_z)
        self._sites = grid
        self._phase = rng.uniform(0, 2 * np.pi, size=grid.shape)
        self._omega = rng.uniform(2.0, 4.0, size=grid.shape)
        self._spacing = sp
        self.liquid_dots = LiquidDots(self._liquid_points, mu.mix(liquid_color, cfg.WHITE, 0.3), radius=sp * 0.36)
        self.up_flashes = TimedFlashes(cfg.EVAPORATE, 0.9)
        self.down_flashes = TimedFlashes(cfg.CONDENSE, 0.9)
        self.stage.add_body(*self.liquid_faces, self.liquid_dots)
        self.stage.add_overlay(self.up_flashes, self.down_flashes)
        self._rng = np.random.default_rng(seed + 2)
        self.exchanger: VapourExchange | None = None

    def _gas_region(self) -> Chamber:
        return GasRegion(self.chamber, self)

    def _liquid_points(self) -> np.ndarray:
        ch, sp = self.chamber, self._spacing
        level = float(np.clip(self.level, 0.0, ch.height))
        sites = self._sites[self._sites[:, 1] < level - 0.25 * sp]
        if not len(sites):
            return np.zeros((0, 3))
        idx = self._sites[:, 1] < level - 0.25 * sp
        wobble = 0.16 * sp * np.sin(self.stage.clock * self._omega[idx] + self._phase[idx])
        base = np.column_stack([ch.cx - ch.half_x + sites[:, 0] * 2 * ch.half_x, ch.floor + sites[:, 1],
                                ch.cz - ch.half_z + sites[:, 2] * 2 * ch.half_z])
        return base + wobble

    # --- the pool -----------------------------------------------------------------------------------
    def level_to(self, level: float, **kwargs) -> Param:
        return set_attr(self.stage, self, "level", level, **kwargs)

    def surface_y(self) -> float:
        return self.region.floor

    def vapour_count(self) -> int:
        return self.cloud.active_count()

    def condense(self, k: int) -> None:
        """Move the ``k`` vapour molecules nearest the surface into the pool."""
        active = np.nonzero(self.gas.active)[0]
        if not len(active) or k <= 0:
            return
        order = active[np.argsort(self.cloud.world[active, 1])][:k]
        for i in order:
            self.gas.active[i] = False
            point = self.cloud.world[i].copy()
            point[1] = self.surface_y()
            self.down_flashes.spark(point, 1)

    def evaporate(self, k: int) -> None:
        """Release ``k`` molecules from the surface into the vapour, heading up."""
        idle = np.nonzero(~self.gas.active)[0][:max(k, 0)]
        for i in idle:
            fx, fz = self._rng.uniform(0.08, 0.92, 2)
            self.cloud.activate(int(i), inlet=(fx, 0.02, fz), axis=1)
            self.cloud.world = self.gas.positions(self.region.lo(), self.region.extent())
            self.up_flashes.spark(self.cloud.world[int(i)].copy(), 1)

    def set_vapour(self, n: int) -> None:
        n = int(np.clip(n, 0, self.gas.count))
        have = self.vapour_count()
        if n < have:
            self.condense(have - n)
        elif n > have:
            self.evaporate(n - have)

    def exchange(self, rate: float, capture: float = 1.0, seed: int = cfg.SEED + 3) -> "VapourExchange":
        self.exchanger = VapourExchange(self, rate, capture, seed)
        return self.exchanger


class VapourExchange:
    """Evaporation and condensation at a liquid surface, molecule by molecule.

    Molecules leave the pool at ``rate`` per second of gas time (raise it to
    warm the liquid: more molecules have the energy to escape); every vapour
    molecule that strikes the surface is captured with probability
    ``capture``. Starting from an empty space, the vapour grows until the two
    rates match: a dynamic equilibrium, with molecules still crossing both
    ways. ``rates()`` reports the recent (up, down) rates per second. Seeded,
    so a render at a given frame rate is reproducible."""

    def __init__(self, box: TwoPhaseBox, rate: float, capture: float = 1.0, seed: int = cfg.SEED + 3) -> None:
        self.box, self.rate, self.capture = box, float(rate), float(capture)
        self.rng = np.random.default_rng(seed)
        self.enabled = True
        self.owed = 0.0
        self.up: list[float] = []
        self.down: list[float] = []
        self._last = box.cloud.time
        box.cloud.hit_hook = self._on_hit
        box.stage.add_body(Ticker(self._tick))

    def _on_hit(self, i: int, axis: int, side: int) -> None:
        if not self.enabled or axis != 1 or side != 0 or not self.box.gas.active[i]:
            return
        if self.rng.random() < self.capture:
            self.box.gas.active[i] = False
            point = self.box.cloud.world[i].copy()
            point[1] = self.box.surface_y()
            self.box.down_flashes.spark(point, 1)
            self.down.append(self.box.cloud.time)

    def _tick(self) -> None:
        now = self.box.cloud.time
        dt = max(now - self._last, 0.0)
        self._last = now
        if not self.enabled or dt <= 0:
            return
        self.owed += self.rate * dt
        while self.owed >= 1.0:
            self.owed -= 1.0
            if (~self.box.gas.active).any():
                self.box.evaporate(1)
                self.up.append(now)
        cut = now - 12.0
        self.up = [t for t in self.up if t > cut]
        self.down = [t for t in self.down if t > cut]

    def tween_rate(self, value: float, **kwargs) -> Param:
        return set_attr(self.box.stage, self, "rate", value, **kwargs)

    def rates(self, window: float = 3.0) -> tuple[float, float]:
        now = self.box.cloud.time
        up = sum(1 for t in self.up if t > now - window)
        down = sum(1 for t in self.down if t > now - window)
        return up / window, down / window


# ----------------------------------------------------------------------------
# Speeds: Maxwell-Boltzmann curves, markers, histograms, a speed colour scale
# ----------------------------------------------------------------------------

# Speed densities from pm.mb_pdf are per (m/s); plots use per (km/s) so axes read ~0-2.5.
PDF_SCALE = 1000.0


def speed_color(speed: float, top: float = 2.0) -> str:
    """Slow (blue) -> cyan -> white -> gold -> fast (orange), for ``speed`` in [0, top]."""
    stops = [cfg.SLOW, cfg.CYAN, cfg.WHITE, cfg.GOLD, cfg.FAST]
    x = float(np.clip(speed / top, 0, 1)) * (len(stops) - 1)
    i = min(int(x), len(stops) - 2)
    return mu.mix(stops[i], stops[i + 1], x - i)


def speed_axes(u_max: float, y_max: float, *, at=ORIGIN, x_length: float = 8.0, y_length: float = 3.6,
               ticks: Sequence[float] = (), unit: str = "m/s", x_label: str = "u", y_label: str = "") -> Axes:
    """Axes for a speed distribution: speed (gold symbol) along x, fraction of molecules up y.

    ``axes.unit`` is a small unit label just right of the x symbol (keep ~1 unit of frame free there)."""
    axes = plot_axes((0, u_max), (0, y_max), x_length=x_length, y_length=y_length, at=at, x_label=x_label,
                     y_label=y_label, x_color=cfg.VELOCITY, x_ticks=ticks)
    axes.unit = txt(unit, cfg.FONT["tiny"], cfg.MUTED).next_to(axes.labels[0], RIGHT, buff=0.14, aligned_edge=DOWN)
    decorative(axes.unit)
    axes.add(axes.unit)
    return axes


def mb_curve(axes: Axes, T: float, M: float, color: str = cfg.GOLD, *, u_max: float, width: float = 6,
             fill_opacity: float = 0.0, samples: int = 160) -> VGroup:
    """The 3D Maxwell-Boltzmann speed density of molar mass ``M`` (kg/mol) at ``T`` (K), on ``axes``.

    With ``fill_opacity`` the area under the curve is shaded (it is always 1)."""
    us = np.linspace(0, u_max, samples)
    ys = pm.mb_pdf(us, T, M) * PDF_SCALE
    pts = [axes.c2p(u, y) for u, y in zip(us, ys)]
    core = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0).set_points_smoothly(pts)
    glow = core.copy().set_stroke(color, width=width * 3.2, opacity=0.14)
    group = VGroup()
    if fill_opacity:
        area = Polygon(axes.c2p(0, 0), *pts, axes.c2p(u_max, 0), stroke_width=0, fill_color=color,
                       fill_opacity=fill_opacity)
        group.add(area)
        group.area = area
    group.add(glow, core)
    group.core = core
    return group


def speed_marker(axes: Axes, u: float, T: float, M: float, color: str, label: str | None = None, *,
                 label_size: int | None = None, lift: float = 0.35) -> VGroup:
    """A dashed drop line at speed ``u`` up to the curve, a glowing dot on the curve, an optional label."""
    top = axes.c2p(u, float(pm.mb_pdf(u, T, M)) * PDF_SCALE)
    line = dashed_path(axes.c2p(u, 0), top, color=color, width=3.2, opacity=0.9)
    dot = glow_dot(top, color, radius=0.08)
    group = VGroup(line, dot)
    group.line, group.dot, group.top = line, dot, top
    if label:
        tag = eq(label, label_size or cfg.FONT["label"], color).next_to(top, UP, buff=lift)
        group.add(tag)
        group.label = tag
    return group


def histogram_bars(axes: Axes, samples: np.ndarray, edges: np.ndarray, color: str = cfg.MOLECULE, *,
                   scale: float = 1.0, fill_opacity: float = 0.45) -> VGroup:
    """Bars of a sample's probability density (count / (N * bin width)) times ``scale``."""
    counts, _ = np.histogram(np.asarray(samples, dtype=float), bins=edges)
    density = counts / (max(len(samples), 1) * (edges[1] - edges[0])) * scale
    bars = VGroup()
    for a, b, d in zip(edges[:-1], edges[1:], density):
        if d <= 0:
            continue
        bars.add(Polygon(axes.c2p(a, 0), axes.c2p(b, 0), axes.c2p(b, d), axes.c2p(a, d), stroke_color=color,
                         stroke_width=1.5, fill_color=color, fill_opacity=fill_opacity))
    return bars


# ----------------------------------------------------------------------------
# The one-speed start: 2D hard disks, drawn flat (a two-dimensional model)
# ----------------------------------------------------------------------------


class DiskView(VGroup):
    """Playback of ``pm.disk_movie()`` at simulation time ``clock`` (tween ``clock.to``).

    Disks are coloured by speed (``speed_color``), so the start — every disk
    at one speed — is one colour, and the colours spread as collisions trade
    energy. ``follow`` rings one disk in gold; ``speeds()`` is the current
    sample for a live histogram. Never ``.animate`` a DiskView."""

    BINS = 9

    def __init__(self, at=ORIGIN, unit: float = 0.25, follow: int | None = None, top_speed: float = 2.2) -> None:
        super().__init__()
        self.pos, self.vel, self.times = pm.disk_movie()
        self.unit, self.top_speed = float(unit), float(top_speed)
        self.at = np.asarray(at, dtype=float)
        self.clock = Knob(0.0)
        self.follow, self.follow_alpha = follow, 0.0
        W, H = pm.DISK_BOX
        self.frame_box = RoundedRectangle(width=W * unit, height=H * unit, corner_radius=0.12, stroke_color=cfg.GLASS,
                                          stroke_width=3, stroke_opacity=0.7, fill_color=cfg.PANEL, fill_opacity=0.35)
        self.frame_box.move_to(self.at)
        self.template = Circle(radius=1.0, num_components=6).points.copy()
        self.r = pm.DISK_RADIUS * unit
        self.layers = []
        for k in range(self.BINS):
            color = speed_color((k + 0.5) / self.BINS * top_speed, top_speed)
            self.layers.append((VMobject(stroke_width=0, fill_color=mu.shade(color, 0.55), fill_opacity=1),
                                VMobject(stroke_width=0, fill_color=color, fill_opacity=1)))
        self.ring = Circle(radius=self.r * 2.2, stroke_color=cfg.GOLD, stroke_width=4, fill_opacity=0)
        self.ring_glow = Circle(radius=self.r * 2.2, stroke_color=cfg.GOLD, stroke_width=12, stroke_opacity=0.15,
                                fill_opacity=0)
        self.add(self.frame_box, *[m for pair in self.layers for m in pair], self.ring_glow, self.ring)
        self.add_updater(lambda m: m.refresh())
        self.refresh()

    def _index(self, t: float) -> float:
        return float(np.clip(t / (self.times[1] - self.times[0]), 0, len(self.times) - 1.001))

    def positions(self, t: float | None = None) -> np.ndarray:
        k = self._index(self.clock.value if t is None else t)
        i, f = int(k), k - int(k)
        xy = self.pos[i] * (1 - f) + self.pos[i + 1] * f
        return np.column_stack([xy * self.unit, np.zeros(len(xy))]) + self.at

    def speeds(self, t: float | None = None) -> np.ndarray:
        k = int(round(self._index(self.clock.value if t is None else t)))
        return np.linalg.norm(self.vel[k], axis=1)

    def follow_point(self) -> np.ndarray:
        return self.positions()[self.follow]

    def follow_speed(self) -> float:
        return float(self.speeds()[self.follow])

    def _circles(self, centres: np.ndarray, r: float) -> np.ndarray:
        if len(centres) == 0:
            return np.zeros((0, 3))
        pts = self.template[None, :, :] * r + centres[:, None, :]
        return pts.reshape(-1, 3)

    def refresh(self) -> "DiskView":
        c = self.positions()
        s = self.speeds()
        bins = np.clip((s / self.top_speed * self.BINS).astype(int), 0, self.BINS - 1)
        for k, (base, mid) in enumerate(self.layers):
            mask = bins == k
            base.points = self._circles(c[mask], self.r)
            mid.points = self._circles(c[mask] + np.array([-0.2, 0.2, 0]) * self.r, self.r * 0.7)
        if self.follow is not None and self.follow_alpha > 0.004:
            p = c[self.follow]
            self.ring.move_to(p).set_stroke(opacity=self.follow_alpha)
            self.ring_glow.move_to(p).set_stroke(opacity=0.15 * self.follow_alpha)
        else:
            self.ring.set_stroke(opacity=0)
            self.ring_glow.set_stroke(opacity=0)
        return self


# ----------------------------------------------------------------------------
# 3D helpers: glass spheres, axis triads, surfaces
# ----------------------------------------------------------------------------


def glass_sphere(stage: Stage, centre, radius, color: str, *, presence: float = 1.0, **kwargs) -> SimpleNamespace:
    """A translucent sphere as two bodies (back and front half) so what is inside sorts between them.

    ``centre`` and ``radius`` may be functions (a growing velocity-space shell)."""
    back = SphereHalf(centre, radius, color, front=False, **kwargs)
    front = SphereHalf(centre, radius, color, front=True, **kwargs)
    back.presence = front.presence = presence
    stage.add_body(back, front)
    return SimpleNamespace(back=back, front=front, parts=[back, front])


def fade_all(stage: Stage, parts: Sequence, value: float, **kwargs) -> list[Param]:
    """Fade several bodies or overlays of one stage together."""
    return [stage.fade(part, value, **kwargs) for part in parts]


def axis_triad(stage: Stage, origin, ends: Sequence, colors: Sequence[str], labels: Sequence[str], *,
               width: float = 4.0, label_size: int | None = None, offsets: Sequence | None = None,
               dashed: Sequence[bool] | None = None) -> SimpleNamespace:
    """Three (or any number of) axes from ``origin`` with LaTeX labels pinned beyond their ends."""
    segments, tags = [], []
    origin = np.asarray(origin, dtype=float)
    for k, (end, color, label) in enumerate(zip(ends, colors, labels)):
        end = np.asarray(end, dtype=float)
        segments.append(Segment(origin, end, color, width=width, opacity=0.9,
                                dashed=bool(dashed[k]) if dashed else False))
        direction = mu.unit(end - origin)
        offset = np.asarray(offsets[k], dtype=float) if offsets else np.zeros(3)
        tags.append(Tag(eq(label, label_size or cfg.FONT["section"], color), end + direction * 0.35, offset))
    for segment in segments:
        segment.keep_in_frame = True
    stage.add_body(*segments)
    stage.add_overlay(*tags)
    return SimpleNamespace(segments=segments, tags=tags, parts=[*segments, *tags])


def surface_faces(point: Callable[[float, float], np.ndarray], us: Sequence[float], vs: Sequence[float],
                  color: Callable[[float, float], str], *, opacity: float = 0.5,
                  edge_opacity: float = 0.15) -> list[Face]:
    """Quads of a parametric surface ``point(u, v)`` (world coordinates), each coloured at its centre."""
    faces = []
    for i in range(len(us) - 1):
        for j in range(len(vs) - 1):
            corners = [point(us[i], vs[j]), point(us[i + 1], vs[j]), point(us[i + 1], vs[j + 1]), point(us[i], vs[j + 1])]
            mid_u, mid_v = (us[i] + us[i + 1]) / 2, (vs[j] + vs[j + 1]) / 2
            faces.append(Face(corners, color(mid_u, mid_v), opacity=opacity, edge_opacity=edge_opacity))
    return faces


def surface_lines(point: Callable[[float, float], np.ndarray], us: Sequence[float], vs: Sequence[float], *,
                  fine: int = 60, color: str = cfg.WHITE, opacity: float = 0.35, width: float = 1.4) -> list[Curve]:
    """Mesh lines along both parameters (constant u and constant v)."""
    lines = []
    fu = np.linspace(us[0], us[-1], fine)
    fv = np.linspace(vs[0], vs[-1], fine)
    for v in vs:
        lines.append(Curve(np.array([point(u, v) for u in fu]), color, width=width, glow=False, opacity=opacity))
    for u in us:
        lines.append(Curve(np.array([point(u, v) for v in fv]), color, width=width, glow=False, opacity=opacity))
    return lines


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "gd", "np", "SimpleNamespace"]
