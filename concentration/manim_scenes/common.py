"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing map reads as a conclusion rather than a new picture:

* a **solution** is real glassware on a turning 3D ``Stage`` (``stage3d.py``):
  a beaker, a graduated cylinder or a volumetric flask whose liquid height
  follows its *volume* through the glass's real shape;
* its **molecules** are a ``Swarm``: solvent as fine blue dots (or beads,
  when we count them), solute as glowing gold beads, drawn at the true
  1 : 100 glucose-to-water ratio whenever the picture claims a ratio;
* the **solution's volume** is a purple glow around the liquid; the
  **solvent's mass** is cyan on a balance; the **solution's mass** is rose;
* **what we count** — moles, equivalents, mole fractions — is teal;
* a **concentration** is always a fraction whose numerator and denominator
  carry those same colours, so the denominator that changes is the one that
  changes colour;
* a confirmed result is green; a trap or a wrong denominator is red.

Scene files compose these pieces and choreograph them against the beats in
``narration.py``; nothing in a scene file should invent a second way to draw
one of these ideas, or type a number that ``utils.physics_models`` supplies.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from manim import *

import config as cfg
from manim_scenes.stage3d import (Ball, Box, Face, Glassware, Halo, Param, Rod, Segment, Stage, Swarm, Tag,
                                  Vector)
from narration import SCRIPT
from utils import concentration_data as cd
from utils import math_utils as mu
from utils import physics_models as pm
from utils.render_helpers import fit_inside, fit_to_safe_frame, fit_width

REF = pm.REFERENCE


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
    """Animate any live value (a swarm's speed, a meter's volume) without copying ``mob``."""
    return Param(mob, getter, setter, target, mode=mode, **kwargs)


def set_attr(stage: Stage, obj, name: str, value: float, **kwargs) -> Param:
    """Tween ``obj.name`` (any attribute a stage body reads every frame)."""
    return Param(stage, lambda: getattr(obj, name), lambda v: setattr(obj, name, v), value, **kwargs)


class Knob:
    """A plain number that animations can tween and updaters can read."""

    def __init__(self, value: float) -> None:
        self.value = float(value)

    def to(self, holder: Mobject, value: float, **kwargs) -> Param:
        return Param(holder, lambda: self.value, lambda v: setattr(self, "value", v), value, **kwargs)


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
    glow = main.copy().set_fill(opacity=0).set_stroke(color, width=12, opacity=0.14)
    decorative(glow)
    group = VGroup(shadow, glow, main)
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
    label = eq(latex, size or cfg.FONT["body"], color)
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


def title_card(big: str, small: str, color: str = cfg.GOLD) -> VGroup:
    """The film's title: a big warm line and a smaller cyan one, with an outline,
    an offset shadow and a soft glow."""
    line_one = Text(big, font=cfg.TITLE_FONT, weight=BOLD, font_size=96, color=color)
    line_two = Text(small, font=cfg.TITLE_FONT, weight=BOLD, font_size=56, color=cfg.CYAN)
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


def boxed(mob: Mobject, color: str = cfg.RESULT, buff: float = 0.22) -> VGroup:
    """A result in a glowing box (the film's \\boxed{})."""
    return VGroup(glow_frame(mob, color, buff=buff), mob)


# ----------------------------------------------------------------------------
# Numbers: always from the model, formatted the way they are spoken
# ----------------------------------------------------------------------------


def fx(value: float, decimals: int) -> str:
    """On-screen number with exactly the significant zeros the narrator says."""
    return cd.fixed(value, decimals)


M_TEXT = fx(REF.molarity, 3)            # 0.524
m_TEXT = fx(REF.molality, 3)            # 0.556
X_TEXT = fx(REF.x_solute, 5)            # 0.00990
W_TEXT = fx(REF.mass_percent, 2)        # 9.09
WV_TEXT = fx(REF.wv_percent, 2)         # 9.42
N_SOLUTE = fx(REF.n_solute, 3)          # 0.100
N_SOLVENT = fx(REF.n_solvent, 1)        # 10.0
V_L = fx(REF.volume_L, 4)               # 0.1910
V_ML = fx(REF.volume_mL, 1)             # 191.0
KG = fx(REF.solvent_kg, 4)              # 0.1800


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
    """A 2D particle with the same shading as a swarm bead."""
    base = Circle(radius=radius, stroke_width=0, fill_color=mu.shade(color, 0.55), fill_opacity=1)
    mid = Circle(radius=radius * 0.72, stroke_width=0, fill_color=color, fill_opacity=1).shift(UL * radius * 0.18)
    glint = Circle(radius=radius * 0.24, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.75)
    glint.shift(UL * radius * 0.36)
    parts = [base, mid, glint]
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


def glow_arrow(start, end, color: str, width: float = 6, tip: float = 0.28) -> VGroup:
    under = Line(start, end, stroke_color=color, stroke_width=width * 3.2, stroke_opacity=0.16)
    arrow = Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=tip,
                  max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)
    return VGroup(under, arrow)


def glow_line(start, end, color: str, width: float = 3.5) -> VGroup:
    """A thin glowing connector (the opening's 'threads' from glass to number)."""
    return VGroup(Line(start, end, stroke_color=color, stroke_width=width * 4, stroke_opacity=0.12),
                  Line(start, end, stroke_color=color, stroke_width=width * 2, stroke_opacity=0.25),
                  Line(start, end, stroke_color=mu.mix(color, cfg.WHITE, 0.3), stroke_width=width))


def dashed_path(a, b, color: str = cfg.MUTED, width: float = 2.4, opacity: float = 0.55, dash: float = 0.13) -> VMobject:
    line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    count = max(int(float(np.linalg.norm(b - a)) / (2 * dash)), 1)
    for k in range(count):
        line.start_new_path(a + (b - a) * k / count)
        line.add_line_to(a + (b - a) * (k + 0.55) / count)
    return line


# ----------------------------------------------------------------------------
# Solutions on a stage
# ----------------------------------------------------------------------------


def solution_stage(at, *, profile=None, volume: float = REF.volume_mL, zoom: float = 1.0, yaw: float = 0.3,
                   pitch: float = 0.3, spin: float = 0.12, sway: float = 0.05, solvent: int = 500, solute: int = 5,
                   seed: int = 0, style: str = "dots", solvent_radius: float | None = None,
                   solute_radius: float = 0.12, amplitude: float = 0.07, mark: bool = False, ticks=(),
                   lid: bool = False, scale: float = 1.0,
                   liquid_color: str = cfg.LIQUID) -> tuple[Stage, Glassware, Swarm]:
    """A glass of solution on a gently turning stage, origin at the glass's base centre.

    The stage anchor is the screen point of the base; the glass grows upward
    from it. Particle counts keep the reference solution's 1 : 100 ratio.
    """
    profile = profile or pm.beaker_profile()
    stage = Stage(at, zoom=zoom, yaw=yaw, pitch=pitch, spin=spin, sway=sway)
    glass = Glassware(stage, profile, volume=volume, mark=mark, ticks=ticks, lid=lid, scale=scale,
                      liquid_color=liquid_color)
    radius = solvent_radius or (0.034 if style == "dots" else 0.075)
    swarm = Swarm(stage, glass, solvent=solvent, solute=solute, seed=cfg.SEED + seed, style=style,
                  solvent_radius=radius, solute_radius=solute_radius, amplitude=amplitude)
    return stage, glass, swarm


def molecule_model(stage: Stage, molecule: pm.Molecule, *, scale: float = 0.8, origin=ORIGIN,
                   labels: bool = False, radius_scale: float = 1.0) -> dict:
    """Ball-and-stick model of a ``physics_models.Molecule`` on a stage."""
    origin = np.asarray(origin, dtype=float)
    balls = []
    for element, position in zip(molecule.elements, molecule.positions):
        ball = Ball(origin + position * scale, cfg.ELEMENT_RADII[element] * radius_scale * scale / 0.8,
                    cfg.ELEMENT_COLORS[element], element if labels else None)
        balls.append(ball)
    rods = [Rod(balls[i], balls[j], order, width=11 * scale / 0.8) for i, j, order in molecule.bonds]
    stage.add_body(*rods, *balls)
    return {"balls": balls, "rods": rods}


def move_ball(stage: Stage, ball: Ball, target, **kwargs) -> Param:
    """Glide one atom to a 3D point (a proton leaving its acid)."""
    return Param(stage, ball.where, lambda v: setattr(ball, "pos", np.array(v)), np.asarray(target, dtype=float),
                 mode="vector", **kwargs)


# ----------------------------------------------------------------------------
# Live numbers and instruments (2D)
# ----------------------------------------------------------------------------


def live_number(getter: Callable[[], float], decimals: int, size: int | None = None, color: str = cfg.WHITE) -> DecimalNumber:
    """A number that re-reads ``getter`` every frame."""
    number = DecimalNumber(getter(), num_decimal_places=decimals, font_size=(size or cfg.FONT["section"]) * 1.2,
                           color=color)
    number.set_stroke(cfg.BG, width=0.65, opacity=0.85, background=True)
    number.add_updater(lambda m: m.set_value(getter()))
    return number


class Meter(VGroup):
    """A labelled readout: name, live value, unit, in a panel."""

    def __init__(self, name: str, getter: Callable[[], float], decimals: int, unit_tex: str, color: str, *,
                 width: float = 4.6) -> None:
        super().__init__()
        self.title = txt(name, cfg.FONT["small"], color)
        self.value = live_number(getter, decimals, cfg.FONT["section"], cfg.WHITE)
        self.unit = eq(unit_tex, cfg.FONT["small"], color)
        row = VGroup(self.value, self.unit).arrange(RIGHT, buff=0.32, aligned_edge=DOWN)
        body = VGroup(self.title, row).arrange(DOWN, buff=0.28)
        self.box = RoundedRectangle(width=max(width, body.width + 0.6), height=body.height + 0.6, corner_radius=0.22,
                                    stroke_color=color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.9)
        body.move_to(self.box)
        self.row = row
        self.add(self.box, body)


class Balance(VGroup):
    """A digital lab balance: a pan, a body and a glowing readout in grams."""

    def __init__(self, at=ORIGIN, *, color: str = cfg.SOLVENT_MASS, width: float = 4.4, grams: float = 0.0) -> None:
        super().__init__()
        self.grams = float(grams)
        self.color = color
        body = Polygon([-width / 2, 0, 0], [width / 2, 0, 0], [width / 2 - 0.3, -1.15, 0], [-width / 2 + 0.3, -1.15, 0],
                       stroke_color=cfg.MUTED, stroke_width=2.5, fill_color="#14324F", fill_opacity=1)
        top = Rectangle(width=width, height=0.12, stroke_width=0, fill_color="#2A4D6B", fill_opacity=1).next_to(body, UP, buff=0)
        stem = Rectangle(width=0.22, height=0.22, stroke_width=0, fill_color="#5D7488", fill_opacity=1).next_to(top, UP, buff=0)
        pan = Ellipse(width=width * 0.78, height=0.32, stroke_color=cfg.GLASS, stroke_width=2.5, fill_color="#7D93A8",
                      fill_opacity=1).next_to(stem, UP, buff=-0.08)
        facets = VGroup()
        for k in range(9):
            a, b = k/9, (k+1)/9
            pts = [[-width/2 + width*a,0,0],[-width/2 + width*b,0,0],
                   [-width/2+.3 + (width-.6)*b,-1.15,0],[-width/2+.3 + (width-.6)*a,-1.15,0]]
            facets.add(Polygon(*pts,stroke_width=0,fill_color=mu.mix("#163149","#6D8798",0.28+0.5*(1-abs(k-3)/6)),fill_opacity=1))
        pan_glints = VGroup(*[Ellipse(width=width*.78*f,height=.32*f,stroke_width=0,
                                      fill_color=mu.mix("#617786",cfg.GLASS,(1-f)*1.3),fill_opacity=0.48)
                              .move_to(pan.get_center()+UP*.018*(1-f)) for f in (.94,.75,.50)])
        screen = RoundedRectangle(width=width * 0.6, height=0.78, corner_radius=0.08, stroke_color=color, stroke_width=2,
                                  fill_color="#04121F", fill_opacity=1).move_to(body.get_center() + DOWN * 0.08)
        self.readout = live_number(lambda: self.grams, 1, cfg.FONT["body"], color)
        self.unit = txt("g", cfg.FONT["small"], color)
        self.display = VGroup(self.readout, self.unit)
        self._screen = screen
        self.readout.add_updater(lambda m: self._layout())
        self.pan, self.body = pan, body
        self.add(body, facets, top, stem, pan, pan_glints, screen, self.readout, self.unit)
        self.move_to(at)
        self._layout()

    def _layout(self) -> None:
        group = VGroup(self.readout, self.unit)
        group.arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        fit_inside(group, self._screen.width - 0.2, self._screen.height - 0.08)
        group.move_to(self._screen)

    def pan_top(self) -> np.ndarray:
        return self.pan.get_top() + DOWN * 0.04

    def weigh(self, grams: float, run_time: float = 1.2) -> Param:
        return Param(self, lambda: self.grams, lambda v: setattr(self, "grams", v), grams, run_time=run_time)


class Thermometer(VGroup):
    """A glowing thermometer whose column follows ``celsius`` (a Knob)."""

    def __init__(self, at=ORIGIN, *, low: float = -5.0, high: float = 105.0, height: float = 4.2,
                 color: str = cfg.HEAT) -> None:
        super().__init__()
        self.low, self.high, self.h = low, high, height
        self.celsius = Knob(20.0)
        tube = RoundedRectangle(width=0.36, height=height, corner_radius=0.18, stroke_color=cfg.GLASS, stroke_width=3,
                                fill_color=cfg.PANEL, fill_opacity=0.9)
        bulb = Circle(radius=0.32, stroke_color=cfg.GLASS, stroke_width=3, fill_color=color, fill_opacity=1)
        bulb.next_to(tube, DOWN, buff=-0.12)
        self.tube, self.bulb, self.color = tube, bulb, color
        self.column = Rectangle(width=0.18, height=0.1, stroke_width=0, fill_color=color, fill_opacity=1)
        self.add(tube, bulb, self.column)
        self.move_to(at)
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


def countdown(scene: Scene, at, seconds: int = 3, color: str = cfg.GOLD) -> None:
    """A shrinking ring with 3, 2, 1 — the traps' thinking time."""
    for k in range(seconds, 0, -1):
        digit = txt(str(k), 80, color).move_to(at)
        ring = Circle(radius=0.62, stroke_color=color, stroke_width=7, fill_opacity=0).move_to(at)
        scene.add(digit, ring)
        scene.play(Uncreate(ring), digit.animate.set_opacity(0.15), run_time=1.0, rate_func=linear)
        scene.remove(digit, ring)


# ----------------------------------------------------------------------------
# Concentration fractions in the film's colours
# ----------------------------------------------------------------------------


def fraction(name_tex: str, top_tex: str, bottom_tex: str, top_color: str, bottom_color: str,
             size: int | None = None) -> MathTex:
    """``name = top / bottom`` with the numerator and denominator in their meaning colours.

    Parts: [0] name, [1] '=', [2] '\\frac{', [3] top, [4] '}{', [5] bottom, [6] '}'.
    """
    tex = eq([name_tex, "=", r"\frac{", top_tex, "}{", bottom_tex, "}"], size)
    tex[3].set_color(top_color)
    tex[5].set_color(bottom_color)
    return tex


def numbers_fraction(top: str, bottom: str, result: str, top_color: str, bottom_color: str,
                     size: int | None = None, result_color: str = cfg.RESULT) -> MathTex:
    """``top / bottom = result``. Parts: [0] '\\frac{', [1] top, [2] '}{', [3] bottom, [4] '}', [5] '=', [6] result."""
    tex = eq([r"\frac{", top, "}{", bottom, "}", "=", result], size)
    tex[1].set_color(top_color)
    tex[3].set_color(bottom_color)
    tex[6].set_color(result_color)
    return tex


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
                     txt("Keep asking what you're comparing.", 36, cfg.CYAN)).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "cd", "np", "REF"]
