"""The one visual grammar the whole film speaks.

Every idea is drawn the same way from the first minute to the last, so the
closing synthesis reads as a conclusion rather than a new picture:

* a **nucleus** is a warm orange glowing ball (never to scale);
* **electron density** is a slowly turning cloud of cyan dots. Each dot is a
  seeded sample of a hydrogen-like radial density, so dense regions are more
  probable and the fringe is rare. When two atoms bond, the same dots flow
  from two round clouds into one shared cloud (``PairCloud``); a polar bond
  is a shared cloud that leans (``BondCloud``). These are schematic clouds,
  not computed molecular orbitals;
* **attraction** is teal, **repulsion** is red, both as lines between the
  particles that feel them;
* **energy** is gold: the curve E(r), the marker sliding along it, and every
  energy number;
* **energy released** is teal (a downward arrow), **energy required** is
  orange (an upward arrow);
* **ions**: positive purple, negative green, the same colours as the delta-plus
  and delta-minus ends of a polar bond;
* in 3D, **orbitals** are isosurfaces of simple LCAO densities from
  ``utils.bond_models``: sigma overlap blue, pi overlap purple (and rose for
  the second pi bond of N2);
* **ball-and-stick molecules** use smooth shaded spheres and cylindrical bonds
  projected from rigid 3D coordinates: oxygen red, carbon grey, hydrogen white.
  Atom radii favour readability; model bond lengths share one physical scale;
* a **metal** is a lattice of copper-coloured cores in a drifting electron sea.

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
from utils import bond_data as bd
from utils import bond_models as bm
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
    replacement back inside its group rather than leaving a floating label.
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
    new top-level entry, so members that already live inside a molecule are
    drawn twice — the second time on top of everything. The scene is taught
    to look through groups to the individual animations instead.
    """
    if getattr(scene, "_flattens_groups", False):
        return
    add_from = scene.add_mobjects_from_animations
    moving = scene.get_moving_mobjects
    scene.add_mobjects_from_animations = lambda animations: add_from(list(_leaf_animations(animations)))
    scene.get_moving_mobjects = lambda *animations: moving(*_leaf_animations(animations))
    partition = scene.get_moving_and_static_mobjects

    def live_surface_partition(animations):
        # Cairo normally freezes a flattened list of moving descendants at the
        # start of a play. Isosurface rebuilds its faces, so that list would keep
        # drawing detached OLD faces beside the current mesh during a morph.
        # Render scene roots for these plays; the camera then finds the current
        # faces on every frame. Other animations keep the normal static cache.
        # Some projected models also reorder children as their depth changes.
        # An explicitly marked model must retain its current draw tree.
        live_order = any(getattr(member, "_live_draw_order", False)
                         for root in scene.mobjects for member in root.get_family())
        if live_order or any(isinstance(animation.mobject, Isosurface)
                             for animation in _leaf_animations(animations)):
            return list(scene.mobjects), []
        return partition(animations)

    scene.get_moving_and_static_mobjects = live_surface_partition
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
    return ("−" if value < 0 else "+" if value > 0 else "") + text


def decorative(mob: Mobject) -> Mobject:
    """Mark a glow or shadow copy so the layout audit does not read it as text."""
    for member in mob.get_family():
        member._is_decorative = True
    return mob


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
    """The film's title: a big warm line and a smaller cyan one, with an
    outline, an offset shadow and a soft glow."""
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
    """A single, tracked particle: a bright bead with a halo."""
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
    """A bold arrow with a soft underglow — energy steps and big moves."""
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


def strike(mob: Mobject, color: str = cfg.RED, width: float = 7) -> Line:
    """A diagonal strike-through across anything."""
    return Line(mob.get_corner(DL) + LEFT * 0.1, mob.get_corner(UR) + RIGHT * 0.1, stroke_color=color, stroke_width=width)


# ----------------------------------------------------------------------------
# A generic tween, so live objects (clouds, meters) animate their own state
# ----------------------------------------------------------------------------


class Tween(Animation):
    """Animate ``setter(value)`` from ``getter()`` (read when the animation
    begins) to ``target``. Updaters keep running, so a cloud keeps turning
    while it changes."""

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


def track(tracker: ValueTracker, target: float, **kwargs) -> Tween:
    """Drive a ValueTracker without copying it (live followers stay in step)."""
    return Tween(tracker, tracker.get_value, tracker.set_value, target, **kwargs)


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


class Hold(Animation):
    """An animation that changes nothing: lets live objects run inside a play."""

    def __init__(self, mobject: Mobject | None = None, **kwargs) -> None:
        kwargs.setdefault("suspend_mobject_updating", False)
        super().__init__(mobject or Mobject(), **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        pass


# ----------------------------------------------------------------------------
# Electron clouds
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


class _DotBins:
    """Shared machinery: draw many small dots in a few depth bins (Cairo pays
    per mobject, so six bins draw ~10x faster than hundreds of Dots)."""

    BINS = 6

    def _setup_bins(self, color: str, dot_radius: float) -> None:
        self._shape = Circle(radius=dot_radius, num_components=5).points.copy()
        self._bin_opacity = np.linspace(0.3, 1.0, self.BINS)
        self.dots = VGroup(*[VMobject(fill_color=color, fill_opacity=o, stroke_width=0) for o in self._bin_opacity])

    def _draw_bins(self, positions: np.ndarray, fade: np.ndarray, level: float) -> None:
        everything = self._shape[None, :, :] + positions[:, None, :]
        which = np.clip(np.rint(mu.linear_map(fade, (0.28, 1.0), (0, self.BINS - 1))), 0, self.BINS - 1).astype(int)
        for index, (layer, opacity) in enumerate(zip(self.dots, self._bin_opacity)):
            chosen = everything[which == index]
            layer.points = chosen.reshape(-1, 3) if len(chosen) else np.zeros((0, 3))
            layer.fill_rgbas[:, 3] = opacity * level  # direct write: set_fill is 20x slower


class ElectronCloud(_LiveMixin, _DotBins, VGroup):
    """A seeded, slowly turning 3D sample of where an electron is likely to be.

    The radial distribution has about 90 % of its probability within
    ``radius``. Change the size with ``resize`` and the brightness with
    ``fade_to``; move it by shifting (or Glide), never ``scale``.
    """

    def __init__(self, radius: float, center=ORIGIN, *, count: int = 220, seed: int = 0,
                 color: str = cfg.ELECTRON_COLOR, dot_radius: float = 0.03, spin: float = 0.3,
                 tilt: float = 0.38, glow: float = 0.15, phase: float = 0.0) -> None:
        super().__init__()
        self.unit = pm.cloud_samples(count, cfg.SEED + 7919 * seed)
        self.radius, self.level = float(radius), 1.0
        self.turn, self.spin, self.tilt, self.colour = phase, spin, tilt, color
        self.anchor = Dot(np.asarray(center, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0)
        self.glow = soft_glow(color, peak_opacity=glow) if glow else VGroup()
        self._glow_base = [float(m.get_fill_opacity()) for m in self.glow]
        self._setup_bins(color, dot_radius)
        self.add(self.anchor, self.glow, self.dots)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

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

    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.turn += self.spin * dt
        self._place()

    def _place(self) -> None:
        centre = self.center_point()
        turned = mu.turn_and_tilt(self.unit, self.turn, self.tilt)
        fade = mu.depth_fade(turned[:, 2], pm.CLOUD_REACH)
        offsets = turned * self.radius
        offsets[:, 2] = 0.0
        self._draw_bins(offsets + centre, fade, self.level)
        if len(self.glow):
            self.glow.set_width(2 * GLOW_REACH * self.radius).move_to(centre)
            for disc, base in zip(self.glow, self._glow_base):
                disc.set_fill(opacity=base * min(self.level, 1.0), family=False)


class PairCloud(_LiveMixin, _DotBins, VGroup):
    """Two one-electron atoms whose dots flow into one shared bonding cloud.

    ``share`` 0: two round clouds, one electron each. ``share`` 1: the bonded
    pair, its density gathered between and around both nuclei. The same seeded
    dots move continuously between the two pictures, so the viewer sees the
    electrons rearrange rather than one drawing replace another. ``lean``
    (-1..1) slides the shared density toward the left or right nucleus. It is
    an illustration of electron sharing, not a computed molecular orbital.
    """

    def __init__(self, left, right, radius: float, *, count: int = 460, seed: int = 0,
                 color: str = cfg.ELECTRON_COLOR, dot_radius: float = 0.03, spin: float = 0.35,
                 tilt: float = 0.35, glow: float = 0.14, share: float = 0.0, lean: float = 0.0) -> None:
        super().__init__()
        self.unit = pm.cloud_samples(count, cfg.SEED + 7919 * seed + 31)
        self.owner = np.arange(count) % 2          # 0 = left atom's electron, 1 = right atom's
        self.radius, self.share, self.lean, self.level = float(radius), float(share), float(lean), 1.0
        self.turn, self.spin, self.tilt = 0.0, spin, tilt
        self.ends = VGroup(Dot(np.asarray(left, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0),
                           Dot(np.asarray(right, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0))
        self.glows = VGroup(*[soft_glow(color, peak_opacity=glow) for _ in range(3)]) if glow else VGroup()
        self._glow_base = [[float(m.get_fill_opacity()) for m in g] for g in self.glows]
        self._setup_bins(color, dot_radius)
        self.add(self.ends, self.glows, self.dots)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    # -- state ------------------------------------------------------------
    def center_point(self) -> np.ndarray:
        return (self.ends[0].get_center() + self.ends[1].get_center()) / 2

    def set_ends(self, left, right) -> None:
        self.ends[0].move_to(np.asarray(left, dtype=float))
        self.ends[1].move_to(np.asarray(right, dtype=float))
        self._place()

    def set_share(self, value: float) -> None:
        self.share = float(np.clip(value, 0, 1))
        self._place()

    def set_lean(self, value: float) -> None:
        self.lean = float(np.clip(value, -1, 1))
        self._place()

    def set_level(self, value: float) -> None:
        self.level = max(float(value), 0.0)
        self._place()

    def set_radius(self, value: float) -> None:
        self.radius = max(float(value), 1e-3)
        self._place()

    def resize_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.radius, self.set_radius, value, **kwargs)

    def share_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.share, self.set_share, value, **kwargs)

    def lean_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.lean, self.set_lean, value, **kwargs)

    def fade_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.level, self.set_level, value, **kwargs)

    def glide(self, point, **kwargs) -> Glide:
        return Glide(self, point, **kwargs)

    # -- drawing ------------------------------------------------------------
    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.turn += self.spin * dt
        self._place()

    def _place(self) -> None:
        a, b = self.ends[0].get_center(), self.ends[1].get_center()
        mid = (a + b) / 2
        half = max(abs(b[0] - a[0]) / 2, 1e-3)
        s = smooth(self.share)
        lean = self.lean
        turned = mu.turn_and_tilt(self.unit, self.turn, self.tilt)
        fade = mu.depth_fade(turned[:, 2], pm.CLOUD_REACH)
        flat = turned.copy()
        flat[:, 2] = 0.0
        homes = np.where(self.owner[:, None] == 0, a, b)
        # A leaning bond shrinks the giver's share of the cloud and swells the taker's.
        own_scale = np.where(self.owner == 0, 1 - 0.35 * max(lean, 0), 1 - 0.35 * max(-lean, 0))
        atomic = homes + flat * self.radius
        centre = mid + RIGHT * lean * half * 0.85
        ellipsoid = centre + flat * np.array([half * (1 - 0.45 * abs(lean)) + 0.72 * self.radius,
                                              0.8 * self.radius, 0.0])
        taker = np.where(lean >= 0, b, a)
        contracted = np.where(np.abs(lean) > 1e-6,
                              homes + (taker - homes) * abs(lean) * 0.9 + flat * self.radius * own_scale[:, None] * 0.85,
                              homes + flat * self.radius * 0.85)
        bonded = 0.4 * contracted + 0.6 * ellipsoid
        positions = atomic + (bonded - atomic) * s
        self._draw_bins(positions, fade, self.level)
        if len(self.glows):
            spots = (a, b, centre)
            widths = (2 * GLOW_REACH * self.radius, 2 * GLOW_REACH * self.radius,
                      2 * GLOW_REACH * (half + 0.7 * self.radius))
            weights = (1 - 0.6 * s, 1 - 0.6 * s, s)
            for glow, base, spot, width, weight in zip(self.glows, self._glow_base, spots, widths, weights):
                tall = 2 * GLOW_REACH * self.radius * (0.85 if glow is self.glows[2] else 1.0)
                glow.stretch_to_fit_width(width).stretch_to_fit_height(tall).move_to(spot)
                for disc, value in zip(glow, base):
                    disc.set_fill(opacity=value * weight * min(self.level, 1.0), family=False)


class BondCloud(_LiveMixin, _DotBins, VGroup):
    """The shared pair of a horizontal bond: a seeded dot cloud stretched
    between two nuclei, turning about the bond axis.

    ``lean`` runs from -1 (all toward the left atom) through 0 (even sharing)
    to +1 (all toward the right atom); the cloud slides and tightens toward
    the stronger puller. An illustration of unequal sharing, not a computed
    molecular orbital.
    """

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
        self._setup_bins(color, dot_radius)
        self.add(self.ends, self.glow, self.dots)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    def center_point(self) -> np.ndarray:
        return (self.ends[0].get_center() + self.ends[1].get_center()) / 2

    def set_lean(self, lean: float) -> None:
        self.lean = float(np.clip(lean, -1, 1))
        self._place()

    def lean_to(self, lean: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.lean, self.set_lean, lean, **kwargs)

    def set_level(self, level: float) -> None:
        self.level = max(float(level), 0.0)
        self._place()

    def fade_to(self, level: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.level, self.set_level, level, **kwargs)

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
        self._draw_bins(offsets + self.centre(), fade, self.level)
        if len(self.glow):
            self.glow.stretch_to_fit_width(2 * GLOW_REACH * sx).stretch_to_fit_height(2 * GLOW_REACH * sy)
            self.glow.move_to(self.centre())
            for disc, base in zip(self.glow, self._glow_base):
                disc.set_fill(opacity=base * min(self.level, 1.0), family=False)


def nucleus_core(label: str | None, radius: float = 0.24, color: str = cfg.NUCLEUS_COLOR,
                 size: int | None = None, *, polished: bool = False) -> VGroup:
    """A glowing warm nucleus with its charge written on it (not to scale)."""
    glow = halo(radius * 2.6, color, layers=6, peak_opacity=0.24)
    if polished:
        ball = polished_ball(radius, color)
    else:
        ball = Circle(radius=radius, stroke_color=interpolate_color(ManimColor(color), ManimColor(cfg.WHITE), 0.4),
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
    """Nucleus, optional gray core cloud, and the cyan outer cloud."""

    def __init__(self, radius: float, center=ORIGIN, *, charge: str | None = None,
                 core: float | None = None, count: int = 220, core_count: int = 120, seed: int = 0,
                 nucleus_radius: float = 0.24, color: str = cfg.ELECTRON_COLOR,
                 dot_radius: float = 0.03, glow: float = 0.15, label_size: int | None = None) -> None:
        super().__init__()
        center = np.asarray(center, dtype=float)
        self.cloud = ElectronCloud(radius, center, count=count, seed=seed, color=color,
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


def follow(mob: Mobject, where: Callable[[], np.ndarray]) -> Mobject:
    """Keep ``mob`` centred on a moving point (a nucleus riding a tracker)."""
    mob.add_updater(lambda m: m.move_to(where()))
    return mob


def bind_pair(cloud: "PairCloud", separation: Callable[[], float], center=ORIGIN) -> "PairCloud":
    """Make a PairCloud's two nuclei sit at +/- separation/2 around ``center`` every frame.

    ``center`` may be a point or a callable returning one (to move the molecule).

    The updater runs first, so the cloud redraws around the new positions in
    the same frame.
    """
    where = center if callable(center) else (lambda: center)

    def update(m: Mobject) -> None:
        half = separation() / 2
        middle = np.asarray(where(), dtype=float)
        m.ends[0].move_to(middle + LEFT * half)
        m.ends[1].move_to(middle + RIGHT * half)

    cloud.add_updater(update, index=0)
    update(cloud)
    cloud._place()
    return cloud


def pair_nuclei(cloud: "PairCloud", labels: tuple[str | None, str | None] = ("+", "+"), radius: float = 0.22,
                *, polished: bool = False) -> VGroup:
    """Two nuclei that ride a PairCloud's ends (add the cloud to the scene first)."""
    nuclei = VGroup()
    for index, label in enumerate(labels):
        core = nucleus_core(label, radius, polished=polished).move_to(cloud.ends[index].get_center())
        core.add_updater(lambda m, i=index: m.move_to(cloud.ends[i].get_center()))
        nuclei.add(core)
    return nuclei


def force_line(a: Callable[[], np.ndarray], b: Callable[[], np.ndarray], color: str, *, width: float = 5,
               dashed: bool = False, buff: float = 0.2, strength: Callable[[float], float] | None = None,
               thickness: Callable[[float], float] | None = None) -> VMobject:
    """A live line between two moving particles: teal for attraction, red (dashed) for repulsion.

    ``strength(distance)`` (0..1) sets the opacity and ``thickness(distance)``
    the width, so an interaction can fade with distance or swell up close.
    ``line.gain`` scales the opacity; tween it with ``line_gain``.
    """

    def ends() -> tuple[np.ndarray, np.ndarray, float]:
        start, end = np.asarray(a(), dtype=float), np.asarray(b(), dtype=float)
        length = float(np.linalg.norm(end - start))
        if length < 2 * buff + 0.02:
            middle = (start + end) / 2
            return middle + LEFT * 0.01, middle + RIGHT * 0.01, length
        unit = (end - start) / length
        return start + unit * buff, end - unit * buff, length

    def build() -> VMobject:
        start, end, length = ends()
        w = thickness(length) if thickness else width
        if dashed:
            line = DashedLine(start, end, stroke_color=color, stroke_width=w, dash_length=0.13, dashed_ratio=0.55)
        else:
            line = Line(start, end, stroke_color=color, stroke_width=w)
        return line

    line = build()
    line.gain = 1.0

    def refresh(m: VMobject) -> None:
        start, end, length = ends()
        if dashed:
            m.become(build())
        else:
            m.put_start_and_end_on(start, end)
            if thickness:
                m.set_stroke(width=thickness(length))
        level = strength(length) if strength else 1.0
        m.set_stroke(opacity=float(np.clip(level, 0, 1)) * m.gain)

    line.add_updater(refresh)
    refresh(line)
    return line


def line_gain(line: VMobject, value: float, **kwargs) -> Tween:
    """Fade a live force line in or out without fighting its updater."""
    def setter(v: float) -> None:
        line.gain = v
    return Tween(line, lambda: line.gain, setter, value, **kwargs)


# ----------------------------------------------------------------------------
# Energy: the curve, its marker, and level diagrams
# ----------------------------------------------------------------------------


H2 = (bd.BOND_ENTHALPY_KJ["H-H"], bd.BOND_LENGTH_PM["H-H"], bd.MORSE_A_PER_PM["H-H"])


class EnergyPlot(VGroup):
    """Energy against separation for one bond (a Morse model of the measured bond).

    The x axis of ``Axes`` sits at E = 0 — the separated atoms — and the
    distance tick labels live along the bottom edge, clear of the valley.
    """

    def __init__(self, depth: float = H2[0], r_e: float = H2[1], a: float = H2[2], *,
                 r_max: float = 320, e_min: float = -600, e_max: float = 500, x_length: float = 11.0,
                 y_length: float = 4.4, x_step: float = 100, y_step: float = 200, center=DOWN * 1.4,
                 color: str = cfg.ENERGY, labels: bool = True, curve: bool = True) -> None:
        super().__init__()
        self.well_depth, self.r_e, self.a, self.e_min, self.e_max, self.r_max = depth, r_e, a, e_min, e_max, r_max
        self.axes = Axes(
            x_range=[0, r_max, x_step], y_range=[e_min, e_max, y_step], x_length=x_length, y_length=y_length,
            tips=False, axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3, "include_ticks": False},
        )
        self.axes.move_to(center)
        self.frame_lines = VGroup(
            Line(self.axes.c2p(0, e_min), self.axes.c2p(r_max, e_min), stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5),
        )
        self.add(self.axes, self.frame_lines)
        self.labels = VGroup()
        if labels:
            for r in np.arange(x_step, r_max + 1e-6, x_step):
                tick = Line(self.axes.c2p(r, e_min), self.axes.c2p(r, e_min) + DOWN * 0.1, stroke_color=cfg.MUTED, stroke_width=2)
                label = txt(f"{int(r)}", cfg.FONT["tiny"], cfg.MUTED).next_to(tick, DOWN, buff=0.08)
                self.labels.add(tick, label)
            for value in np.arange(np.ceil(e_min / y_step) * y_step, e_max + 1e-6, y_step):
                if value == 0:
                    text = "0"
                else:
                    text = signed(value)
                label = txt(text, cfg.FONT["tiny"], cfg.MUTED).next_to(self.axes.c2p(0, value), LEFT, buff=0.14)
                self.labels.add(label)
            self.x_title = VGroup(eq("r", cfg.FONT["label"], cfg.WHITE), txt("pm", cfg.FONT["tiny"], cfg.MUTED)).arrange(RIGHT, buff=0.14)
            self.x_title.next_to(self.axes.c2p(r_max, e_min), RIGHT, buff=0.3)
            self.y_title = VGroup(eq("E", cfg.FONT["label"], cfg.ENERGY), txt("kJ/mol", cfg.FONT["tiny"], cfg.MUTED)).arrange(RIGHT, buff=0.16)
            self.y_title.next_to(self.axes.c2p(0, e_max), RIGHT, buff=0.25)
            self.labels.add(self.x_title, self.y_title)
            self.add(self.labels)
        self.curve = self.energy_curve(color) if curve else VGroup()
        self.add(self.curve)

    # -- model ---------------------------------------------------------------
    def energy(self, r: float) -> float:
        return float(bm.morse(r, self.well_depth, self.r_e, self.a))

    def r_clip(self) -> float:
        return bm.morse_inverse(self.e_max, self.well_depth, self.r_e, self.a)

    def point(self, r: float) -> np.ndarray:
        return self.axes.c2p(r, float(np.clip(self.energy(r), self.e_min, self.e_max)))

    def energy_curve(self, color: str, width: float = 6) -> VGroup:
        start = max(self.r_clip(), 1.0)
        line = self.axes.plot(lambda r: self.energy(r), x_range=[start, self.r_max, 0.5],
                              color=color, stroke_width=width, use_smoothing=False)
        under = line.copy().set_stroke(color, width=width * 3.4, opacity=0.16)
        group = VGroup(under, line)
        group.line = line
        return group

    def term_curve(self, which: str, color: str, width: float = 5) -> VGroup:
        """One of the two Morse terms ('push' or 'pull'), clipped to the plot."""
        def value(r):
            push, pull = bm.morse_terms(r, self.well_depth, self.r_e, self.a)
            return float(push if which == "push" else pull)

        rs = np.linspace(1, self.r_max, 800)
        values = np.array([value(r) for r in rs])
        keep = (values <= self.e_max) & (values >= self.e_min)
        rs = rs[keep]
        line = self.axes.plot(value, x_range=[rs[0], rs[-1], 0.5], color=color, stroke_width=width, use_smoothing=False)
        under = line.copy().set_stroke(color, width=width * 3, opacity=0.14)
        return VGroup(under, line)

    def marker(self, tracker: ValueTracker, color: str = cfg.ENERGY, radius: float = 0.13) -> VGroup:
        """The gold dot riding the curve at the tracker's separation."""
        dot = glow_dot(self.point(tracker.get_value()), radius, color)
        dot.add_updater(lambda m: m.move_to(self.point(tracker.get_value())))
        return dot

    def minimum_marks(self, color: str = cfg.WHITE) -> VGroup:
        base = self.axes.c2p(self.r_e, self.e_min)
        bottom = self.axes.c2p(self.r_e, -self.well_depth)
        drop = DashedLine(bottom, base, stroke_color=color, stroke_width=3, dash_length=0.1)
        return drop

    def depth_arrow(self, color: str = cfg.ENERGY) -> VGroup:
        """A double arrow from the valley floor up to zero (the bond energy)."""
        x = self.r_e + 26
        top, bottom = self.axes.c2p(x, 0), self.axes.c2p(x, -self.well_depth)
        return DoubleArrow(bottom, top, buff=0.02, color=color, stroke_width=6, tip_length=0.22,
                           max_tip_length_to_length_ratio=0.2)


def level_shelf(y: float, x0: float, x1: float, color: str, label: str | None = None, *,
                size: int | None = None, side=RIGHT, tex: bool = True) -> VGroup:
    """A glowing horizontal energy shelf with a label beside it."""
    shelf = glow_line([x0, y, 0], [x1, y, 0], color, 4)
    group = VGroup(shelf)
    group.shelf, group.label = shelf, None
    if label:
        tag = (eq(label, size or cfg.FONT["small"], color) if tex else txt(label, size or cfg.FONT["small"], color))
        tag.next_to(shelf, side, buff=0.25)
        group.add(tag)
        group.label = tag
    return group


def energy_step(x: float, y0: float, y1: float, color: str, label: str, *, side=RIGHT,
                size: int | None = None) -> VGroup:
    """An up (required) or down (released) energy arrow with its number."""
    arrow = glow_arrow([x, y0, 0], [x, y1, 0], color, 7, tip=0.26)
    tag = txt(label, size or cfg.FONT["small"], color).next_to(arrow, side, buff=0.18)
    group = VGroup(arrow, tag)
    group.arrow, group.tag = arrow, tag
    return group


# ----------------------------------------------------------------------------
# Lewis structures
# ----------------------------------------------------------------------------

LEWIS_DOT = 0.075
LEWIS_GAP = 0.15          # half-spacing of the two dots in a pair


def e_dot(point=ORIGIN, color: str = cfg.ELECTRON_COLOR, radius: float = LEWIS_DOT) -> VGroup:
    """One valence electron in a Lewis drawing: a small bright bead."""
    core = Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=1)
    glow = Circle(radius=radius * 2.1, stroke_width=0, fill_color=color, fill_opacity=0.18)
    return VGroup(glow, core).move_to(point)


_SIDES = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}


class LewisAtom(VGroup):
    """An element symbol with its valence electrons as dots on four sides.

    ``layout`` maps a side ('up', 'down', 'left', 'right') to 1, 2 or 3 dots.
    ``self.slots[side]`` holds those dots, so a scene can move exactly the
    electrons that pair up into a bond.
    """

    def __init__(self, symbol: str, layout: dict[str, int], *, color: str = cfg.WHITE, size: int = 72,
                 dot_color: str = cfg.ELECTRON_COLOR, center=ORIGIN, reach: float = 0.2) -> None:
        super().__init__()
        self.symbol = txt(symbol, size, color).move_to(center)
        self.reach, self.dot_color = reach, dot_color
        self.slots: dict[str, VGroup] = {}
        self.add(self.symbol)
        for side, count in layout.items():
            dots = VGroup(*[e_dot(p, dot_color) for p in self.side_points(side, count)])
            self.slots[side] = dots
            self.add(dots)

    def side_points(self, side: str, count: int) -> list[np.ndarray]:
        centre = self.symbol.get_center()
        w, h = self.symbol.width / 2 + self.reach, self.symbol.height / 2 + self.reach
        direction = _SIDES[side]
        base = centre + np.array([direction[0] * w, direction[1] * h, 0])
        along = RIGHT if side in ("up", "down") else UP
        offsets = {1: [0.0], 2: [LEWIS_GAP, -LEWIS_GAP], 3: [2 * LEWIS_GAP, 0.0, -2 * LEWIS_GAP]}[count]
        return [base + along * o for o in offsets]

    def all_dots(self) -> VGroup:
        return VGroup(*[d for dots in self.slots.values() for d in dots])


def pair_targets(left: Mobject, right: Mobject, pairs: int, column_gap: float = 0.3) -> list[list[np.ndarray]]:
    """Where k shared pairs sit between two symbols: k columns of two stacked dots."""
    mid = (left.get_right() + right.get_left()) / 2
    columns = []
    for j in range(pairs):
        x = (j - (pairs - 1) / 2) * column_gap
        columns.append([mid + RIGHT * x + UP * LEWIS_GAP, mid + RIGHT * x + DOWN * LEWIS_GAP])
    return columns


def bond_lines(left: Mobject, right: Mobject, order: int, color: str = cfg.WHITE, gap: float = 0.17,
               width: float = 7) -> VGroup:
    """The line form of a bond: one, two or three strokes between the symbols."""
    start, end = left.get_right() + RIGHT * 0.14, right.get_left() + LEFT * 0.14
    lines = VGroup()
    for j in range(order):
        y = (j - (order - 1) / 2) * gap
        lines.add(Line(start + UP * y, end + UP * y, stroke_color=color, stroke_width=width))
    return lines


def octet_ring(atom: Mobject, radius: float, color: str = cfg.GREEN, shift=ORIGIN) -> VMobject:
    """A dashed ring that encloses the electrons an atom 'counts'."""
    ring = Circle(radius=radius, stroke_color=color, stroke_width=3.5, stroke_opacity=0.9)
    return DashedVMobject(ring, num_dashes=40, dashed_ratio=0.55).move_to(atom.get_center() + shift)


# ----------------------------------------------------------------------------
# Ionic crystals: shaded balls, hand-projected in 3D, drawn back to front
# ----------------------------------------------------------------------------


ION_COLORS = {"+": cfg.CATION, "-": cfg.ANION}


def shaded_ball(radius: float, color: str) -> VGroup:
    """A sphere-looking disc: radial sheen plus a small highlight."""
    body = Circle(radius=radius, stroke_color=interpolate_color(ManimColor(color), ManimColor(cfg.BG), 0.45),
                  stroke_width=1.5, fill_color=color, fill_opacity=1)
    body.set_sheen(-0.55, UL)
    shine = Circle(radius=radius * 0.28, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.55)
    shine.move_to(body.get_center() + UL * radius * 0.38)
    return VGroup(body, shine)


def polished_ball(radius: float, color: str, *, layers: int = 64) -> VGroup:
    """Smooth sphere shading in vectors, with no visible tessellation grid.

    Nested colour contours and a soft reflection give a round, lit appearance
    while preserving the flat camera and light rendering cost of the ledger.
    """
    color = ManimColor(color)
    dark = ManimColor(color.to_rgb() * 0.23)
    ball = VGroup(Circle(radius=radius, fill_color=dark, fill_opacity=1, stroke_width=0))
    for fraction in np.linspace(0.992, 0.025, layers):
        brightness = 0.25 + 0.75 * np.sqrt(1 - fraction * fraction)
        contour = Circle(radius=radius * fraction, stroke_width=0,
                         fill_color=ManimColor(color.to_rgb() * brightness), fill_opacity=1)
        contour.shift(UL * radius * 0.34 * (1 - fraction))
        ball.add(contour)
    # Feather the reflection instead of adding a hard white dot.
    for fraction in np.linspace(1, 0.05, 16):
        reflection = Circle(radius=radius * 0.28 * fraction, stroke_width=0,
                            fill_color=cfg.WHITE, fill_opacity=0.065 * (1 - fraction))
        reflection.shift(UL * radius * 0.33)
        ball.add(reflection)
    return ball


def ion_ball(kind: str, radius: float, sign_size: int | None = None, *, polished: bool = False) -> VGroup:
    """An ion with its whole-ion charge; optionally use smooth sphere shading."""
    ball = (polished_ball if polished else shaded_ball)(radius, ION_COLORS[kind])
    sign = txt("+" if kind == "+" else "−", sign_size or cfg.FONT["small"], cfg.WHITE)
    sign.move_to(ball)
    return VGroup(ball, sign)


class ProjectedMolecule(VGroup):
    """A perspective ball-and-stick model driven by rigid 3D coordinates.

    Smooth shaded atom billboards avoid a faceted surface grid. Bonds use
    layered cylindrical strokes; depth and projected atom sizes change during
    genuine 3D rotations. Local sites stay fixed, preserving lengths/angles.
    """

    def __init__(self, sites: np.ndarray, symbols: Sequence[str], bonds: Sequence[tuple[int, int, int]],
                 radii: dict[str, float], colors: dict[str, str], center=ORIGIN,
                 *, yaw: float = 0.0, tilt: float = 0.0) -> None:
        super().__init__()
        self.sites = np.asarray(sites, dtype=float).copy()
        self.symbols = list(symbols)
        self.yaw, self.tilt = float(yaw), float(tilt)
        self.anchor = Dot(np.asarray(center, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0)
        self.atoms = VGroup(*[polished_ball(radii[symbol], colors[symbol]) for symbol in symbols])
        self._all_atoms = list(self.atoms)
        self._shapes = [[part.points.copy() for part in atom] for atom in self._all_atoms]
        self.rods = VGroup()
        self._rod_sites = []
        self._rod_widths = []
        for a, b, order in bonds:
            direction = self.sites[b] - self.sites[a]
            side = np.cross(OUT, direction)
            side /= max(np.linalg.norm(side), 1e-9)
            for offset in ((-0.11, 0.11) if order == 2 else (0.0,)):
                self._rod_sites.append(np.array([self.sites[a] + side * offset, self.sites[b] + side * offset]))
                width = 11 if order == 2 else 17
                widths = np.linspace(width, width * 0.18, 9)
                rod = VGroup(*[Line(LEFT, RIGHT, stroke_width=float(w),
                                    stroke_color=interpolate_color(ManimColor("#354858"), ManimColor("#E1EDF5"), k / 8))
                               for k, w in enumerate(widths)])
                self.rods.add(rod)
                self._rod_widths.append(widths)
        self._live_draw_order = True
        self.add(self.anchor, self.rods, self.atoms)
        self._place()

    def _project(self, points):
        rotation = mu.rotation_x(self.tilt) @ mu.rotation_y(self.yaw)
        turned = np.asarray(points, dtype=float) @ rotation.T
        sizes = mu.perspective(turned[:, 2], 12.0)
        screen = turned * sizes[:, None]
        screen[:, 2] = 0
        return screen + self.anchor.get_center(), sizes, turned[:, 2]

    def _place(self) -> None:
        self.projected_sites, sizes, depths = self._project(self.sites)
        for atom, shapes, center, size in zip(self._all_atoms, self._shapes, self.projected_sites, sizes):
            for part, shape in zip(atom, shapes):
                part.points = shape * size + center
        for rod, sites, widths in zip(self.rods, self._rod_sites, self._rod_widths):
            points, sizes, _ = self._project(sites)
            for stroke, width in zip(rod, widths):
                stroke.put_start_and_end_on(*points)
                stroke.set_stroke(width=float(width * sizes.mean()))
        self.atoms.submobjects = [self._all_atoms[i] for i in np.argsort(depths)]

    def set_pose(self, yaw: float, tilt: float) -> None:
        self.yaw, self.tilt = float(yaw), float(tilt)
        self._place()

    def pose_to(self, yaw: float, tilt: float, **kwargs) -> Animation:
        first_yaw, first_tilt = self.yaw, self.tilt
        return UpdateFromAlphaFunc(self, lambda m, a: m.set_pose(
            interpolate(first_yaw, yaw, a), interpolate(first_tilt, tilt, a)), **kwargs)


class ProjectedCrystal(_LiveMixin, VGroup):
    """Ions at 3D lattice sites, rotated and projected by hand each frame.

    Cheap in Cairo (no lit surfaces), and the balls are re-sorted by depth so
    near ions always cover far ones. Sizes are shrunk relative to the real
    lattice so the arrangement stays visible. ``assembly`` (0..1) flies every
    ion in from outside, in a staggered wave; ``highlight`` dims all but a
    chosen set; ``links`` are live lines from one site to others.
    """

    def __init__(self, sites: np.ndarray, kinds: Sequence[str], radii: dict[str, float],
                 colors: dict[str, str], spacing: float, center=ORIGIN, *, spin: float = 0.22,
                 tilt: float = 0.42, turn: float = 0.5, bonds: bool = True, assembly: float = 1.0,
                 polished: bool = False) -> None:
        super().__init__()
        self.sites = np.asarray(sites, dtype=float) * spacing
        self.kinds, self.spin, self.tilt, self.turn = list(kinds), spin, tilt, turn
        self.spacing, self.assembly = spacing, float(assembly)
        self.anchor = Dot(np.asarray(center, dtype=float), radius=0.002, fill_opacity=0, stroke_width=0)
        # Small lattice ions need fewer diffuse contours than large atom
        # close-ups; retain the same soft reflection and colour palette.
        make_ball = (lambda r, c: polished_ball(r, c, layers=32)) if polished else shaded_ball
        self.balls = VGroup(*[make_ball(radii[k], colors[k]) for k in self.kinds])
        # Effective contour overlap, tuned to retain a faint lattice context
        # at the scene's 12% dim setting even in Cairo's 8-bit alpha output.
        self._opacity_layers = 8 if polished else 1
        self._shapes = [[part.points.copy() for part in ball] for ball in self.balls]
        self._all_balls = list(self.balls.submobjects)
        self._base_opacity = [[float(part.get_fill_opacity()) for part in ball] for ball in self._all_balls]
        for ball in self._all_balls:
            ball._crystal_home = ball.get_center().copy()
        distance = np.linalg.norm(self.sites, axis=1)
        self._delay = 0.6 * distance / max(distance.max(), 1e-6)
        self._dim = np.ones(len(self.sites))
        self._pairs = []
        if bonds:
            for i in range(len(self.sites)):
                for j in range(i + 1, len(self.sites)):
                    if abs(np.linalg.norm(self.sites[i] - self.sites[j]) - spacing) < 1e-6:
                        self._pairs.append((i, j))
        self.bonds = VGroup(*[Line(ORIGIN, RIGHT, stroke_color=cfg.MUTED, stroke_width=2.5, stroke_opacity=0.45)
                              for _ in self._pairs])
        self._links: list[tuple[int, int]] = []
        self.links = VGroup()
        self.add(self.anchor, self.bonds, self.links, self.balls)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    def center_point(self) -> np.ndarray:
        return self.anchor.get_center()

    def set_assembly(self, value: float) -> None:
        self.assembly = float(np.clip(value, 0, 1))
        self._place()

    def assemble(self, value: float = 1.0, **kwargs) -> Tween:
        return Tween(self, lambda: self.assembly, self.set_assembly, value, **kwargs)

    def set_highlight(self, keep: Iterable[int] | None, dim: float = 0.18) -> None:
        self._dim = np.ones(len(self.sites)) if keep is None else np.full(len(self.sites), dim)
        if keep is not None:
            self._dim[list(keep)] = 1.0
        self._place()

    def set_links(self, pairs: Sequence[tuple[int, int]], color: str, width: float = 5, dashed: bool = False) -> None:
        self._links = list(pairs)
        lines = [Line(ORIGIN, RIGHT, stroke_color=color, stroke_width=width) for _ in self._links]
        self.links.submobjects = lines
        self._link_dashed = dashed
        self._place()

    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.turn += self.spin * dt
        self._place()

    def _local(self) -> np.ndarray:
        return np.clip((self.assembly - self._delay) / 0.4, 0, 1)

    def _place(self) -> None:
        centre = self.anchor.get_center()
        local = self._local()
        eased = local * local * (3 - 2 * local)
        positions = self.sites * (1 + (1 - eased)[:, None] * 3.2)
        turned = mu.turn_and_tilt(positions, self.turn, self.tilt)
        sizes = mu.perspective(turned[:, 2], 14.0)
        projected = turned.copy()
        projected[:, 2] = 0
        projected += centre
        for index, (ball, shapes, point, size) in enumerate(zip(self._all_balls, self._shapes, projected, sizes)):
            home = ball._crystal_home
            visible = eased[index] * self._dim[index]
            # Nested translucent contours otherwise accumulate almost opaque
            # even when a background ion should be faint. Compensate for the
            # effective contour overlap; fully visible ions keep their shading.
            if self._opacity_layers > 1:
                visible = 1 - (1 - visible) ** (1 / self._opacity_layers)
            for part, shape, base in zip(ball, shapes, self._base_opacity[index]):
                part.points = (shape - home) * size + point
                part.fill_rgbas[:, 3] = base * visible
                if len(part.stroke_rgbas):
                    part.stroke_rgbas[:, 3] = min(1.0, visible)
        done = min(1.0, max(self.assembly - 0.75, 0) / 0.25)
        for line, (i, j) in zip(self.bonds, self._pairs):
            line.put_start_and_end_on(projected[i], projected[j])
            line.set_stroke(opacity=0.45 * done * min(self._dim[i], self._dim[j]) ** 0.5)
        for line, (i, j) in zip(self.links, self._links):
            line.put_start_and_end_on(projected[i], projected[j])
        # Draw far balls first so near ones cover them.
        self.balls.submobjects = [self._all_balls[i] for i in np.argsort(turned[:, 2])]

    def site_index(self, site) -> int:
        return int(np.argmin(np.linalg.norm(self.sites / self.spacing - np.asarray(site, dtype=float), axis=1)))


def rock_salt_crystal(n: int = 1, spacing: float = 1.3, center=ORIGIN, *, cation: float = 0.24,
                      anion: float = 0.42, **kwargs) -> ProjectedCrystal:
    sites, kinds = bm.rock_salt_sites(n)
    return ProjectedCrystal(sites, kinds, {"+": cation, "-": anion}, ION_COLORS, spacing, center, **kwargs)


# ----------------------------------------------------------------------------
# Metals: positive cores in a drifting electron sea (2D slice)
# ----------------------------------------------------------------------------


class MetalSea(_LiveMixin, _DotBins, VGroup):
    """A close-packed layer of copper-coloured ion cores inside a sea of
    delocalised electrons.

    Each electron wanders on a seeded smooth path anywhere in the slab — it
    belongs to no core. ``drift`` (screen units per second) adds a steady
    flow, as an applied voltage would; positions wrap around the slab, so
    the current is continuous. A simplified picture of delocalised states.
    ``polished`` opts into smooth sphere shading without changing electron paths.
    """

    def __init__(self, cols: int = 9, rows: int = 5, spacing: float = 0.95, center=ORIGIN, *,
                 core_radius: float = 0.3, electrons: int = 150, seed: int = 0, signs: bool = True,
                 dot_radius: float = 0.045, polished: bool = False) -> None:
        super().__init__()
        center = np.asarray(center, dtype=float)
        self.spacing, self.rows, self.cols = spacing, rows, cols
        self.anchor = Dot(center, radius=0.002, fill_opacity=0, stroke_width=0)
        self.cores = VGroup()
        self.layers: list[VGroup] = []
        height = (rows - 1) * spacing * np.sqrt(3) / 2
        for row in range(rows):
            layer = VGroup()
            y = center[1] + height / 2 - row * spacing * np.sqrt(3) / 2
            offset = 0.5 * spacing if row % 2 else 0.0
            for col in range(cols):
                x = center[0] + (col - (cols - 1) / 2) * spacing + offset - 0.25 * spacing
                core = (polished_ball if polished else shaded_ball)(core_radius, cfg.METAL_CORE).move_to([x, y, 0])
                if signs:
                    core.add(txt("+", cfg.FONT["tiny"], cfg.BG).move_to(core))
                layer.add(core)
            self.layers.append(layer)
            self.cores.add(layer)
        self.half_w = cols * spacing / 2 + 0.2
        self.half_h = height / 2 + spacing * 0.75
        rng = np.random.default_rng(cfg.SEED + 4409 * seed)
        self._base = np.column_stack([rng.uniform(-1, 1, electrons), rng.uniform(-1, 1, electrons)])
        self._freq = rng.uniform(0.35, 0.9, (electrons, 2))
        self._phase = rng.uniform(0, TAU, (electrons, 2))
        self._amp = rng.uniform(0.25, 0.6, (electrons, 1)) * spacing
        self._depth = rng.uniform(-1, 1, electrons)
        self.time, self.offset, self.drift, self.level = 0.0, 0.0, 0.0, 1.0
        self.haze = RoundedRectangle(width=2 * self.half_w, height=2 * self.half_h, corner_radius=0.35,
                                     stroke_width=0, fill_color=cfg.ELECTRON_COLOR, fill_opacity=0.07).move_to(center)
        self._setup_bins(cfg.ELECTRON_COLOR, dot_radius)
        self.add(self.anchor, self.haze, self.cores, self.dots)
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    def center_point(self) -> np.ndarray:
        return self.anchor.get_center()

    def set_drift(self, value: float) -> None:
        self.drift = float(value)

    def drift_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.drift, self.set_drift, value, **kwargs)

    def set_level(self, value: float) -> None:
        self.level = max(float(value), 0.0)
        self._place()

    def fade_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.level, self.set_level, value, **kwargs)

    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.time += dt
        self.offset += self.drift * dt
        self._place()

    def _place(self) -> None:
        centre = self.anchor.get_center()
        wander = self._amp * np.sin(self._freq * self.time + self._phase)
        x = self._base[:, 0] * self.half_w + wander[:, 0] + self.offset
        y = self._base[:, 1] * (self.half_h - 0.15) + wander[:, 1] * 0.6
        x = (x + self.half_w) % (2 * self.half_w) - self.half_w
        y = np.clip(y, -self.half_h + 0.12, self.half_h - 0.12)
        positions = np.column_stack([x, y, np.zeros_like(x)]) + centre
        fade = 0.5 + 0.5 * (0.5 + 0.5 * np.sin(self._depth * 3 + self.time * 0.8))
        self._draw_bins(positions, fade, self.level)


def ion_layers(rows: int = 4, cols: int = 7, spacing: float = 0.9, center=ORIGIN, radius: float = 0.34,
               *, polished: bool = False) -> VGroup:
    """A 2D slice of an ionic crystal: alternating + and − in every direction."""
    layers = VGroup()
    for row in range(rows):
        layer = VGroup()
        for col in range(cols):
            kind = "+" if (row + col) % 2 == 0 else "-"
            ball = ion_ball(kind, radius if kind == "-" else radius * 0.72, polished=polished)
            ball.kind = kind
            ball.move_to(np.asarray(center, dtype=float) + np.array([(col - (cols - 1) / 2) * spacing,
                                                                    ((rows - 1) / 2 - row) * spacing, 0]))
            layer.add(ball)
        layers.add(layer)
    return layers


# ----------------------------------------------------------------------------
# 3D: meshes built from computed point grids (orbitals, energy landscapes)
# ----------------------------------------------------------------------------


class GridSurface(VGroup):
    """Shaded quadrilateral faces from a (rows, cols, 3) grid of points.

    Faces whose corners have collapsed onto a line (where an isosurface is
    absent) are skipped. ``colorer(face_centre)`` may pick each face colour.
    """

    def __init__(self, grid: np.ndarray, color: str, opacity: float = 0.75, *,
                 colorer: Callable[[np.ndarray], str] | None = None, stroke_width: float = 0.0,
                 stroke_opacity: float = 0.3, min_size: float = 2e-3) -> None:
        super().__init__()
        self.build(grid, color, opacity, colorer=colorer, stroke_width=stroke_width,
                   stroke_opacity=stroke_opacity, min_size=min_size)

    def build(self, grid: np.ndarray, color: str, opacity: float, *, colorer=None, stroke_width: float = 0.0,
              stroke_opacity: float = 0.3, min_size: float = 1e-3) -> "GridSurface":
        faces = []
        rows, cols = grid.shape[0] - 1, grid.shape[1] - 1
        for i in range(rows):
            for j in range(cols):
                corners = np.array([grid[i, j], grid[i + 1, j], grid[i + 1, j + 1], grid[i, j + 1]])
                area = np.linalg.norm(np.cross(corners[2] - corners[0], corners[3] - corners[1]))
                if area < min_size * min_size:
                    continue  # the surface is absent here (collapsed onto the axis)
                face = ThreeDVMobject()
                face.set_points_as_corners([*corners, corners[0]])
                colour = colorer(corners.mean(axis=0)) if colorer else color
                face.set_fill(colour, opacity)
                face.set_stroke(colour, width=stroke_width, opacity=stroke_opacity)
                faces.append(face)
        self.submobjects = faces
        return self


class Isosurface(GridSurface):
    """A GridSurface that can be rebuilt in place from new parameters.

    ``maker(value) -> grid`` computes the points; ``morph_to`` tweens the
    parameter, rebuilding the faces every frame (only while it plays).
    """

    def __init__(self, maker: Callable[[float], np.ndarray], value: float, color: str, opacity: float = 0.75,
                 **kwargs) -> None:
        self.maker, self.value, self.colour, self.opacity_level, self._kwargs = maker, float(value), color, opacity, kwargs
        super().__init__(maker(value), color, opacity, **kwargs)

    def set_value(self, value: float) -> None:
        self.value = float(value)
        centre_shift = getattr(self, "_offset", np.zeros(3))
        self.build(self.maker(self.value) + centre_shift, self.colour, self.opacity_level, **self._kwargs)
        self._apply_rotation()

    def morph_to(self, value: float, **kwargs) -> Tween:
        return Tween(self, lambda: self.value, self.set_value, value, **kwargs)

    def place_at(self, point) -> "Isosurface":
        self._offset = np.asarray(point, dtype=float)
        self.set_value(self.value)
        return self

    def turned(self, angle: float, axis=RIGHT) -> "Isosurface":
        """Remember a fixed rotation (about the origin) applied after every rebuild."""
        self._rotation = (angle, np.asarray(axis, dtype=float))
        self.set_value(self.value)
        return self

    def _apply_rotation(self) -> None:
        rotation = getattr(self, "_rotation", None)
        if rotation:
            centre = getattr(self, "_offset", np.zeros(3))
            self.rotate(rotation[0], axis=rotation[1], about_point=centre)


# Orbital pictures are computed in Bohr radii and drawn at ORB_SCALE screen
# units per Bohr radius (P_SCALE for the larger p orbitals).
ORB_SCALE = 0.8
P_SCALE = 0.46
S_RADIUS = 2.0                  # the isolated 1s contour radius, in Bohr radii
S_CONTOUR = bm.contour_for_radius(S_RADIUS)
P_CONTOUR = bm.p_contour(0.3)


def sigma_s_grid(separation: float, xs_count: int = 46, segments: int = 24) -> np.ndarray:
    half = separation / 2
    xs = np.linspace(-half - S_RADIUS - 0.2, half + S_RADIUS + 0.2, xs_count)
    profile = bm.revolution_profile(bm.sigma_s_amplitude(separation), xs, S_CONTOUR)
    return bm.revolution_grid(profile, xs, segments) * ORB_SCALE


def sigma_p_grid(separation: float, xs_count: int = 50, segments: int = 20) -> np.ndarray:
    half = separation / 2
    xs = np.linspace(-half - 5.5, half + 5.5, xs_count)
    profile = bm.revolution_profile(bm.sigma_p_amplitude(separation), xs, P_CONTOUR)
    return bm.revolution_grid(profile, xs, segments) * P_SCALE


def single_p_grid(xs_count: int = 40, segments: int = 20) -> np.ndarray:
    xs = np.linspace(-5.5, 5.5, xs_count)
    profile = bm.revolution_profile(bm.single_p_amplitude, xs, P_CONTOUR)
    return bm.revolution_grid(profile, xs, segments) * P_SCALE


def pi_grid(separation: float, upper: bool = True, xs_count: int = 34, segments: int = 16) -> np.ndarray:
    half = separation / 2
    xs = np.linspace(-half - 2.6, half + 2.6, xs_count)
    grid, _ = bm.pi_lobe_grid(separation, P_CONTOUR, xs, segments, upper=upper)
    return grid * P_SCALE


def orbital_shade(color: str) -> Callable[[np.ndarray], str]:
    """Lighter toward the bond axis: a hint of where the density is greatest."""
    light = interpolate_color(ManimColor(color), ManimColor(cfg.WHITE), 0.35)

    def pick(point: np.ndarray) -> str:
        reach = np.hypot(point[1], point[2])
        return interpolate_color(light, ManimColor(color), float(np.clip(reach / 1.4, 0, 1)))

    return pick


def nucleus_3d(point, radius: float = 0.14, color: str = cfg.NUCLEUS_COLOR) -> Sphere:
    ball = Sphere(center=np.asarray(point, dtype=float), radius=radius, resolution=(10, 6))
    ball.set_fill(color, 1).set_stroke(width=0)
    return ball


def atom_ball(point, radius: float, color: str, resolution=(16, 10)) -> Sphere:
    ball = Sphere(center=np.asarray(point, dtype=float), radius=radius, resolution=resolution)
    ball.set_fill(color, 1).set_stroke(color, width=0.2, opacity=0.25)
    return ball


def bond_rod(a, b, color: str = cfg.MUTED, thickness: float = 0.07) -> Line3D:
    rod = Line3D(np.asarray(a, dtype=float), np.asarray(b, dtype=float), thickness=thickness, resolution=(2, 10))
    rod.set_fill(color, 1).set_stroke(width=0)
    return rod


def well_grid(depth_units: float = 2.2, scale: float = 1 / 55, r_max: float = 330, rings: int = 30,
              segments: int = 40, cap: float = 0.6) -> np.ndarray:
    """The 3D energy landscape: the H2 Morse curve swept round a vertical axis.

    Radius on screen is the separation (pm) times ``scale``; height is
    energy / D times ``depth_units``, capped at ``cap`` D on the repulsive
    wall (the flat top marks 'too close to show').
    """
    depth, r_e, a = H2
    r_wall = bm.morse_inverse(cap * depth, depth, r_e, a)
    rs = np.concatenate([np.linspace(0, r_wall, 3, endpoint=False),
                         np.linspace(r_wall, r_e * 2.2, rings // 2, endpoint=False),
                         np.linspace(r_e * 2.2, r_max, rings - rings // 2)])
    energies = np.clip(bm.morse(rs, depth, r_e, a), -depth, cap * depth) / depth * depth_units
    angles = np.linspace(0, TAU, segments + 1)
    grid = np.zeros((len(rs), len(angles), 3))
    grid[:, :, 0] = (rs * scale)[:, None] * np.cos(angles)[None, :]
    grid[:, :, 1] = (rs * scale)[:, None] * np.sin(angles)[None, :]
    grid[:, :, 2] = energies[:, None]
    return grid


def well_colorer(depth_units: float = 2.2, cap: float = 0.6) -> Callable[[np.ndarray], str]:
    def pick(point: np.ndarray) -> str:
        t = mu.unit_interval(point[2], -depth_units, cap * depth_units)
        return mu.scale_color(t, cfg.WELL_STOPS)

    return pick


def well_height(r_pm: float, depth_units: float = 2.2, cap: float = 0.6) -> float:
    depth, r_e, a = H2
    return float(np.clip(bm.morse(r_pm, depth, r_e, a), -depth, cap * depth) / depth * depth_units)


# ----------------------------------------------------------------------------
# Elements and the table (computed by utils.physics_models, as in Parts 3-4)
# ----------------------------------------------------------------------------


def block_color(z: int) -> str:
    return cfg.BLOCK_COLORS[pm.block(z)]


def element_tile(z: int, size: float = 0.66, color: str | None = None, *, symbol: bool = True,
                 number: bool = False, fill: float = 0.18) -> VGroup:
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
        tag._tile_label = True
        tile.add(tag)
        tile.number = tag
    return tile


TABLE_PITCH = 0.70
TABLE_CENTER = DOWN * 0.42


def grid_point(row: float, col: float, pitch: float = TABLE_PITCH, center=TABLE_CENTER) -> np.ndarray:
    gap = 0.38 * pitch
    x = (col - 9.5) * pitch
    y = (8 * pitch + gap) / 2 - (row - 1) * pitch - (gap if row >= 8 else 0)
    return np.array([x, y, 0.0]) + np.asarray(center, dtype=float)


def table_point(z: int, pitch: float = TABLE_PITCH, center=TABLE_CENTER) -> np.ndarray:
    """Where element ``z`` sits on screen. The row and column come from the model."""
    row, col = pm.position(z)
    return grid_point(row, col, pitch, center)


def periodic_table(pitch: float = TABLE_PITCH, center=TABLE_CENTER, zs: Iterable[int] | None = None, *,
                   style: str = "block", symbols: bool = True, fill_ratio: float = 0.9) -> VGroup:
    """The table, assembled from the filling model ('block', 'plain' or 'silhouette')."""
    table = VGroup()
    table.tiles = {}
    for z in zs or range(1, len(pm.SYMBOLS) + 1):
        colour = None if style == "block" else (cfg.CYAN if style == "plain" else cfg.MUTED)
        tile = element_tile(z, pitch * fill_ratio, colour, symbol=symbols and style != "silhouette",
                            fill=0.10 if style == "silhouette" else 0.18)
        tile.move_to(table_point(z, pitch, center))
        table.add(tile)
        table.tiles[z] = tile
    return table


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
        txt("Next: molecular geometry", 36, cfg.CYAN),
    ).arrange(DOWN, buff=0.16)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    card.thank_you, card.subscribe, card.rule, card.tagline = thank_you, subscribe, rule, tagline
    return card


__all__ = [name for name in dir() if not name.startswith("_")] + ["cfg", "pm", "mu", "bm", "bd", "np"]
