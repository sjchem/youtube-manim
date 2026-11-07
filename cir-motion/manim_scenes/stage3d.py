"""A projected 3D stage: real rotating geometry, drawn as smooth 2D shapes.

Every track, car, turntable, helix and planet in the film lives on a
``Stage``. Bodies keep true 3D coordinates; each frame the stage turns them
(yaw about the vertical, pitch toward the viewer, an optional model
rotation), projects them with a gentle perspective, sorts them back to front,
and redraws them:

* ``Ball``      — the particle (or the Earth, a marker): a polished sphere of nested
  shading contours (``Halo`` glows behind one);
* ``Rod``       — a lit cylinder between two balls (a post, a cannon barrel);
* ``Segment`` and ``Face`` — lines and translucent faces (axes, walls);
* ``Grid``      — a ruled plane (the ground, a wall), drawn behind everything;
* ``Curve``     — a glowing polyline through live 3D points (a trail, a
  trajectory, a running track, a space-time curve);
* ``Disc``      — a flat circle lying in a plane (a turntable, a flash);
* ``Block``     — a lit box with a heading (car bodies, cabins, wheels);
* ``Band``      — a flat strip along a curve (roads and running tracks);
* overlay items that are never hidden: ``Vector`` (arrows), ``Tag`` (any 2D
  label pinned to a 3D point).

Why not ``ThreeDScene``? Cairo draws ThreeDScene surfaces as faceted meshes,
and fixed-in-frame captions in Manim CE have known pitfalls (stray glyph
copies, captions dragged by frame_center moves). The stage keeps every
caption a plain 2D object, keeps spheres perfectly smooth, and is cheap
enough to keep every field slowly turning, so no shot is ever static.

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
        self.glow = glow
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
        wide = self._outline(screen[0], screen[1], self.width * 1.8, self.tip * 1.08)
        self.halo.set_points_as_corners(wide)
        self.body.set_fill(opacity=visibility).set_stroke(opacity=visibility)
        self.halo.set_fill(opacity=(0.10 if self.glow else 0) * visibility)


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
# Planes, curves and discs
# ----------------------------------------------------------------------------


def _segments_as_points(screen: np.ndarray) -> np.ndarray:
    """(2n, 3) endpoint pairs -> VMobject points holding n separate straight subpaths."""
    p, q = screen[0::2], screen[1::2]
    quads = np.stack([p, p + (q - p) / 3, p + 2 * (q - p) / 3, q], axis=1)
    return quads.reshape(-1, 3)


class Grid(Body):
    """A ruled plane through ``origin`` spanned by directions ``u`` and ``v``.

    Lines run every ``step`` across ``u_range`` x ``v_range`` (world units);
    every ``major``-th line is drawn brighter. An optional translucent panel
    fills the plane. Grids sit behind every other body (``bias``)."""

    def __init__(self, origin, u, v, u_range: tuple[float, float], v_range: tuple[float, float], *,
                 step: float = 1.0, major: int = 5, color: str = cfg.GRID, width: float = 1.6,
                 opacity: float = 0.5, fill: str | None = None, fill_opacity: float = 0.0,
                 bias: float = -1e4) -> None:
        super().__init__()
        self.bias = bias
        origin, u, v = (np.asarray(x, dtype=float) for x in (origin, u, v))
        minor, major_pts = [], []
        for k, a in enumerate(np.arange(u_range[0], u_range[1] + 1e-9, step)):
            pair = [origin + u * a + v * v_range[0], origin + u * a + v * v_range[1]]
            (major_pts if major and k % major == 0 else minor).extend(pair)
        for k, b in enumerate(np.arange(v_range[0], v_range[1] + 1e-9, step)):
            pair = [origin + v * b + u * u_range[0], origin + v * b + u * u_range[1]]
            (major_pts if major and k % major == 0 else minor).extend(pair)
        self.minor_pts, self.major_pts = np.array(minor), np.array(major_pts) if major_pts else np.zeros((0, 3))
        self.corners = np.array([origin + u * u_range[0] + v * v_range[0], origin + u * u_range[1] + v * v_range[0],
                                 origin + u * u_range[1] + v * v_range[1], origin + u * u_range[0] + v * v_range[1]])
        self.opacity, self.fill_opacity = opacity, fill_opacity
        self.panel = VMobject(stroke_width=0, fill_color=fill or color, fill_opacity=fill_opacity)
        self.minor = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
        self.major = VMobject(stroke_color=mu.mix(color, cfg.WHITE, 0.25), stroke_width=width * 1.7,
                              stroke_opacity=min(opacity * 1.4, 1.0), fill_opacity=0)
        self.mob = VGroup(self.panel, self.minor, self.major)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        screen, _, depth = stage.project(self.corners, R)
        self.depth_key = float(depth.mean())
        self.panel.set_points_as_corners([*screen, screen[0]])
        self.minor.points = _segments_as_points(stage.project(self.minor_pts, R)[0])
        if len(self.major_pts):
            self.major.points = _segments_as_points(stage.project(self.major_pts, R)[0])
        self.panel.set_fill(opacity=self.fill_opacity * visibility)
        self.minor.set_stroke(opacity=self.opacity * visibility)
        self.major.set_stroke(opacity=min(self.opacity * 1.4, 1.0) * visibility)


class Curve(Body):
    """A glowing polyline through 3D points (an array, or a function returning one).

    ``fill`` closes and fills it (a running track); ``dashed`` draws a guide."""

    def __init__(self, points, color: str, *, width: float = 5.0, glow: bool = True, opacity: float = 1.0,
                 fill: str | None = None, fill_opacity: float = 0.0, dashed: bool = False, bias: float = 0.0) -> None:
        super().__init__()
        self.points, self.bias, self.opacity, self.dashed = points, bias, opacity, dashed
        self.fill_opacity = fill_opacity
        self.area = VMobject(stroke_width=0, fill_color=fill or color, fill_opacity=fill_opacity)
        spread = ((width * 4.2, 0.10), (width * 2.2, 0.22)) if glow else ()
        self.layers = [VMobject(stroke_color=color, stroke_width=w, stroke_opacity=o, fill_opacity=0) for w, o in spread]
        self.core = VMobject(stroke_color=mu.mix(color, cfg.WHITE, 0.2), stroke_width=width, fill_opacity=0)
        self.alphas = [o for _, o in spread] + [1.0]
        self.mob = VGroup(self.area, *self.layers, self.core)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        pts = np.asarray(_value(self.points), dtype=float)
        if len(pts) < 2:
            for m in (self.area, *self.layers, self.core):
                m.points = np.zeros((0, 3))
            self.depth_key = -1e9
            return
        screen, _, depth = stage.project(pts, R)
        self.depth_key = float(depth.mean())
        if self.dashed:
            pairs = []
            for p, q in zip(screen[:-1], screen[1:]):
                pairs.extend([p, p + (q - p) * 0.55])
            path = _segments_as_points(np.array(pairs))
            for m in (*self.layers, self.core):
                m.points = path
        else:
            for m in (*self.layers, self.core):
                m.set_points_as_corners(screen)
        if self.fill_opacity:
            self.area.set_points_as_corners([*screen, screen[0]])
        for m, a in zip((*self.layers, self.core), self.alphas):
            m.set_stroke(opacity=a * self.opacity * visibility)
        self.area.set_fill(opacity=self.fill_opacity * visibility)


class Disc(Body):
    """A flat circle in the plane through ``centre`` with ``normal``: a soft
    shadow (``soft``: feathered layers), or a translucent rotor or marker."""

    SAMPLES = 40

    def __init__(self, centre, radius, color: str, *, normal=(0.0, 1.0, 0.0), opacity: float = 0.5,
                 soft: bool = False, stroke: str | None = None, bias: float = 0.0) -> None:
        super().__init__()
        self.centre, self.radius, self.opacity, self.bias = centre, radius, opacity, bias
        frame = mu.frame_from_axis(normal)
        angles = np.linspace(0, 2 * np.pi, self.SAMPLES, endpoint=False)
        self.ring = np.outer(np.cos(angles), frame[:, 0]) + np.outer(np.sin(angles), frame[:, 1])
        self.scales = (1.0, 0.78, 0.55) if soft else (1.0,)
        self.weights = (0.4, 0.45, 0.6) if soft else (1.0,)
        self.layers = [VMobject(stroke_width=0, fill_color=color, fill_opacity=opacity) for _ in self.scales]
        self.edge = VMobject(stroke_color=stroke or color, stroke_width=2.5 if stroke else 0, fill_opacity=0)
        self.mob = VGroup(*self.layers, self.edge)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        centre, radius = _vec(self.centre), float(_value(self.radius))
        screen_c, _, depth = stage.project(centre[None, :], R)
        self.depth_key = float(depth[0])
        for layer, s, w in zip(self.layers, self.scales, self.weights):
            screen = stage.project(centre + self.ring * radius * s, R)[0]
            layer.set_points_as_corners([*screen, screen[0]])
            layer.set_fill(opacity=self.opacity * w * visibility if len(self.scales) > 1 else self.opacity * visibility)
        if self.edge.stroke_width:
            screen = stage.project(centre + self.ring * radius, R)[0]
            self.edge.set_points_as_corners([*screen, screen[0]])
            self.edge.set_stroke(opacity=visibility)


# ----------------------------------------------------------------------------
# Solids and strips (Episode 02: cars, tracks, a satellite)
# ----------------------------------------------------------------------------

# Corner index = 4*(x>0) + 2*(y>0) + (z>0); each face lists its corners in a cycle.
_BOX_FACES = (
    ((1.0, 0.0, 0.0), (4, 5, 7, 6)), ((-1.0, 0.0, 0.0), (0, 2, 3, 1)),
    ((0.0, 1.0, 0.0), (2, 6, 7, 3)), ((0.0, -1.0, 0.0), (0, 1, 5, 4)),
    ((0.0, 0.0, 1.0), (1, 3, 7, 5)), ((0.0, 0.0, -1.0), (0, 4, 6, 2)),
)
_BOX_SIGNS = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)], dtype=float)
_LIGHT = mu.unit([-0.45, 0.78, 0.5])


class Block(Body):
    """A lit box that turns with a heading: a car body, a cabin, a wheel, a satellite bus.

    ``centre`` and ``heading`` may be values or zero-argument functions.
    ``size`` is (length along the heading, height, width). The heading is
    an angle in the ground plane measured counterclockwise *seen from above*,
    so heading 0 points along +x and heading pi/2 along -z (away from the
    viewer), matching ``common.ground``. Faces turned away from the eye are
    skipped; the rest are shaded by a light from the upper left."""

    def __init__(self, centre, size, color: str, heading=0.0, *, opacity: float = 1.0,
                 edge: str | None = None) -> None:
        super().__init__()
        self.centre, self.heading, self.opacity = centre, heading, opacity
        self.half = np.asarray(size, dtype=float) / 2
        self.rgb = np.array(ManimColor(color).to_rgb())
        edge_color = edge or mu.shade(color, 0.45)
        self.faces = [VMobject(stroke_color=edge_color, stroke_width=1.2, fill_opacity=opacity) for _ in _BOX_FACES]
        self.mob = VGroup(*self.faces)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        c = _vec(self.centre)
        Rh = mu.rotation_y(float(_value(self.heading)))
        corners = c + (_BOX_SIGNS * self.half) @ Rh.T
        screen, _, depth = stage.project(corners, R)
        view = corners @ R.T
        eye = np.array([0.0, 0.0, stage.distance])
        self.depth_key = float(depth.mean())
        order = []
        for k, ((normal, idx), face) in enumerate(zip(_BOX_FACES, self.faces)):
            n_view = R @ (Rh @ np.asarray(normal))
            middle = view[list(idx)].mean(axis=0)
            if float(np.dot(n_view, eye - middle)) <= 1e-6:
                face.points = np.zeros((0, 3))
                continue
            face.set_points_as_corners([*screen[list(idx)], screen[idx[0]]])
            light = 0.42 + 0.58 * max(0.0, float(np.dot(n_view, _LIGHT)))
            face.set_fill(ManimColor(np.clip(self.rgb * light, 0, 1)), opacity=self.opacity * visibility)
            face.set_stroke(opacity=0.8 * visibility)
            order.append((float(middle[2]), k))
        self.mob.submobjects = [self.faces[k] for _, k in sorted(order)]


class Band(Body):
    """A flat strip along a centre line in the ground plane: a road or a running track.

    ``points`` is an (n, 3) array (or a function returning one). A closed band
    is an annulus (the inner edge is reversed, so it cuts a hole); an open band
    is a single strip. Edge lines and a dashed centre line are optional."""

    def __init__(self, points, half_width: float, color: str, *, closed: bool = True, opacity: float = 0.9,
                 edge: str | None = None, edge_opacity: float = 0.8, centre_line: str | None = None,
                 bias: float = -0.95e4) -> None:
        super().__init__()
        self.points, self.w, self.closed, self.opacity = points, half_width, closed, opacity
        self.edge_opacity, self.bias = edge_opacity, bias
        self.area = VMobject(stroke_width=0, fill_color=color, fill_opacity=opacity)
        self.edges = VMobject(stroke_color=edge or mu.mix(color, cfg.WHITE, 0.5), stroke_width=2.2 if edge else 0,
                              fill_opacity=0)
        self.dashes = VMobject(stroke_color=centre_line or cfg.WHITE, stroke_width=2.4 if centre_line else 0,
                               fill_opacity=0)
        self.mob = VGroup(self.area, self.edges, self.dashes)

    def _edges(self, pts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        if self.closed:
            tangent = np.roll(pts, -1, axis=0) - np.roll(pts, 1, axis=0)
        else:
            tangent = np.gradient(pts, axis=0)
        side = np.cross(tangent, np.array([0.0, 1.0, 0.0]))
        side /= np.maximum(np.linalg.norm(side, axis=1, keepdims=True), 1e-9)
        return pts + side * self.w, pts - side * self.w

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        pts = np.asarray(_value(self.points), dtype=float)
        outer, inner = self._edges(pts)
        so = stage.project(outer, R)[0]
        si = stage.project(inner, R)[0]
        self.depth_key = float(stage.project(pts, R)[2].mean())
        if self.closed:
            self.area.set_points_as_corners([*so, so[0]])
            self.area.start_new_path(si[-1])
            self.area.add_points_as_corners([*si[::-1][1:], si[-1]])
        else:
            self.area.set_points_as_corners([*so, *si[::-1], so[0]])
        if self.edges.stroke_width:
            self.edges.set_points_as_corners([*so, so[0]] if self.closed else list(so))
            self.edges.start_new_path(si[0])
            self.edges.add_points_as_corners([*si[1:], si[0]] if self.closed else list(si[1:]))
        if self.dashes.stroke_width:
            centre = stage.project(pts, R)[0]
            pairs = []
            for k in range(0, len(centre) - 1, 2):
                pairs.extend([centre[k], centre[k] + (centre[k + 1] - centre[k]) * 0.9])
            self.dashes.points = _segments_as_points(np.array(pairs))
        self.area.set_fill(opacity=self.opacity * visibility)
        self.edges.set_stroke(opacity=self.edge_opacity * visibility)
        self.dashes.set_stroke(opacity=0.55 * visibility)
