"""A projected 3D stage: real rotating geometry, drawn as smooth 2D shapes.

Every molecule, glass of solution and litre cube in the film lives on a
``Stage``. Bodies keep true 3D coordinates; each frame the stage turns them
(yaw about the vertical, pitch toward the viewer, an optional model
rotation), projects them with a gentle perspective, sorts them back to front,
and redraws them:

* ``Ball``      — an atom: a polished sphere of nested shading contours, with an
  optional element symbol that turns with it (``Halo`` glows behind one);
* ``Rod``       — a bond between two balls, a layered cylinder; double bonds
  split into parallel strands in screen space so they always read;
* ``Segment`` and ``Face`` — edges and translucent faces (the litre cube);
* ``Glassware`` — a beaker, cylinder or volumetric flask: a solid of revolution
  whose liquid height follows its volume through the glass's real profile;
* ``Swarm``     — solvent and solute particles jiggling inside a glass or a box,
  hundreds of them drawn as a handful of multi-path shapes;
* overlay items that are never hidden: ``Vector`` (arrows), ``Tag`` (any 2D
  label pinned to a 3D point).

Why not ``ThreeDScene``? Cairo draws ThreeDScene surfaces as faceted meshes,
and fixed-in-frame captions in Manim CE have known pitfalls (stray glyph
copies, captions dragged by frame_center moves). The stage keeps every
caption a plain 2D object, keeps spheres and glass perfectly smooth, and is
cheap enough to keep every model slowly turning, so no shot is ever static.

Stage state is changed only through ``Param`` animations (never ``.animate``
or Transform on the stage — those would copy a live object; see the
AnimationGroup / live-object notes in ``common.py``).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import lru_cache

import numpy as np
from manim import (ORIGIN, UL, Animation, Camera, Circle, Dot, Group, ImageMobject, ManimColor,
                   Mobject, Text, VGroup, VMobject, interpolate_color)

import config as cfg
from utils import math_utils as mu


def _value(thing):
    return thing() if callable(thing) else thing


def _vec(thing) -> np.ndarray:
    return np.asarray(_value(thing), dtype=float)


class _LiveMixin:
    """Copies made by Transform-type animations are born frozen, so a hidden
    copy never runs the stage's updater (it would desynchronise the picture)."""

    _live = True

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result._live = False
        return result


# ----------------------------------------------------------------------------
# Animation of stage parameters
# ----------------------------------------------------------------------------


class Param(Animation):
    """Tween one value of a stage (or of a body on it) without copying the stage.

    ``mode``: "scalar" (linear), "vector" (linear in 3D), "direction" (along
    the sphere, keeps unit length) or "path" (``target`` is a (frames, n, 3)
    array of directions to play through; the setter receives each frame).
    """

    def __init__(self, stage: Mobject, getter: Callable, setter: Callable, target, *, mode: str = "scalar",
                 **kwargs) -> None:
        self._get, self._set, self._target, self._mode = getter, setter, target, mode
        self._from = None
        kwargs.setdefault("suspend_mobject_updating", False)
        super().__init__(stage, **kwargs)

    def create_starting_mobject(self) -> Mobject:
        return Mobject()   # nothing to interpolate from: the setter does the work

    def begin(self) -> None:
        if self._mode != "path":
            start = self._get()
            self._from = np.array(start, dtype=float) if self._mode != "scalar" else float(start)
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        a = self.rate_func(alpha)
        if self._mode == "scalar":
            self._set(self._from + (float(self._target) - self._from) * a)
        elif self._mode == "vector":
            target = np.asarray(self._target, dtype=float)
            self._set(self._from + (target - self._from) * a)
        elif self._mode == "direction":
            self._set(mu.slerp(self._from, self._target, a))
        elif self._mode == "path":
            path = self._target
            position = a * (len(path) - 1)
            i = int(min(np.floor(position), len(path) - 2))
            f = position - i
            blend = path[i] * (1 - f) + path[i + 1] * f
            self._set(blend / np.linalg.norm(blend, axis=-1, keepdims=True))
        else:
            raise ValueError(self._mode)


# ----------------------------------------------------------------------------
# Bodies
# ----------------------------------------------------------------------------


class Body:
    """Something with 3D extent that the stage sorts by depth."""

    def __init__(self) -> None:
        self.presence = 1.0
        self.bias = 0.0        # nudges the depth order (e.g. a halo just behind its atom)
        self.mob = VGroup()
        self.depth_key = 0.0
        self._alpha_cache = None

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:  # pragma: no cover - abstract
        raise NotImplementedError


def _polished_parts(color: str, layers: int) -> list[VMobject]:
    """Unit-radius sphere shading: a dark base, nested brighter contours that
    drift toward the light (upper left), and a feathered reflection."""
    base_rgb = np.array(ManimColor(color).to_rgb())
    parts: list[VMobject] = [Circle(radius=1, stroke_width=0, fill_color=ManimColor(base_rgb * 0.22), fill_opacity=1)]
    for fraction in np.linspace(0.985, 0.05, layers):
        brightness = 0.24 + 0.76 * np.sqrt(1 - fraction * fraction)
        disc = Circle(radius=fraction, stroke_width=0, fill_color=ManimColor(np.clip(base_rgb * brightness, 0, 1)),
                      fill_opacity=1, num_components=7)
        disc.shift(UL * 0.36 * (1 - fraction))
        parts.append(disc)
    for fraction in np.linspace(1, 0.05, 12):
        glint = Circle(radius=0.3 * fraction, stroke_width=0, fill_color=cfg.WHITE,
                       fill_opacity=0.065 * (1 - fraction), num_components=5)
        glint.shift(UL * 0.36)
        parts.append(glint)
    return parts


@lru_cache(maxsize=8)
def _sphere_pixels(color: str) -> np.ndarray:
    """Cache the shared sphere material for dense, depth-sorted particle clouds."""
    camera = Camera(pixel_width=160, pixel_height=160, frame_width=2.02, frame_height=2.02,
                    background_opacity=0)
    camera.capture_mobjects([VGroup(*_polished_parts(color, 48))])
    return np.array(camera.get_image())


class Ball(Body):
    """An atom. ``pos`` may be a point or a zero-argument function."""

    LAYERS = 36

    def __init__(self, pos, radius: float, color: str, label: str | None = None, *, label_scale: float = 0.95,
                 layers: int | None = None) -> None:
        super().__init__()
        self.pos, self.radius, self.color = pos, float(radius), color
        self.parts = _polished_parts(color, layers or self.LAYERS)
        self.templates = [part.points.copy() for part in self.parts]
        self.base_alpha = [part.fill_rgbas[:, 3].copy() for part in self.parts]
        self.mob = VGroup(*self.parts)
        self.label = None
        if label:
            text_color = cfg.BG if mu.luminance(color) > 0.42 else cfg.WHITE
            glyphs = Text(label, font=cfg.FONT_FAMILY, weight="BOLD", font_size=48, color=text_color)
            glyphs.scale(label_scale * (0.62 if len(label) > 1 else 0.9) / max(glyphs.height, 1e-6))
            if glyphs.width > 1.35:
                glyphs.scale(1.35 / glyphs.width)
            glyphs.move_to(ORIGIN)
            for member in glyphs.get_family():
                member._is_decorative = True   # covered correctly by depth order; not caption text
            self.label = glyphs
            self.label_parts = [g for g in glyphs.family_members_with_points()]
            self.label_templates = [g.points.copy() for g in self.label_parts]
            self.mob.add(glyphs)

    def where(self) -> np.ndarray:
        return _vec(self.pos)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        screen, size, depth = stage.project(self.where()[None, :], R)
        s = self.radius * size[0]
        centre = screen[0]
        for part, template in zip(self.parts, self.templates):
            part.points = template * s + centre
        if self.label is not None:
            for glyph, template in zip(self.label_parts, self.label_templates):
                glyph.points = template * s + centre
        self.depth_key = depth[0]
        if self._alpha_cache != visibility:
            # Nested opaque contours would make a half-faded ball look solid in
            # the middle; spread the fade across the stack instead.
            opaque_layers = sum(base[0] > 0.5 for base in self.base_alpha)
            layer = 1 - (1 - visibility) ** (1 / opaque_layers) if visibility < 1 else 1.0
            for part, base in zip(self.parts, self.base_alpha):
                part.fill_rgbas[:, 3] = base * (layer if base[0] > 0.5 else visibility)
            if self.label is not None:
                for glyph in self.label_parts:
                    glyph.set_fill(opacity=visibility ** 2)
                    glyph.set_stroke(opacity=0)
            self._alpha_cache = visibility


class Halo(Body):
    """A soft glow drawn just behind a ball (a 'this one matters' cue)."""

    def __init__(self, ball: Ball, color: str, reach: float = 2.2, layers: int = 10, peak: float = 0.16) -> None:
        super().__init__()
        self.ball, self.reach = ball, reach
        self.bias = -1e-3
        self.parts = [Circle(radius=(i + 1) / layers, stroke_width=0, fill_color=color,
                             fill_opacity=2.2 * peak / layers) for i in range(layers)]
        self.templates = [p.points.copy() for p in self.parts]
        self.base_alpha = [p.fill_rgbas[:, 3].copy() for p in self.parts]
        self.mob = VGroup(*self.parts)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        screen, size, depth = stage.project(self.ball.where()[None, :], R)
        s = self.ball.radius * self.reach * size[0]
        for part, template in zip(self.parts, self.templates):
            part.points = template * s + screen[0]
        self.depth_key = depth[0]
        if self._alpha_cache != visibility:
            for part, base in zip(self.parts, self.base_alpha):
                part.fill_rgbas[:, 3] = base * visibility
            self._alpha_cache = visibility


ROD_DARK = "#2E4152"
ROD_LIGHT = "#E6F0F7"


class Rod(Body):
    """A bond between two balls: layered strokes give a lit cylinder."""

    def __init__(self, a: Ball, b: Ball, order: int = 1, *, width: float = 20.0, strands_gap: float = 0.12,
                 dark: str = ROD_DARK, light: str = ROD_LIGHT) -> None:
        super().__init__()
        self.a, self.b, self.order = a, b, order
        self.gap = strands_gap
        each = width if order == 1 else width * (0.66 if order == 2 else 0.5)
        self.widths = np.linspace(each, each * 0.16, 5)
        self.strands = VGroup()
        for _ in range(order):
            strand = VGroup(*[VMobject(stroke_color=interpolate_color(ManimColor(dark), ManimColor(light), k / 4),
                                       stroke_width=float(w), fill_opacity=0)
                              for k, w in enumerate(self.widths)])
            self.strands.add(strand)
        self.mob = self.strands

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        pa, pb = self.a.where(), self.b.where()
        span = pb - pa
        length = np.linalg.norm(span)
        if length < 1e-6:
            self.depth_key = -1e9
            return
        d = span / length
        # Trim into each ball so the rod emerges from its surface.
        start = pa + d * self.a.radius * 0.55
        end = pb - d * self.b.radius * 0.55
        screen, size, depth = stage.project(np.array([start, end]), R)
        self.depth_key = float(depth.mean())
        flat = screen[1] - screen[0]
        n = np.linalg.norm(flat[:2])
        side = np.array([-flat[1], flat[0], 0.0]) / n if n > 1e-6 else np.array([0.0, 1.0, 0.0])
        mean = float(size.mean())
        offsets = [0.0] if self.order == 1 else (
            [-0.5, 0.5] if self.order == 2 else [-1.0, 0.0, 1.0])
        for strand, offset in zip(self.strands, offsets):
            shift = side * offset * self.gap * mean * 2
            for line, width in zip(strand, self.widths):
                line.set_points_as_corners([screen[0] + shift, screen[1] + shift])
                line.stroke_width = float(width * mean)
        if self._alpha_cache != visibility:
            for strand in self.strands:
                for line in strand:
                    line.set_stroke(opacity=visibility)
            self._alpha_cache = visibility


class Segment(Body):
    """A thin straight line between two 3D points (guides, cube edges)."""

    def __init__(self, a, b, color: str = cfg.MUTED, width: float = 3.0, opacity: float = 0.6,
                 dashed: bool = False) -> None:
        super().__init__()
        self.a, self.b, self.opacity, self.dashed = a, b, opacity, dashed
        self.line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
        self.mob = VGroup(self.line)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        screen, _, depth = stage.project(np.array([_vec(self.a), _vec(self.b)]), R)
        if self.dashed:
            count = 14
            points = []
            for k in range(count):
                t0, t1 = k / count, (k + 0.55) / count
                points.append((screen[0] + (screen[1] - screen[0]) * t0, screen[0] + (screen[1] - screen[0]) * t1))
            self.line.clear_points()
            for p, q in points:
                self.line.start_new_path(p)
                self.line.add_line_to(q)
        else:
            self.line.set_points_as_corners([screen[0], screen[1]])
        self.depth_key = float(depth.mean())
        self.line.set_stroke(opacity=self.opacity * visibility)


class Face(Body):
    """A translucent polygon through 3D points (faces of a polyhedron)."""

    def __init__(self, corners: Sequence, color: str, opacity: float = 0.14, edge_opacity: float = 0.5) -> None:
        super().__init__()
        self.corners, self.opacity, self.edge_opacity = corners, opacity, edge_opacity
        self.poly = VMobject(fill_color=color, fill_opacity=opacity, stroke_color=color, stroke_width=2.4,
                             stroke_opacity=edge_opacity)
        self.mob = VGroup(self.poly)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        pts = np.array([_vec(c) for c in _value(self.corners)])
        screen, _, depth = stage.project(pts, R)
        self.poly.set_points_as_corners([*screen, screen[0]])
        self.depth_key = float(depth.mean())
        self.poly.set_fill(opacity=self.opacity * visibility).set_stroke(opacity=self.edge_opacity * visibility)


# ----------------------------------------------------------------------------
# Overlay items (always drawn on top, never resized by perspective)
# ----------------------------------------------------------------------------


class Overlay:
    def __init__(self) -> None:
        self.presence = 1.0
        self.mob = VGroup()

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:  # pragma: no cover - abstract
        raise NotImplementedError


class Vector(Overlay):
    """A filled arrow between two 3D points (dipoles, tip-to-tail sums)."""

    def __init__(self, start, end, color: str, *, width: float = 0.09, tip: float = 0.3, glow: bool = True) -> None:
        super().__init__()
        self.start, self.end, self.width, self.tip = start, end, width, tip
        self.halo = VMobject(stroke_width=0, fill_color=color, fill_opacity=0.18 if glow else 0)
        self.body = VMobject(stroke_color=mu.shade(color, 0.55), stroke_width=1.5, fill_color=color, fill_opacity=1)
        self.mob = VGroup(self.halo, self.body)

    def _outline(self, p: np.ndarray, q: np.ndarray, w: float, tip: float) -> list[np.ndarray] | None:
        span = q - p
        n = np.linalg.norm(span[:2])
        if n < 1e-4:
            return None
        d = span / n
        side = np.array([-d[1], d[0], 0.0])
        tip = min(tip, 0.6 * n)
        neck = q - d * tip
        return [p + side * w / 2, neck + side * w / 2, neck + side * w * 1.6, q, neck - side * w * 1.6,
                neck - side * w / 2, p - side * w / 2, p + side * w / 2]

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        screen, _, _ = stage.project(np.array([_vec(self.start), _vec(self.end)]), R)
        outline = self._outline(screen[0], screen[1], self.width, self.tip)
        if outline is None:
            self.body.points = np.zeros((0, 3))
            self.halo.points = np.zeros((0, 3))
            return
        self.body.set_points_as_corners(outline)
        wide = self._outline(screen[0], screen[1], self.width * 2.6, self.tip * 1.25)
        self.halo.set_points_as_corners(wide)
        self.body.set_fill(opacity=visibility).set_stroke(opacity=visibility)
        self.halo.set_fill(opacity=0.18 * visibility)


class Tag(Overlay):
    """Any 2D mobject pinned near a 3D point, with a fixed screen offset.

    Fading keeps each part's own opacity (a soft glow stays soft)."""

    def __init__(self, mob: Mobject, point, offset=ORIGIN) -> None:
        super().__init__()
        self.point, self.offset = point, np.asarray(offset, dtype=float)
        self.mob = VGroup(mob)
        self.content = mob
        self.parts = [m for m in mob.get_family() if isinstance(m, VMobject)]
        self.base = [(m.get_fill_opacities().copy(), m.get_stroke_opacities().copy()) for m in self.parts]
        self._shown = None

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        spot, _, _ = stage.project(_vec(self.point)[None, :], R)
        self.content.move_to(spot[0] + self.offset)
        if self._shown != visibility:
            for part, (fill, stroke) in zip(self.parts, self.base):
                part.fill_rgbas[:, 3] = fill * visibility if len(part.fill_rgbas) == len(fill) else fill[0] * visibility
                part.stroke_rgbas[:, 3] = (stroke * visibility if len(part.stroke_rgbas) == len(stroke)
                                           else stroke[0] * visibility)
            self._shown = visibility


# ----------------------------------------------------------------------------
# The stage
# ----------------------------------------------------------------------------


class Stage(_LiveMixin, VGroup):
    """A turning, projecting container for bodies and overlay items."""

    def __init__(self, at=ORIGIN, *, zoom: float = 1.0, yaw: float = 0.0, pitch: float = 0.0, spin: float = 0.0,
                 sway: float = 0.0, distance: float = 14.0, presence: float = 1.0) -> None:
        super().__init__()
        self.anchor = Dot(np.asarray(at, dtype=float), radius=0.001, fill_opacity=0, stroke_width=0)
        self.zoom, self.yaw, self.pitch = float(zoom), float(yaw), float(pitch)
        self.spin, self.sway, self.distance = float(spin), float(sway), float(distance)
        self.model = np.eye(3)
        self.presence = float(presence)
        self.clock = 0.0
        self.bodies: list[Body] = []
        self.overlays: list[Overlay] = []
        self.world = VGroup()
        self.top = VGroup()
        self.add(self.anchor, self.world, self.top)
        # The draw tree changes every frame (depth sort), so the scene must
        # render this stage's live children rather than a frozen family list.
        self._live_draw_order = True
        self.add_updater(lambda m, dt: m._advance(dt))

    # --- geometry ---------------------------------------------------------------

    def rotation(self) -> np.ndarray:
        sway_yaw = self.sway * np.sin(0.23 * self.clock)
        sway_pitch = 0.35 * self.sway * np.sin(0.17 * self.clock + 0.8)
        return mu.view_rotation(self.yaw + sway_yaw, self.pitch + sway_pitch) @ self.model

    def project(self, points: np.ndarray, R: np.ndarray | None = None):
        R = self.rotation() if R is None else R
        view = np.atleast_2d(points) @ R.T
        size = mu.perspective(view[:, 2], self.distance) * self.zoom
        screen = view * size[:, None]
        screen[:, 2] = 0
        screen += self.anchor.get_center()
        return screen, size, view[:, 2]

    def screen_point(self, point) -> np.ndarray:
        return self.project(np.asarray(point, dtype=float)[None, :])[0][0]

    def center_point(self) -> np.ndarray:
        return self.anchor.get_center()

    # --- contents ---------------------------------------------------------------

    def add_body(self, *bodies: Body) -> Body:
        for body in bodies:
            if body not in self.bodies:
                self.bodies.append(body)
        self.refresh()
        return bodies[0] if bodies else None

    def add_overlay(self, *items: Overlay) -> Overlay:
        for item in items:
            if item not in self.overlays:
                self.overlays.append(item)
        self.refresh()
        return items[0] if items else None

    def drop(self, *things) -> None:
        for thing in things:
            if thing in self.bodies:
                self.bodies.remove(thing)
            if thing in self.overlays:
                self.overlays.remove(thing)
        self.refresh()

    # --- per frame --------------------------------------------------------------

    def _advance(self, dt: float) -> None:
        if not self._live:
            return
        self.clock += dt
        self.yaw += self.spin * dt
        self.refresh()

    def refresh(self) -> None:
        R = self.rotation()
        shown = []
        for body in self.bodies:
            visibility = body.presence * self.presence
            if visibility <= 0.004:
                continue
            body.place(self, R, min(visibility, 1.0))
            shown.append((body.depth_key + body.bias, len(shown), body.mob))
        shown.sort(key=lambda item: (item[0], item[1]))
        self.world.submobjects = [mob for _, _, mob in shown]
        top = []
        for item in self.overlays:
            visibility = item.presence * self.presence
            if visibility <= 0.004:
                continue
            item.place(self, R, min(visibility, 1.0))
            top.append(item.mob)
        self.top.submobjects = top

    # --- animations ---------------------------------------------------------------

    def tween(self, getter, setter, target, mode: str = "scalar", **kwargs) -> Param:
        return Param(self, getter, setter, target, mode=mode, **kwargs)

    def fade(self, thing=0.5, value: float | None = None, family: bool = True, **kwargs):
        """Fade a body or overlay item (or the whole stage) to ``value``.

        Called Manim's way — ``fade(darkness, family)``, as FadeIn/FadeOut do
        on a (frozen) stage — it behaves like ``Mobject.fade``.
        """
        if value is None and isinstance(thing, (int, float)):
            return super().fade(thing, family)

        def setter(v, t=thing):
            t.presence = max(0.0, v)
        return Param(self, lambda t=thing: t.presence, setter, value, **kwargs)

    def turn(self, yaw: float | None = None, pitch: float | None = None, **kwargs) -> list[Param]:
        moves = []
        if yaw is not None:
            moves.append(Param(self, lambda: self.yaw, lambda v: setattr(self, "yaw", v), yaw, **kwargs))
        if pitch is not None:
            moves.append(Param(self, lambda: self.pitch, lambda v: setattr(self, "pitch", v), pitch, **kwargs))
        return moves

    def set_spin(self, rate: float, **kwargs) -> Param:
        return Param(self, lambda: self.spin, lambda v: setattr(self, "spin", v), rate, **kwargs)

    def zoom_to(self, value: float, **kwargs) -> Param:
        return Param(self, lambda: self.zoom, lambda v: setattr(self, "zoom", v), value, **kwargs)

    def glide(self, point, **kwargs) -> Param:
        return Param(self, self.anchor.get_center, self.anchor.move_to, np.asarray(point, dtype=float),
                     mode="vector", **kwargs)

    def align(self, target: np.ndarray, **kwargs) -> Param:
        """Turn the model, along the shortest rotation, until ``model == target``."""
        start: dict[str, np.ndarray] = {}

        def get():
            start["model"] = self.model.copy()
            relative = np.asarray(target, dtype=float) @ self.model.T
            angle = float(np.arccos(np.clip((np.trace(relative) - 1) / 2, -1, 1)))
            axis = np.array([relative[2, 1] - relative[1, 2], relative[0, 2] - relative[2, 0],
                             relative[1, 0] - relative[0, 1]])
            if np.linalg.norm(axis) < 1e-9:
                # At 180 degrees the antisymmetric part vanishes. Recover
                # the invariant axis instead of choosing an unrelated y axis.
                _, vectors = np.linalg.eigh((relative + relative.T) / 2)
                axis = vectors[:, -1]
            start["axis"], start["angle"] = mu.unit(axis), angle
            return 0.0

        def put(value):
            self.model = mu.rotation_about(start["axis"], value * start["angle"]) @ start["model"]

        return Param(self, get, put, 1.0, **kwargs)

    def rock(self, axis, angle: float, **kwargs) -> Param:
        """Turn the model itself about a fixed axis (relative to its current pose)."""
        start = {}

        def get():
            start["model"] = self.model.copy()
            return 0.0

        def put(value):
            self.model = mu.rotation_about(axis, value) @ start["model"]

        return Param(self, get, put, angle, **kwargs)


# ----------------------------------------------------------------------------
# Glassware: a solid of revolution with liquid inside
# ----------------------------------------------------------------------------


def _ring_arcs(P: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Split a projected ring into its lower (front) and upper (back) arcs,
    each running left to right."""
    n = len(P)
    i_left, i_right = int(np.argmin(P[:, 0])), int(np.argmax(P[:, 0]))
    a = [(i_left + k) % n for k in range((i_right - i_left) % n + 1)]
    b = [(i_right + k) % n for k in range((i_left - i_right) % n + 1)]
    arc_a, arc_b = P[a], P[b][::-1]
    if arc_a[:, 1].mean() <= arc_b[:, 1].mean():
        return arc_a, arc_b
    return arc_b, arc_a


class Glassware:
    """A beaker, cylinder or volumetric flask on a stage, with liquid in it.

    The glass is ``utils.physics_models.Profile`` turned about the vertical
    axis; ``volume`` (mL) sets the liquid height through the profile, so
    liquid in a thin neck rises fast and in a wide bulb slowly. It is drawn as
    two bodies — a back (rear wall, liquid body, surface) kept behind
    everything inside, and a front (front rim, silhouette, calibration mark,
    ticks, highlight, the purple *volume* glow) kept in front — so particles
    on the same stage always sit inside the glass.
    """

    SAMPLES = 64

    def __init__(self, stage: "Stage", profile, origin=ORIGIN, *, volume: float = 0.0, scale: float = 1.0,
                 liquid_color: str = cfg.LIQUID, glass_color: str = cfg.GLASS, ticks: Sequence[float] = (),
                 mark: bool = False, lid: bool = False) -> None:
        self.stage, self.profile, self.scale = stage, profile, float(scale)
        self.origin = np.asarray(origin, dtype=float)
        self.volume = float(volume)
        self.liquid_color, self.glass_color = liquid_color, glass_color
        self.reflection_alpha = 1.0  # scene-level control for broad glass reflections
        self.ticks, self.mark, self.lid = tuple(ticks), mark, lid
        self.glow = 0.0          # purple outline of the liquid: "the solution's volume"
        self.liquid_alpha = 1.0
        self.glass_alpha = 1.0
        self.mark_glow = 0.0
        theta = np.linspace(0, 2 * np.pi, self.SAMPLES, endpoint=False)
        self._cs = np.column_stack([np.cos(theta), np.zeros_like(theta), np.sin(theta)])
        self.back = _GlassBack(self)
        self.front = _GlassFront(self)
        stage.add_body(self.back, self.front)

    # --- geometry --------------------------------------------------------------
    @property
    def height(self) -> float:
        return self.profile.height * self.scale

    def level(self) -> float:
        """Liquid height above the base, screen units."""
        if self.volume <= 0:
            return 0.0
        return self.profile.height_for(self.volume) * self.scale

    def radius(self, y: np.ndarray | float) -> np.ndarray:
        return np.interp(np.asarray(y) / self.scale, self.profile.ys, self.profile.rs) * self.scale

    def ring(self, y: float) -> np.ndarray:
        return self.origin + self._cs * float(self.radius(y)) + np.array([0.0, y, 0.0])

    def world(self, u: np.ndarray) -> np.ndarray:
        """Homes (a, v, b) -> points inside the liquid (a, b in the unit disc, v in 0..1)."""
        u = np.asarray(u, dtype=float)
        level = max(self.level(), 1e-3)
        y = 0.04 * self.scale + u[:, 1] * (level - 0.1 * self.scale)
        r = self.radius(y) * 0.86
        return self.origin + np.column_stack([u[:, 0] * r, y, u[:, 2] * r])

    def top_point(self) -> np.ndarray:
        return self.origin + np.array([0.0, self.height, 0.0])

    def surface_point(self) -> np.ndarray:
        return self.origin + np.array([0.0, self.level(), 0.0])

    def _heights(self, top: float) -> np.ndarray:
        ys = [y * self.scale for y in self.profile.ys if 0 < y * self.scale < top]
        ys += list(np.linspace(0, top, 14))
        return np.unique(np.clip(np.array(ys + [0.0, top]), 0, top))

    def outline(self, top: float, R: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:
        """Silhouette polygon of the glass (or liquid) up to height ``top``."""
        rings = [self.stage.project(self.ring(y), R)[0] for y in self._heights(top)]
        lower_bottom, _ = _ring_arcs(rings[0])
        _, upper_top = _ring_arcs(rings[-1])
        right = [r[np.argmax(r[:, 0])] for r in rings[1:-1]]
        left = [r[np.argmin(r[:, 0])] for r in rings[1:-1]][::-1]
        pts = [*lower_bottom, *right, *upper_top[::-1], *left]
        return np.array(pts), rings

    def set_volume(self, volume: float, **kwargs) -> Param:
        return Param(self.stage, lambda: self.volume, lambda v: setattr(self, "volume", v), volume, **kwargs)

    def set_glow(self, value: float, **kwargs) -> Param:
        return Param(self.stage, lambda: self.glow, lambda v: setattr(self, "glow", v), value, **kwargs)

    def set_attr(self, name: str, value: float, **kwargs) -> Param:
        return Param(self.stage, lambda: getattr(self, name), lambda v: setattr(self, name, v), value, **kwargs)


def _poly(mob: VMobject, pts: np.ndarray, closed: bool = True) -> None:
    pts = np.asarray(pts)
    if len(pts) < 2:
        mob.points = np.zeros((0, 3))
        return
    mob.set_points_as_corners([*pts, pts[0]] if closed else list(pts))


class _GlassBack(Body):
    def __init__(self, glass: Glassware) -> None:
        super().__init__()
        self.glass = glass
        g = glass
        self.wall = VMobject(stroke_width=0, fill_color=g.glass_color, fill_opacity=0.05)
        self.floor = VMobject(stroke_color=g.glass_color, stroke_width=2.0, stroke_opacity=0.35, fill_opacity=0)
        self.rim = VMobject(stroke_color=g.glass_color, stroke_width=2.6, stroke_opacity=0.45, fill_opacity=0)
        self.liquid = VMobject(stroke_width=0, fill_color=g.liquid_color, fill_opacity=0.3)
        self.liquid_bands = [VMobject(stroke_width=0, fill_color=mu.mix(g.liquid_color, cfg.WHITE, 0.18),
                                      fill_opacity=0) for _ in range(7)]
        self.surface = VMobject(stroke_color=mu.mix(g.liquid_color, cfg.WHITE, 0.55), stroke_width=2.2,
                                stroke_opacity=0.55, fill_color=mu.mix(g.liquid_color, cfg.WHITE, 0.25), fill_opacity=0.22)
        self.mark_back = VMobject(stroke_color=cfg.WHITE, stroke_width=2.2, stroke_opacity=0.3, fill_opacity=0)
        self.mob = VGroup(self.wall, self.floor, self.rim, self.liquid, *self.liquid_bands, self.surface, self.mark_back)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        g = self.glass
        self.depth_key = -1e5
        outline, rings = g.outline(g.height, R)
        _poly(self.wall, outline)
        _poly(self.floor, rings[0])
        _, upper = _ring_arcs(rings[-1])
        _poly(self.rim, upper, closed=False)
        level = g.level()
        if level > 1e-3:
            liquid, lrings = g.outline(level, R)
            _poly(self.liquid, liquid)
            _poly(self.surface, lrings[-1])
            left = np.array([r[np.argmin(r[:, 0])] for r in lrings])
            right = np.array([r[np.argmax(r[:, 0])] for r in lrings])
            for band, (lo, hi) in zip(self.liquid_bands, zip(np.linspace(0.05, 0.75, 7), np.linspace(0.25, 0.95, 7))):
                _poly(band, np.vstack([left + (right-left)*lo, (left + (right-left)*hi)[::-1]]))
        else:
            self.liquid.points = np.zeros((0, 3))
            self.surface.points = np.zeros((0, 3))
            for band in self.liquid_bands:
                band.points = np.zeros((0, 3))
        if g.mark:
            mark_ring = stage.project(g.ring(g.profile.mark_y * g.scale), R)[0]
            _, back_arc = _ring_arcs(mark_ring)
            _poly(self.mark_back, back_arc, closed=False)
        else:
            self.mark_back.points = np.zeros((0, 3))
        a, la = visibility * g.glass_alpha, visibility * g.liquid_alpha
        self.wall.set_fill(opacity=0.05 * a)
        self.floor.set_stroke(opacity=0.35 * a)
        self.rim.set_stroke(opacity=0.45 * a)
        self.liquid.set_fill(opacity=0.3 * la)
        for band, weight in zip(self.liquid_bands, (0.025, 0.035, 0.045, 0.05, 0.04, 0.03, 0.02)):
            band.set_fill(opacity=weight * la)
        self.surface.set_fill(opacity=0.22 * la).set_stroke(opacity=0.55 * la)
        self.mark_back.set_stroke(opacity=0.3 * a)


class _GlassFront(Body):
    def __init__(self, glass: Glassware) -> None:
        super().__init__()
        self.glass = glass
        g = glass
        light = mu.mix(g.glass_color, cfg.WHITE, 0.4)
        self.glow_layers = [VMobject(stroke_color=cfg.VOLUME, stroke_width=w, stroke_opacity=o, fill_opacity=0)
                            for w, o in ((18, 0.10), (9, 0.22), (3.6, 1.0))]
        self.glow_fill = VMobject(stroke_width=0, fill_color=cfg.VOLUME, fill_opacity=0.0)
        self.meniscus = VMobject(stroke_color=mu.mix(g.liquid_color, cfg.WHITE, 0.6), stroke_width=3.0,
                                 stroke_opacity=0.8, fill_opacity=0)
        self.left = VMobject(stroke_color=light, stroke_width=3.0, stroke_opacity=0.7, fill_opacity=0)
        self.right = VMobject(stroke_color=light, stroke_width=3.0, stroke_opacity=0.7, fill_opacity=0)
        self.rim = VMobject(stroke_color=light, stroke_width=3.6, stroke_opacity=0.85, fill_opacity=0)
        self.bottom = VMobject(stroke_color=light, stroke_width=3.0, stroke_opacity=0.6, fill_opacity=0)
        self.shine = VMobject(stroke_color=cfg.WHITE, stroke_width=9, stroke_opacity=0.12, fill_opacity=0)
        self.reflections = [VMobject(stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0) for _ in range(3)]
        self.inner_rim = VMobject(stroke_color=cfg.WHITE, stroke_width=1.4, stroke_opacity=0.45, fill_opacity=0)
        self.heel = VMobject(stroke_color=cfg.GLASS, stroke_width=5.0, stroke_opacity=0.22, fill_opacity=0)
        self.mark_front = VMobject(stroke_color=cfg.WHITE, stroke_width=3.4, stroke_opacity=0.95, fill_opacity=0)
        self.mark_glow = VMobject(stroke_color=cfg.GOLD, stroke_width=12, stroke_opacity=0.0, fill_opacity=0)
        self.tick_mob = VMobject(stroke_color=light, stroke_width=2.6, stroke_opacity=0.75, fill_opacity=0)
        self.lid = VMobject(stroke_color=light, stroke_width=2.6, stroke_opacity=0.9, fill_color="#5D7488",
                            fill_opacity=0.85)
        self.mob = VGroup(self.glow_fill, *self.glow_layers, self.meniscus, self.left, self.right, self.bottom,
                          self.shine, *self.reflections, self.inner_rim, self.heel, self.mark_glow, self.mark_front, self.tick_mob, self.rim, self.lid)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        g = self.glass
        self.depth_key = 1e5
        _, rings = g.outline(g.height, R)
        right = np.array([r[np.argmax(r[:, 0])] for r in rings])
        left = np.array([r[np.argmin(r[:, 0])] for r in rings])
        _poly(self.left, left, closed=False)
        _poly(self.right, right, closed=False)
        lower_top, _ = _ring_arcs(rings[-1])
        _poly(self.rim, lower_top, closed=False)
        lower_bottom, _ = _ring_arcs(rings[0])
        _poly(self.bottom, lower_bottom, closed=False)
        _poly(self.heel, lower_bottom + np.array([0, 0.035*g.scale, 0]), closed=False)
        axis_top = g.origin + np.array([0, g.height, 0])
        inner = axis_top + (g.ring(g.height)-axis_top) * np.array([0.965, 1, 0.965])
        front_inner, _ = _ring_arcs(stage.project(inner, R)[0])
        _poly(self.inner_rim, front_inner, closed=False)
        for band, (lo, hi) in zip(self.reflections, ((0.07,0.105),(0.14,0.155),(0.88,0.90))):
            _poly(band, np.vstack([left[1:-1] + (right-left)[1:-1]*lo,
                                  (left[1:-1] + (right-left)[1:-1]*hi)[::-1]]))
        shine = left + (right - left) * 0.16
        _poly(self.shine, shine[1:-1] if len(shine) > 3 else shine, closed=False)
        level = g.level()
        if level > 1e-3:
            liquid, lrings = g.outline(level, R)
            lower_surface, _ = _ring_arcs(lrings[-1])
            _poly(self.meniscus, lower_surface, closed=False)
            for layer in (*self.glow_layers, self.glow_fill):
                _poly(layer, liquid)
        else:
            for layer in (self.meniscus, *self.glow_layers, self.glow_fill):
                layer.points = np.zeros((0, 3))
        if g.mark:
            mark_ring = stage.project(g.ring(g.profile.mark_y * g.scale), R)[0]
            front_arc, _ = _ring_arcs(mark_ring)
            _poly(self.mark_front, front_arc, closed=False)
            _poly(self.mark_glow, front_arc, closed=False)
        else:
            self.mark_front.points = np.zeros((0, 3))
            self.mark_glow.points = np.zeros((0, 3))
        self.tick_mob.clear_points()
        for y in g.ticks:
            ring = stage.project(g.ring(y * g.scale), R)[0]
            front = int(np.argmin(ring[:, 1]))   # lowest point = nearest the viewer
            idx = [(front + k) % len(ring) for k in range(-3, 4)]
            self.tick_mob.start_new_path(ring[idx[0]])
            for i in idx[1:]:
                self.tick_mob.add_line_to(ring[i])
        if g.lid:
            _poly(self.lid, rings[-1])
        else:
            self.lid.points = np.zeros((0, 3))
        a = visibility * g.glass_alpha
        for mob, base in ((self.left, 0.7), (self.right, 0.7), (self.rim, 0.85), (self.bottom, 0.6),
                          (self.shine, 0.12 * g.reflection_alpha), (self.mark_front, 0.95), (self.tick_mob, 0.75)):
            mob.set_stroke(opacity=base * a)
        for band, opacity in zip(self.reflections, (0.11,0.16,0.08)):
            band.set_fill(opacity=opacity*a*g.reflection_alpha)
        self.inner_rim.set_stroke(opacity=0.5*a)
        self.heel.set_stroke(opacity=0.28*a)
        self.lid.set_fill(opacity=0.85 * a).set_stroke(opacity=0.9 * a)
        self.mark_glow.set_stroke(opacity=0.35 * g.mark_glow * visibility)
        self.meniscus.set_stroke(opacity=0.8 * visibility * g.liquid_alpha)
        for layer, base in zip(self.glow_layers, (0.10, 0.22, 1.0)):
            layer.set_stroke(opacity=base * g.glow * visibility)
        self.glow_fill.set_fill(opacity=0.14 * g.glow * visibility)


class Box:
    """A cube-shaped region (e.g. one litre of solution) for a swarm to live in."""

    def __init__(self, centre=ORIGIN, half: float = 1.5) -> None:
        self.centre, self.half = np.asarray(centre, dtype=float), float(half)

    def world(self, u: np.ndarray) -> np.ndarray:
        u = np.asarray(u, dtype=float)
        # Homes are drawn for a cylinder (a, v, b); map them into the cube.
        mapped = np.column_stack([u[:, 0] / 0.86, 2 * u[:, 1] - 1, u[:, 2] / 0.86])
        return self.centre + np.clip(mapped, -1, 1) * self.half * 0.88


# ----------------------------------------------------------------------------
# A swarm of molecules: solvent as fine dots or beads, solute as glowing beads
# ----------------------------------------------------------------------------


def _circle_template(components: int = 6) -> np.ndarray:
    return Circle(radius=1.0, num_components=components).points.copy()


class Swarm(Body):
    """Solvent and solute particles jiggling inside a container.

    Every particle has a fixed *home* (normalised, from ``physics_models``)
    which the container maps to a point in its liquid, so when the liquid
    grows (heating, dilution) the particles spread with it. Thermal motion is
    a smooth deterministic jiggle whose rate is ``speed``. Particles are
    drawn as a handful of VMobjects, each holding many circles as separate
    sub-paths, so a swarm of hundreds costs about as much as a few shapes.

    Tweenable scalars: ``speed``, ``amplitude``, ``mix`` (0: the solute is a
    crystal above the liquid, 1: dissolved), ``solute_alpha``,
    ``solvent_alpha``, ``solute_glow``, ``solvent_glow`` and ``transfer``
    (0: in ``container``, 1: in ``target``).

    ``style="polished"`` gives solute beads feathered sphere shading and
    suppresses the solvent's white dot highlights for close-up shots.
    ``style="spheres"`` shades both species and depth-sorts every sphere.
    """

    def __init__(self, stage: "Stage", container, *, solvent: int, solute: int, seed: int, style: str = "dots",
                 solvent_radius: float = 0.035, solute_radius: float = 0.11, amplitude: float = 0.08,
                 solvent_color: str = cfg.SOLVENT, solute_color: str = cfg.SOLUTE_DEEP) -> None:
        super().__init__()
        from utils import physics_models as pm

        rng = np.random.default_rng(seed)
        self.container, self.target = container, None
        self.n_solvent, self.n_solute = solvent, solute
        n = solvent + solute
        self.homes = pm.disc_cylinder_samples(n, rng)
        self.freqs = rng.uniform(0.6, 1.7, (n, 3))
        self.phases = rng.uniform(0, 2 * np.pi, (n, 3))
        self.crystal = rng.normal(0, 1, (solute, 3)) * 0.09 + np.array([0.0, 0.0, 0.0])
        self.delays = rng.uniform(0, 0.45, solute)
        self.style = style
        self.r_solvent, self.r_solute = solvent_radius, solute_radius
        self.solvent_color, self.solute_color = solvent_color, solute_color
        self.speed, self.amplitude, self.mix, self.transfer = 1.0, float(amplitude), 1.0, 0.0
        self.solute_alpha = self.solvent_alpha = 1.0
        self.solute_glow, self.solvent_glow = 0.0, 0.0
        self.drop_from = None    # world point the crystal falls from (mix < 1)
        self.t = 0.0
        self._last_clock = None
        self.screen = np.zeros((n, 3))
        self.size = np.ones(n)
        self.template = _circle_template()
        self.dot_bins = [VMobject(stroke_width=0, fill_color=solvent_color, fill_opacity=0.5) for _ in range(2)]
        self.dot_mids = [VMobject(stroke_width=0, fill_color=solvent_color, fill_opacity=0) for _ in range(2)]
        self.dot_glints = [VMobject(stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.0) for _ in range(2)]
        deep = mu.shade(solute_color, 0.55)
        self.halo_layers = [VMobject(stroke_width=0, fill_color=solute_color, fill_opacity=0.0) for _ in range(3)]
        self.bead_base = VMobject(stroke_width=0, fill_color=deep, fill_opacity=1)
        self.bead_mid = VMobject(stroke_width=0, fill_color=solute_color, fill_opacity=1)
        self.bead_glint = VMobject(stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.75)
        # The opening close-up resolves the material shading; use the same
        # feathered sphere contours as the molecular atoms, batched by layer.
        self.polished_beads = _polished_parts(solute_color, 28) if style == "polished" else []
        self.polished_templates = [part.points.copy() for part in self.polished_beads]
        self.polished_opacities = [part.get_fill_opacity() for part in self.polished_beads]
        bead_parts = self.polished_beads or [self.bead_base, self.bead_mid, self.bead_glint]
        self.mob = VGroup(self.dot_bins[0], self.dot_mids[0], self.dot_glints[0], *self.halo_layers,
                          *bead_parts, self.dot_bins[1], self.dot_mids[1], self.dot_glints[1])
        self.sphere_sprites = []
        self.sphere_templates = []
        self.sphere_opacities = [None] * n
        if style == "spheres":
            for index in range(n):
                color = solvent_color if index < solvent else solute_color
                sprite = ImageMobject(_sphere_pixels(color)).set_width(2.02)
                self.sphere_sprites.append(sprite)
                self.sphere_templates.append(sprite.points.copy())
            self.mob = Group(*self.sphere_sprites)
        self.stage = stage
        stage.add_body(self)

    # --- motion ---------------------------------------------------------------------
    def positions(self) -> np.ndarray:
        """World positions of every particle (solvent first, then solute)."""
        wobble = np.sin(self.freqs * self.t + self.phases) * self.amplitude
        here = self.container.world(self.homes)
        if self.target is not None and self.transfer > 0:
            there = self.target.world(self.homes)
            s = mu.smoothstep(self.transfer)
            lift = np.array([0.0, 1.0, 0.0]) * np.sin(np.pi * s) * 1.4
            here = here * (1 - s) + there * s + lift
        pos = here + wobble
        if self.n_solute and self.mix < 1:
            k = self.n_solvent
            free = pos[k:]
            drop = _vec(self.drop_from) if self.drop_from is not None else free.mean(axis=0) + np.array([0, 2.5, 0])
            centre_in = self.container.world(np.array([[0.0, 0.55, 0.0]]))[0]
            fall = mu.smoothstep(min(self.mix / 0.35, 1.0))
            centre = drop + (centre_in - drop) * fall
            clump = centre + self.crystal
            spread = np.clip((self.mix - 0.35 - self.delays * 0.5) / 0.45, 0, 1)
            spread = spread * spread * (3 - 2 * spread)
            pos[k:] = clump * (1 - spread[:, None]) + free * spread[:, None]
        return pos

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        if self._last_clock is None:
            self._last_clock = stage.clock
        self.t += (stage.clock - self._last_clock) * self.speed
        self._last_clock = stage.clock
        pos = self.positions()
        screen, size, depth = stage.project(pos, R)
        self.screen, self.size = screen, size
        self.depth_key = float(depth.mean())
        k = self.n_solvent
        if self.style == "spheres":
            for index, (sprite, template) in enumerate(zip(self.sphere_sprites, self.sphere_templates)):
                solvent = index < k
                radius = self.r_solvent * (1 + 0.45 * self.solvent_glow) if solvent else self.r_solute
                sprite.points = template * (radius * size[index]) + screen[index]
                opacity = visibility * (self.solvent_alpha if solvent else self.solute_alpha)
                if self.sphere_opacities[index] != opacity:
                    sprite.set_opacity(opacity)
                    self.sphere_opacities[index] = opacity
            self.mob.submobjects = [self.sphere_sprites[int(i)] for i in np.argsort(depth)]
            return
        sv, sd, dd = screen[:k], size[:k], depth[:k]
        mid = float(np.median(dd)) if k else 0.0
        glow_tone = mu.mix(self.solvent_color, cfg.CYAN, 0.6)
        for b, mask in enumerate((dd < mid, dd >= mid)):
            radius = self.r_solvent * sd[mask] * (1 + 0.45 * self.solvent_glow)
            self.dot_bins[b].points = self._circles(sv[mask], radius)
            tone = mu.mix(self.solvent_color, glow_tone, self.solvent_glow)
            alpha = self.solvent_alpha * visibility
            self.dot_bins[b].set_fill(color=mu.shade(tone, 0.58),
                                      opacity=min(1.0, 0.48 + 0.3*b + 0.25*self.solvent_glow)*alpha)
            mid_c = sv[mask] + np.array([-0.18, 0.18, 0.0]) * radius[:, None]
            self.dot_mids[b].points = self._circles(mid_c, radius * 0.76)
            self.dot_mids[b].set_fill(color=tone, opacity=(0.54 + 0.12*b)*alpha)
            glint_c = sv[mask] + np.array([-0.36, 0.36, 0.0]) * radius[:, None]
            self.dot_glints[b].points = self._circles(glint_c, radius * 0.23)
            glint_alpha = 0.0 if self.style == "polished" else (0.52 if self.style == "beads" else 0.28)
            self.dot_glints[b].set_fill(opacity=glint_alpha*alpha)
        su, ss = screen[k:], size[k:]
        if len(su):
            r = self.r_solute * ss
            for layer, (reach, peak) in zip(self.halo_layers, ((3.4, 0.10), (2.4, 0.16), (1.6, 0.24))):
                layer.points = self._circles(su, r * reach)
                layer.set_fill(opacity=peak * self.solute_glow * self.solute_alpha * visibility)
            self.bead_base.points = self._circles(su, r)
            self.bead_mid.points = self._circles(su + np.array([-0.18, 0.18, 0]) * r[:, None], r * 0.72)
            self.bead_glint.points = self._circles(su + np.array([-0.36, 0.36, 0]) * r[:, None], r * 0.24)
            a = self.solute_alpha * visibility
            self.bead_base.set_fill(opacity=a)
            self.bead_mid.set_fill(opacity=a)
            self.bead_glint.set_fill(opacity=0.75 * a)
            if self.polished_beads:
                opaque_layers = sum(opacity > 0.5 for opacity in self.polished_opacities)
                fade = 1 - (1 - a) ** (1 / opaque_layers) if a < 1 else 1.0
                for part, template, opacity in zip(self.polished_beads, self.polished_templates,
                                                   self.polished_opacities):
                    points = template[None, :, :] * r[:, None, None] + su[:, None, :]
                    points[:, :, 2] = 0
                    part.points = points.reshape(-1, 3)
                    part.set_fill(opacity=opacity * (fade if opacity > 0.5 else a))
        else:
            for m in (*self.halo_layers, self.bead_base, self.bead_mid, self.bead_glint, *self.polished_beads):
                m.points = np.zeros((0, 3))

    def _circles(self, centres: np.ndarray, radii) -> np.ndarray:
        if len(centres) == 0:
            return np.zeros((0, 3))
        radii = np.broadcast_to(np.asarray(radii, dtype=float), (len(centres),))
        pts = self.template[None, :, :] * radii[:, None, None] + centres[:, None, :]
        pts[:, :, 2] = 0
        return pts.reshape(-1, 3)

    def tween(self, name: str, value: float, **kwargs) -> Param:
        return Param(self.stage, lambda: getattr(self, name), lambda v: setattr(self, name, v), value,
                     **kwargs)
