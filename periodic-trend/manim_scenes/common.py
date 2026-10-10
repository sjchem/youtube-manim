"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing heat maps read as a conclusion rather than a new picture:

* an **atom** is a glowing nucleus inside a slowly turning cloud of dots. Each
  dot is a seeded sample of a hydrogen-like radial density, so dense regions
  are more probable and the fringe is rare. The 3D radial sample is normalized
  to put approximately 90 % inside a unit sphere, then projected and scaled for each shot.
  The dashed contour is a display guide, not a measured probability boundary
  or a hard atomic edge; these are schematic clouds, not element-specific orbitals.
* **inner (core) electrons** are a smaller, gray cloud: background structure
  that shields;
* the **pull** of the nucleus is always gold arrows pointing inward, their
  thickness scaled by Slater's estimate of the charge the electron feels;
* an **element** is a rounded tile outlined in its block colour, and the
  **table** is never typed: every tile goes where ``utils.physics_models``
  says the filling of electrons puts it (exactly as in Part 3);
* a **property** is one cool-to-warm colour scale, and in 3D, a tower height;
* **energy released** is green, **energy required** is orange.

Scene files compose these pieces and choreograph them against the beats in
``narration.py``; nothing in a scene file should invent a second way to draw
one of these ideas.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

import numpy as np
from manim import *

import config as cfg
from narration import SCRIPT
from utils import element_data as ed
from utils import math_utils as mu
from utils import physics_models as pm
from utils.render_helpers import fit_inside, fit_to_safe_frame, fit_width

def fade_labels(old, new) -> list[Animation]:
    """Fade out, pause briefly, then fade in; preserve fixed 3D HUD objects."""
    return [FadeOut(old, rate_func=lambda a: smooth(min(a / 0.45, 1.0))),
            FadeIn(new, rate_func=lambda a: smooth(max((a - 0.55) / 0.45, 0.0)))]


class FadeThrough(FadeTransform):
    """Replace a label with a short clear interval, avoiding ghosted words.

    Keep Manim's replacement cleanup and live-object freezing, but fade the
    source completely before the target appears. Optional ``parent`` puts a
    replacement back inside its atom rather than leaving a floating label.
    """

    def __init__(self, mobject, target_mobject, *, parent=None, **kwargs):
        self.label_parent = parent
        super().__init__(mobject, target_mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        phases = (min(alpha / 0.45, 1.0), max((alpha - 0.55) / 0.45, 0.0))
        for index, phase in enumerate(phases):
            for current, first, last in zip(
                self.mobject[index].get_family(),
                self.starting_mobject[index].get_family(),
                self.ending_mobject[index].get_family(),
            ):
                current.interpolate(first, last, self.rate_func(phase), path_func=self.path_func)

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        if self.label_parent is not None:
            scene.remove(self.to_add_on_completion)
            self.label_parent.add(self.to_add_on_completion)


# ----------------------------------------------------------------------------
# Scene lifecycle
# ----------------------------------------------------------------------------


def _leaf_animations(animations):
    for animation in animations:
        if isinstance(animation, AnimationGroup):
            yield from _leaf_animations(animation.animations)
        else:
            yield animation


def flatten_animation_groups(scene: Scene) -> None:
    """Stop AnimationGroup from adding a second copy of its members to the scene.

    Manim CE adds an AnimationGroup's ``Group`` of mobjects to the scene as a
    new top-level entry, so members that already live inside an atom are drawn
    twice — the second time on top of the nucleus. The scene is taught to look
    through groups to the individual animations instead, both when adding
    mobjects and when deciding which ones move.
    """
    if getattr(scene, "_flattens_groups", False):
        return
    add_from = scene.add_mobjects_from_animations
    moving = scene.get_moving_mobjects
    scene.add_mobjects_from_animations = lambda animations: add_from(list(_leaf_animations(animations)))
    scene.get_moving_mobjects = lambda *animations: moving(*_leaf_animations(animations))
    scene._flattens_groups = True


def start(scene: Scene, key: str, title: str | None = None) -> tuple[float, VGroup | None]:
    """Theme the scene, add the quiet background, and show the chapter heading."""
    flatten_animation_groups(scene)
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


def dismiss_opening_title(scene: Scene, started_at: float, head: VGroup | None) -> None:
    """Clear an opening title around four seconds, using the existing cue hold."""
    if head is None:
        return
    if float(scene.time) - started_at < 3.4:
        cue(scene, started_at, 3.4)
    scene.play(FadeOut(head), run_time=0.6)
    if is_3d(scene):
        scene.camera.remove_fixed_in_frame_mobjects(head)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """scene.play with an explicit default run time, so pacing is never accidental."""
    kwargs["run_time"] = kwargs.get("run_time", 1.0)
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Hold the composition steady; live clouds keep turning."""
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
    if is_3d(scene):
        scene.stop_ambient_camera_rotation()
    visible = [mob for mob in scene.mobjects if not getattr(mob, "_is_project_background", False)]
    for mob in visible:
        for member in mob.get_family():
            member.clear_updaters()
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

    The mobjects are registered but not added; bring them in with FadeIn or
    Write only — never morph a 3D object into HUD text (stray glyph copies).
    """
    if is_3d(scene):
        scene.camera.add_fixed_in_frame_mobjects(*mobjects)


def move_camera(scene: Scene, run_time: float = 2.0, **kwargs) -> None:
    """Tilt or zoom only. Recentre a shot by moving the content, never the
    camera's frame_center: that would drag every HUD caption with it."""
    if "frame_center" in kwargs:
        raise ValueError("move the content, not frame_center (HUD text would move too)")
    if is_3d(scene):
        scene.move_camera(run_time=run_time, **kwargs)
    else:
        scene.wait(run_time)


# ----------------------------------------------------------------------------
# Background
# ----------------------------------------------------------------------------


def add_background(scene: Scene) -> VGroup:
    """A faint, static Oceanic background shared by every chapter.

    There is deliberately no flat backdrop rectangle: in a 3D chapter the
    camera draws flat mobjects after the depth-sorted solids, so a backdrop
    would paint over them. The camera background colour does that job.
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
    result.set_stroke(cfg.BG, width=0.75, opacity=0.85, background=True)
    return result


# Computer Modern sets visibly smaller than Lato at the same nominal
# size; this factor makes ``eq(x, 40)`` read as large as ``txt(y, 40)``.
MATH_SCALE = 1.35


def eq(latex: str, size: int | None = None, color: str = cfg.WHITE, **kwargs) -> MathTex:
    """An equation with the same dark outline as the captions, sized like text."""
    result = MathTex(latex, font_size=(size or cfg.FONT["section"]) * MATH_SCALE, color=color, **kwargs)
    result.set_stroke(cfg.BG, width=0.65, opacity=0.85, background=True)
    return result


def signed(value: float, digits: int = 0) -> str:
    """A number with a true minus sign (U+2212), as typeset maths would show it."""
    text = f"{abs(value):.{digits}f}"
    return ("−" if value < 0 else "") + text


def decorative(mob: Mobject) -> Mobject:
    """Mark a glow or shadow copy so the layout audit does not read it as text."""
    for member in mob.get_family():
        member._is_decorative = True
    return mob


def number(value: int, size: int | None = None, color: str = cfg.GOLD) -> Integer:
    """An animatable integer, sized to match ``eq`` and ``txt``."""
    result = Integer(value, font_size=(size or cfg.FONT["section"]) * MATH_SCALE, color=color)
    result.set_stroke(cfg.BG, width=0.65, opacity=0.85, background=True)
    return result


def heading(title: str, color: str = cfg.GOLD, size: int = 46) -> VGroup:
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


def swap_heading(scene: Scene, old: VGroup | None, title: str, run_time: float = 0.6) -> VGroup:
    """Replace the chapter caption (fade, never morph, so HUD registration holds)."""
    new = heading(title)
    hud(scene, new)
    if old is not None:
        scene.play(*fade_labels(old, new), run_time=run_time)
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


def eq_chip(latex: str, color: str = cfg.WHITE, size: int | None = None, stroke: str | None = None) -> VGroup:
    """A rounded pill holding an equation."""
    label = eq(latex, size or cfg.FONT["label"], color)
    pill = RoundedRectangle(
        width=label.width + 0.7, height=label.height + 0.4, corner_radius=0.22,
        stroke_color=stroke or color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.92,
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


def title_card(big: str, small: str, color: str = cfg.GOLD, small_first: bool = False) -> VGroup:
    """The film's title: a big warm line and a smaller cyan one (below it, or
    above it with ``small_first``), with an outline, an offset shadow and a
    soft glow."""
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


# ----------------------------------------------------------------------------
# Glow and marks
# ----------------------------------------------------------------------------


def halo(radius: float, color: str, layers: int = 5, peak_opacity: float = 0.16) -> VGroup:
    """Concentric translucent discs — a soft glow without a raster image."""
    group = VGroup()
    for index in range(layers):
        frac = (index + 1) / layers
        group.add(Circle(radius=radius * (0.35 + 0.65 * frac), stroke_width=0,
                         fill_color=color, fill_opacity=peak_opacity * (1.15 - frac)))
    return group


GLOW_REACH = 1.4


def soft_glow(color: str, layers: int = 14, peak_opacity: float = 0.15, reach: float = GLOW_REACH) -> VGroup:
    """Many faint nested discs: brightest at the centre, fading linearly to
    nothing at ``reach`` (unit radius 1), so a cloud never shows an edge."""
    each = 2.2 * peak_opacity / layers
    return VGroup(*[Circle(radius=reach * (i + 1) / layers, stroke_width=0, fill_color=color, fill_opacity=each)
                    for i in range(layers)])


def glow_dot(point=ORIGIN, radius: float = 0.11, color: str = cfg.ELECTRON_COLOR) -> VGroup:
    """A single, tracked electron: a bright bead with a halo."""
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


def glow_arrow(start, end, color: str, width: float = 6, tip: float = 0.28) -> VGroup:
    """A bold arrow with a soft underglow — trend directions and big moves."""
    under = Line(start, end, stroke_color=color, stroke_width=width * 3.2, stroke_opacity=0.16)
    arrow = Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=tip,
                  max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)
    group = VGroup(under, arrow)
    group.arrow = arrow
    return group


def check_mark(size: float = 0.32, color: str = cfg.GREEN) -> VMobject:
    mark = VMobject(stroke_color=color, stroke_width=8)
    mark.set_points_as_corners([LEFT * size + UP * 0.05, DOWN * size * 0.75 + LEFT * size * 0.15, RIGHT * size + UP * size])
    return mark


def cross_mark(size: float = 0.3, color: str = cfg.RED) -> VGroup:
    return VGroup(
        Line(UL * size, DR * size, stroke_color=color, stroke_width=9),
        Line(UR * size, DL * size, stroke_color=color, stroke_width=9),
    )


def arrow_between(start, end, color: str = cfg.MUTED, width: float = 4) -> Arrow:
    return Arrow(start, end, buff=0.1, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


# ----------------------------------------------------------------------------
# A generic tween, so live objects (clouds, meters) animate their own state
# ----------------------------------------------------------------------------


class Tween(Animation):
    """Animate ``setter(value)`` from ``getter()`` (read when the animation
    begins) to ``target``. Updaters keep running, so a cloud keeps turning
    while it shrinks."""

    def __init__(self, mobject: Mobject, getter: Callable[[], float], setter: Callable[[float], None],
                 target: float, **kwargs) -> None:
        self._get, self._set, self._target = getter, setter, float(target)
        self._from = None
        kwargs.setdefault("suspend_mobject_updating", False)
        super().__init__(mobject, **kwargs)

    def begin(self) -> None:
        self._from = float(self._get())
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        a = self.rate_func(alpha)
        self._set(self._from + (self._target - self._from) * a)


class Glide(Animation):
    """Move a live object (an atom, a cloud, a crystal) to ``point`` by shifting
    it frame by frame. Unlike ``.animate``, nothing is copied or interpolated,
    so a cloud whose dots change every frame cannot be scrambled."""

    def __init__(self, mobject: Mobject, point, **kwargs) -> None:
        self._goal = np.asarray(point, dtype=float)
        self._origin = None
        kwargs.setdefault("suspend_mobject_updating", False)
        super().__init__(mobject, **kwargs)

    def _where(self) -> np.ndarray:
        locate = getattr(self.mobject, "center_point", None)
        return locate() if locate else self.mobject.get_center()

    def begin(self) -> None:
        self._origin = self._where().copy()
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        want = self._origin + (self._goal - self._origin) * self.rate_func(alpha)
        self.mobject.shift(want - self._where())


# ----------------------------------------------------------------------------
# Atoms: nucleus + seeded electron clouds
# ----------------------------------------------------------------------------


class _LiveMixin:
    """Only the original object animates itself.

    Manim keeps calling the updaters of the hidden start/target copies a
    Transform (FadeIn, Indicate, ...) makes. A cloud's dot layers change size
    every frame, so a copy that kept turning would no longer line up with the
    original and the interpolation would scramble the picture. Copies are
    therefore born frozen.
    """

    _live = True

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result._live = False
        return result


class ElectronCloud(_LiveMixin, VGroup):
    """A seeded, slowly turning 3D sample of where an electron is likely to be.

    The underlying radial distribution has approximately 90 % probability within ``radius``
    in 3D; its 2D projection is not a measured atomic radius. Nearer dots are
    brighter. Change
    the size with ``resize`` — the dots keep their size, so a shrinking cloud
    visibly gets denser. Move a cloud by shifting it (or its atom); never
    ``scale`` it, because the next frame redraws it at its own radius.
    """

    BINS = 6

    def __init__(self, radius: float, center=ORIGIN, *, count: int = 220, seed: int = 0,
                 color: str = cfg.ELECTRON_COLOR, dot_radius: float = 0.03, spin: float = 0.3,
                 tilt: float = 0.38, glow: float = 0.15, contour: bool = False, phase: float = 0.0) -> None:
        super().__init__()
        self.unit = pm.cloud_samples(count, cfg.SEED + 7919 * seed)
        self.radius, self.level = float(radius), 1.0
        self.turn, self.spin, self.tilt, self.colour = phase, spin, tilt, color
        self.anchor = Dot(np.asarray(center, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0)
        self.glow = soft_glow(color, peak_opacity=glow) if glow else VGroup()
        self._glow_base = [float(m.get_fill_opacity()) for m in self.glow]
        # Dots are drawn in a few depth bins, each one VMobject of many small
        # circles: Cairo pays per mobject, so 6 bins draw ~10x faster than
        # hundreds of separate Dots, and look identical.
        self._shape = Circle(radius=dot_radius, num_components=5).points.copy()
        self._bin_opacity = np.linspace(0.3, 1.0, self.BINS)
        self.dots = VGroup(*[VMobject(fill_color=color, fill_opacity=o, stroke_width=0) for o in self._bin_opacity])
        if contour:
            ring = Circle(radius=1, stroke_color=color, stroke_width=2.6, stroke_opacity=0.6)
            self.contour = DashedVMobject(ring, num_dashes=44, dashed_ratio=0.55)
        else:
            self.contour = VGroup()
        self._contour_opacity = 0.6
        self.add(self.anchor, self.glow, self.dots, self.contour)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    # -- state ------------------------------------------------------------
    def center_point(self) -> np.ndarray:
        return self.anchor.get_center()

    def glide(self, point, **kwargs) -> Glide:
        return Glide(self, point, **kwargs)

    def set_radius(self, radius: float) -> None:
        self.radius = max(float(radius), 1e-3)
        self._place()

    def set_level(self, level: float) -> None:
        self.level = max(float(level), 0.0)
        self._place()

    def resize(self, radius: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.radius, self.set_radius, radius, **kwargs)

    def fade_to(self, level: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.level, self.set_level, level, **kwargs)

    # -- drawing ------------------------------------------------------------
    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.turn += self.spin * dt
        self._place()

    def _place(self) -> None:
        centre = self.center_point()
        turned = mu.turn_and_tilt(self.unit, self.turn, self.tilt)
        fade = mu.depth_fade(turned[:, 2], pm.CLOUD_REACH) * self.level
        offsets = turned * self.radius
        offsets[:, 2] = 0.0
        offsets += centre
        everything = self._shape[None, :, :] + offsets[:, None, :]
        which = np.clip(np.rint(mu.linear_map(fade / max(self.level, 1e-6), (0.28, 1.0), (0, self.BINS - 1))),
                        0, self.BINS - 1).astype(int)
        for index, (layer, opacity) in enumerate(zip(self.dots, self._bin_opacity)):
            chosen = everything[which == index]
            layer.points = chosen.reshape(-1, 3) if len(chosen) else np.zeros((0, 3))
            layer.fill_rgbas[:, 3] = opacity * self.level  # direct write: set_fill is 20x slower
        if len(self.glow):
            self.glow.set_width(2 * GLOW_REACH * self.radius).move_to(centre)
            for disc, base in zip(self.glow, self._glow_base):
                disc.set_fill(opacity=base * min(self.level, 1.0), family=False)
        if len(self.contour):
            self.contour.set_width(2 * self.radius).move_to(centre)
            self.contour.set_stroke(opacity=self._contour_opacity * min(self.level, 1.0))


class BondCloud(_LiveMixin, VGroup):
    """The shared pair of a horizontal bond: a seeded dot cloud stretched
    between two nuclei, turning about the bond axis.

    ``lean`` runs from -1 (all toward the left atom) through 0 (even sharing)
    to +1 (all toward the right atom); the cloud slides and tightens toward
    the stronger puller. An illustration of unequal sharing, not a computed
    molecular orbital.
    """

    BINS = 6

    def __init__(self, left, right, *, count: int = 320, seed: int = 0, color: str = cfg.ELECTRON_COLOR,
                 width: float = 0.62, dot_radius: float = 0.03, spin: float = 0.6, glow: float = 0.16,
                 lean: float = 0.0) -> None:
        super().__init__()
        self.unit = pm.cloud_samples(count, cfg.SEED + 7919 * seed + 17)
        self.lean, self.level, self.turn, self.spin, self.width_scale = float(lean), 1.0, 0.0, spin, width
        self.ends = VGroup(Dot(np.asarray(left, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0),
                           Dot(np.asarray(right, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0))
        self.glow = soft_glow(color, peak_opacity=glow) if glow else VGroup()
        self._glow_base = [float(m.get_fill_opacity()) for m in self.glow]
        self._shape = Circle(radius=dot_radius, num_components=5).points.copy()
        self._bin_opacity = np.linspace(0.3, 1.0, self.BINS)
        self.dots = VGroup(*[VMobject(fill_color=color, fill_opacity=o, stroke_width=0) for o in self._bin_opacity])
        self.add(self.ends, self.glow, self.dots)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    def set_lean(self, lean: float) -> None:
        self.lean = float(np.clip(lean, -1, 1))
        self._place()

    def lean_to(self, lean: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.lean, self.set_lean, lean, **kwargs)

    def centre(self) -> np.ndarray:
        left, right = self.ends[0].get_center(), self.ends[1].get_center()
        half = (right[0] - left[0]) / 2
        return (left + right) / 2 + RIGHT * self.lean * half * 0.82

    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.turn += self.spin * dt
        self._place()

    def _place(self) -> None:
        left, right = self.ends[0].get_center(), self.ends[1].get_center()
        half = (right[0] - left[0]) / 2
        sx = half * 0.72 * (1 - 0.35 * abs(self.lean))
        sy = self.width_scale * (1 - 0.2 * abs(self.lean))
        turned = self.unit @ mu.rotation_x(self.turn).T
        fade = mu.depth_fade(turned[:, 2], pm.CLOUD_REACH)
        offsets = np.zeros_like(turned)
        offsets[:, 0], offsets[:, 1] = turned[:, 0] * sx, turned[:, 1] * sy
        offsets += self.centre()
        everything = self._shape[None, :, :] + offsets[:, None, :]
        which = np.clip(np.rint(mu.linear_map(fade, (0.28, 1.0), (0, self.BINS - 1))), 0, self.BINS - 1).astype(int)
        for index, (layer, opacity) in enumerate(zip(self.dots, self._bin_opacity)):
            chosen = everything[which == index]
            layer.points = chosen.reshape(-1, 3) if len(chosen) else np.zeros((0, 3))
            layer.fill_rgbas[:, 3] = opacity * self.level
        if len(self.glow):
            self.glow.stretch_to_fit_width(2 * GLOW_REACH * sx).stretch_to_fit_height(2 * GLOW_REACH * sy)
            self.glow.move_to(self.centre())


def nucleus_core(label: str | None, radius: float = 0.3, color: str = cfg.NUCLEUS_COLOR,
                 size: int | None = None) -> VGroup:
    """A glowing nucleus with its charge written on it (not to scale)."""
    glow = halo(radius * 2.5, color, layers=6, peak_opacity=0.24)
    ball = Circle(radius=radius, stroke_color=interpolate_color(ManimColor(color), ManimColor(cfg.WHITE), 0.35),
                  stroke_width=2, fill_color=color, fill_opacity=1)
    ball.set_sheen(-0.45, UL)
    group = VGroup(glow, ball)
    group.ball, group.glow, group.label = ball, glow, None
    if label:
        text = txt(label, size or cfg.FONT["tiny"], cfg.WHITE)
        fit_inside(text, radius * 1.62, radius * 1.05)
        text.move_to(ball)
        group.add(text)
        group.label = text
    return group


class Atom(VGroup):
    """Nucleus, optional gray core cloud, and the cyan outer cloud.

    ``radius`` is in screen units; scenes compute it from measured radii with
    one shared scale per shot. Resize with ``atom.resize(...)``.
    """

    def __init__(self, radius: float, center=ORIGIN, *, charge: str | None = None,
                 core: float | None = None, count: int = 220, core_count: int = 120, seed: int = 0,
                 nucleus_radius: float = 0.3, contour: bool = False, color: str = cfg.ELECTRON_COLOR,
                 dot_radius: float = 0.03, glow: float = 0.15, label_size: int | None = None) -> None:
        super().__init__()
        center = np.asarray(center, dtype=float)
        self.cloud = ElectronCloud(radius, center, count=count, seed=seed, color=color, contour=contour,
                                   dot_radius=dot_radius, glow=glow, phase=0.6 * seed)
        self.core = None
        if core:
            self.core = ElectronCloud(core, center, count=core_count, seed=seed + 101, color=cfg.CORE_COLOR,
                                      dot_radius=dot_radius * 0.85, spin=-0.45, glow=0.10, phase=0.3 * seed)
        self.nucleus = nucleus_core(charge, nucleus_radius, size=label_size).move_to(center)
        self.add(*([self.core] if self.core else []), self.cloud, self.nucleus)

    def center_point(self) -> np.ndarray:
        return self.cloud.center_point()

    @property
    def radius(self) -> float:
        return self.cloud.radius

    def resize(self, radius: float, core: float | None = None, **kwargs) -> list[Animation]:
        """Animations (a list: unpack with ``*``) that change the cloud sizes."""
        animations = [self.cloud.resize(radius, **kwargs)]
        if core is not None and self.core is not None:
            animations.append(self.core.resize(core, **kwargs))
        return animations

    def place(self, point) -> "Atom":
        """Shift instantly so the nucleus sits on ``point`` (use Glide to animate)."""
        return self.shift(np.asarray(point, dtype=float) - self.center_point())

    def glide(self, point, **kwargs) -> Glide:
        return Glide(self, point, **kwargs)


def relabel_nucleus(atom: Atom, label: str) -> list[Animation]:
    """Animations (a list: unpack with ``*``) that rewrite the nucleus's charge."""
    old = atom.nucleus.label
    new = txt(label, cfg.FONT["tiny"], cfg.WHITE)
    fit_inside(new, atom.nucleus.ball.width * 0.81, atom.nucleus.ball.height * 0.52)
    new.move_to(atom.nucleus.ball)
    atom.nucleus.label = new
    if old is None:
        atom.nucleus.add(new)
        return [FadeIn(new)]
    atom.nucleus.remove(old)
    return [FadeThrough(old, new, parent=atom.nucleus)]


def pull_arrows(center, outer: float, strength: float, count: int = 8, inner: float | None = None,
                color: str = cfg.PULL_COLOR, phase: float = PI / 8) -> VGroup:
    """Inward gold arrows from the cloud's contour: the nucleus's pull.

    Thickness grows with ``strength`` (Slater's Z_eff, roughly 1 to 6).
    """
    center = np.asarray(center, dtype=float)
    inner = inner if inner is not None else max(outer * 0.6, outer - 0.75, 0.46)
    group = VGroup()
    width = 2.0 + 1.5 * strength
    for index in range(count):
        angle = phase + index * TAU / count
        direction = np.array([np.cos(angle), np.sin(angle), 0.0])
        group.add(Arrow(center + direction * (outer + 0.12), center + direction * inner, buff=0,
                        color=color, stroke_width=width, tip_length=0.12 + 0.025 * strength,
                        max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=40))
    return group


def symbol_label(symbol: str, size: int | None = None, color: str = cfg.WHITE) -> Text:
    return txt(symbol, size or cfg.FONT["section"], color)


def ion_tex(base: str, charge: str = "") -> str:
    """LaTeX for an ion such as Na^+, O^{2-}, with a proper minus sign."""
    return rf"\mathrm{{{base}}}" + (rf"^{{{charge}}}" if charge else "")


def escape_electron(start, end, color: str = cfg.ELECTRON_COLOR) -> tuple[VGroup, VMobject]:
    """A bright electron and the gently curved path it leaves along."""
    dot = glow_dot(start, 0.12, color)
    path = ArcBetweenPoints(np.asarray(start, dtype=float), np.asarray(end, dtype=float), angle=-PI / 5)
    return dot, path


# ----------------------------------------------------------------------------
# Energy: meters and level diagrams
# ----------------------------------------------------------------------------


class EnergyMeter(VGroup):
    """A vertical gauge that fills as energy is supplied (kJ/mol)."""

    def __init__(self, height: float = 5.0, width: float = 0.62, top: float = 2500,
                 ticks: Sequence[int] = (0, 500, 1000, 1500, 2000, 2500), color: str = cfg.GOLD,
                 label_side=LEFT) -> None:
        super().__init__()
        self.top, self.height_units, self.value = float(top), height, 0.0
        self.frame = RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=cfg.MUTED,
                                      stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.9)
        self.fill = Rectangle(width=width - 0.16, height=0.01, stroke_width=0, fill_opacity=0.95)
        self.fill.set_fill(color=[color, cfg.ORANGE])
        self.fill.set_sheen_direction(UP)
        self.tick_marks, self.tick_labels = VGroup(), VGroup()
        for value in ticks:
            y = self._y(value)
            self.tick_marks.add(Line([-width / 2 - 0.14, y, 0], [-width / 2, y, 0], stroke_color=cfg.MUTED, stroke_width=3))
            label = txt(f"{value}", cfg.FONT["tiny"], cfg.MUTED)
            label.next_to([-width / 2 - 0.16, y, 0], label_side, buff=0.12)
            self.tick_labels.add(label)
        self.add(self.frame, self.fill, self.tick_marks, self.tick_labels)
        self._bottom = self.frame.get_bottom() + UP * 0.08
        self.set_value(0)

    def _y(self, value: float) -> float:
        return -self.height_units / 2 + 0.08 + (self.height_units - 0.16) * value / self.top

    def set_value(self, value: float) -> None:
        self.value = float(value)
        h = max((self.height_units - 0.16) * self.value / self.top, 0.01)
        self.fill.stretch_to_fit_height(h)
        self.fill.move_to(self.frame.get_bottom() + UP * (0.08 + h / 2))

    def level_point(self, value: float) -> np.ndarray:
        return self.frame.get_bottom() + UP * (0.08 + (self.height_units - 0.16) * value / self.top)

    def fill_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.value, self.set_value, value, **kwargs)


def energy_level(y: float, x0: float, x1: float, color: str, label: str | None = None,
                 size: int | None = None) -> VGroup:
    """A glowing horizontal energy shelf with an equation label on its right."""
    shelf = glow_line([x0, y, 0], [x1, y, 0], color, 4)
    group = VGroup(shelf)
    group.shelf, group.label = shelf, None
    if label:
        tag = eq(label, size or cfg.FONT["label"], color).next_to(shelf, RIGHT, buff=0.3)
        group.add(tag)
        group.label = tag
    return group


# ----------------------------------------------------------------------------
# Graphs
# ----------------------------------------------------------------------------


def trend_axes(x_length: float, y_length: float, y_max: float, y_step: float, *, x_count: int,
               y_labels: bool = True, y_unit: str | None = None) -> Axes:
    """Plain axes in the house style; the scene writes its own x labels."""
    axes = Axes(
        x_range=[0, x_count + 1, 1], y_range=[0, y_max, y_step], x_length=x_length, y_length=y_length,
        tips=False, axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3, "include_ticks": False},
        y_axis_config={"include_ticks": True, "tick_size": 0.07},
    )
    grid = VGroup()
    for value in np.arange(y_step, y_max + 1e-6, y_step):
        grid.add(DashedLine(axes.c2p(0, value), axes.c2p(x_count + 1, value), stroke_color=cfg.MUTED,
                            stroke_width=1.5, stroke_opacity=0.35, dash_length=0.08))
    axes.grid = grid
    axes.add_to_back(grid)
    axes.y_tick_labels = VGroup()
    if y_labels:
        for value in np.arange(y_step, y_max + 1e-6, y_step):
            label = txt(f"{int(value)}", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(0, value), LEFT, buff=0.18)
            axes.y_tick_labels.add(label)
        axes.add(axes.y_tick_labels)
    return axes


def glow_polyline(points: Sequence[np.ndarray], color: str, width: float = 5) -> VGroup:
    """A straight-segment data line with a soft underglow."""
    under = VMobject(stroke_color=color, stroke_width=width * 3.4, stroke_opacity=0.15).set_points_as_corners(points)
    line = VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(points)
    group = VGroup(under, line)
    group.line = line
    return group


# ----------------------------------------------------------------------------
# Elements and the table (as in Part 3)
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
    tile.box, tile.z, tile.color_name, tile.symbol, tile.number = box, z, colour, None, None
    if symbol:
        label = Text(pm.symbol_of(z), font_size=48, color=cfg.WHITE, weight=BOLD)
        fit_inside(label.scale(size * 0.62 / max(label.height, 1e-6)), size * 0.74, size * 0.48)
        label.move_to(box).shift(DOWN * size * (0.06 if number else 0))
        label._tile_label = True
        tile.add(label)
        tile.symbol = label
    if number:
        tag = Text(str(z), font_size=48, color=cfg.MUTED, weight=BOLD)
        tag.scale(size * 0.2 / tag.height).move_to(box.get_corner(UL) + np.array([size * 0.2, -size * 0.16, 0]))
        tag.align_to(box.get_left() + RIGHT * size * 0.1, LEFT)
        tag._tile_label = True
        tile.add(tag)
        tile.number = tag
    return tile


TABLE_PITCH = 0.70
TABLE_CENTER = DOWN * 0.42


def table_point(z: int, layout: str = "standard", pitch: float = TABLE_PITCH, center=TABLE_CENTER) -> np.ndarray:
    """Where element ``z`` sits on screen. The row and column come from the model."""
    row, col = pm.position(z, layout)
    return grid_point(row, col, layout, pitch, center)


def grid_point(row: float, col: float, layout: str = "standard", pitch: float = TABLE_PITCH, center=TABLE_CENTER) -> np.ndarray:
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
    ``silhouette`` (no symbols, muted).
    """
    table = VGroup()
    table.tiles, table.layout, table.pitch, table.center = {}, layout, pitch, np.asarray(center, dtype=float)
    for z in zs or range(1, len(pm.SYMBOLS) + 1):
        colour = None if style == "block" else (cfg.CYAN if style == "plain" else cfg.MUTED)
        tile = element_tile(z, pitch * fill_ratio, colour, symbol=symbols and style != "silhouette",
                            fill=0.10 if style == "silhouette" else 0.18)
        tile.move_to(table_point(z, layout, pitch, center))
        table.add(tile)
        table.tiles[z] = tile
    return table


def tiles_of(table: VGroup, zs: Iterable[int]) -> VGroup:
    return VGroup(*[table.tiles[z] for z in zs if z in table.tiles])


def main_group_zs() -> list[int]:
    """Main-group elements of periods 1-6: the tiles every heat map colours."""
    return [z for z in range(1, 87)
            if pm.position(z)[1] in ed.MAIN_GROUP_COLUMNS and pm.position(z)[0] in ed.HEAT_MAP_PERIODS]


def recolor_tiles(tiles: Iterable[VGroup], color_for, fill: float = 0.22) -> list[Animation]:
    """Animations that re-outline tiles; ``color_for(z)`` picks each colour."""
    animations = []
    for tile in tiles:
        colour = color_for(tile.z)
        tint = interpolate_color(ManimColor(cfg.PANEL), ManimColor(colour), fill)
        animations.append(tile.box.animate.set_stroke(colour).set_fill(tint, 0.95))
    return animations


# ----------------------------------------------------------------------------
# Heat maps
# ----------------------------------------------------------------------------


def heat_fraction(prop: str, z: int) -> float | None:
    """Where an element's value sits on its property's scale (None: no value)."""
    symbol = pm.symbol_of(z)
    value = ed.property_value(prop, symbol)
    if value is None:
        return None
    low, high = ed.property_range(prop, [pm.symbol_of(k) for k in main_group_zs()])
    if prop == "electron_gain":
        low = 0.0
    return mu.unit_interval(value, low, high)


def heat_color(prop: str, z: int) -> str:
    """The cool-to-warm colour of one tile on one property's map."""
    if ed.is_exception(prop, pm.symbol_of(z)):
        return cfg.REQUIRED
    fraction = heat_fraction(prop, z)
    if fraction is None:
        return cfg.NO_DATA
    return mu.scale_color(fraction, cfg.HEAT_STOPS)


def heat_legend(low: str, high: str, width: float = 4.2, height: float = 0.32) -> VGroup:
    """A smooth colour bar with its two ends labelled."""
    steps = 24
    bar = VGroup(*[Rectangle(width=width / steps + 0.004, height=height, stroke_width=0,
                             fill_color=mu.scale_color(i / (steps - 1), cfg.HEAT_STOPS), fill_opacity=1)
                   for i in range(steps)]).arrange(RIGHT, buff=0)
    frame = RoundedRectangle(width=width + 0.08, height=height + 0.08, corner_radius=0.08,
                             stroke_color=cfg.MUTED, stroke_width=2, fill_opacity=0).move_to(bar)
    left = txt(low, cfg.FONT["tiny"], cfg.MUTED).next_to(bar, LEFT, buff=0.22)
    right = txt(high, cfg.FONT["tiny"], cfg.WHITE).next_to(bar, RIGHT, buff=0.22)
    group = VGroup(bar, frame, left, right)
    group.bar, group.low, group.high = bar, left, right
    return group


def tile_prism(point, size: float, height: float, color: str, opacity: float = 0.94) -> Prism:
    """An extruded element tile for the 3D skyline shots."""
    height = max(height, 0.02)
    prism = Prism(dimensions=[size, size, height], fill_color=color, fill_opacity=opacity,
                  stroke_color=interpolate_color(ManimColor(color), ManimColor(cfg.WHITE), 0.35),
                  stroke_width=0.6)
    prism.move_to(np.asarray(point, dtype=float) + OUT * height / 2)
    return prism


# ----------------------------------------------------------------------------
# Orbital boxes and spin arrows (as in Part 3)
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


# ----------------------------------------------------------------------------
# A hand-projected 3D crystal: shaded balls drawn back to front, turning
# ----------------------------------------------------------------------------


def shaded_ball(radius: float, color: str) -> VGroup:
    """A sphere-looking disc: radial sheen plus a small highlight."""
    body = Circle(radius=radius, stroke_color=interpolate_color(ManimColor(color), ManimColor(cfg.BG), 0.45),
                  stroke_width=1.5, fill_color=color, fill_opacity=1)
    body.set_sheen(-0.55, UL)
    shine = Circle(radius=radius * 0.28, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.55)
    shine.move_to(body.get_center() + UL * radius * 0.38)
    return VGroup(body, shine)


class ProjectedCrystal(_LiveMixin, VGroup):
    """Ions at 3D lattice sites, rotated and projected by hand each frame.

    Cheap in Cairo (no lit surfaces), and the balls are re-sorted by depth so
    near ions always cover far ones. Sizes are shrunk relative to the real
    lattice so the arrangement stays visible.
    """

    def __init__(self, sites: np.ndarray, kinds: Sequence[str], radii: dict[str, float],
                 colors: dict[str, str], spacing: float, center=ORIGIN, *, spin: float = 0.22,
                 tilt: float = 0.42, turn: float = 0.5, bonds: bool = True) -> None:
        super().__init__()
        self.sites = np.asarray(sites, dtype=float) * spacing
        self.kinds, self.spin, self.tilt, self.turn = list(kinds), spin, tilt, turn
        self.anchor = Dot(np.asarray(center, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0)
        self.balls = VGroup(*[shaded_ball(radii[k], colors[k]) for k in self.kinds])
        self._shapes = [[part.points.copy() for part in ball] for ball in self.balls]
        self._all_balls = list(self.balls.submobjects)
        for ball in self._all_balls:
            ball._crystal_home = ball.get_center().copy()
        self._pairs = []
        if bonds:
            for i in range(len(self.sites)):
                for j in range(i + 1, len(self.sites)):
                    if abs(np.linalg.norm(self.sites[i] - self.sites[j]) - spacing) < 1e-6:
                        self._pairs.append((i, j))
        self.bonds = VGroup(*[Line(ORIGIN, RIGHT, stroke_color=cfg.MUTED, stroke_width=2.5, stroke_opacity=0.45)
                              for _ in self._pairs])
        self.add(self.anchor, self.bonds, self.balls)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.turn += self.spin * dt
        self._place()

    def _place(self) -> None:
        centre = self.anchor.get_center()
        turned = mu.turn_and_tilt(self.sites, self.turn, self.tilt)
        sizes = mu.perspective(turned[:, 2], 14.0)
        projected = turned.copy()
        projected[:, 2] = 0
        projected += centre
        for ball, shapes, point, size in zip(self._all_balls, self._shapes, projected, sizes):
            home = ball._crystal_home
            for part, shape in zip(ball, shapes):
                part.points = (shape - home) * size + point
        for line, (i, j) in zip(self.bonds, self._pairs):
            line.put_start_and_end_on(projected[i], projected[j])
        # Draw far balls first so near ones cover them.
        self.balls.submobjects = [self._all_balls[i] for i in np.argsort(turned[:, 2])]


def rock_salt_sites(n: int = 1) -> tuple[np.ndarray, list[str]]:
    """Lattice sites of a (2n+1)^3 rock-salt block; even parity = cation."""
    sites, kinds = [], []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                sites.append((i, j, k))
                kinds.append("Na+" if (i + j + k) % 2 == 0 else "Cl-")
    return np.array(sites, dtype=float), kinds


# ----------------------------------------------------------------------------
# Closing card
# ----------------------------------------------------------------------------


def subscribe_card() -> VGroup:
    """The channel's closing card, in the house style."""
    thank_you = txt("THANK YOU FOR WATCHING", 40, cfg.CYAN)
    subscribe = Text("SUBSCRIBE", font_size=96, color=cfg.GOLD, weight=BOLD)
    subscribe.set_stroke("#351F05", width=3, opacity=0.75, background=True)
    rule = Line(LEFT * 3.4, RIGHT * 3.4, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(
        txt("Stay curious.", 44, cfg.WHITE),
        txt("Next: chemical bonding", 36, cfg.CYAN),
    ).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "ed", "np"]
