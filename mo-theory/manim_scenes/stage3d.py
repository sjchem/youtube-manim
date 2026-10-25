"""A projected 3D stage: real rotating geometry, drawn as smooth 2D shapes.

Every molecule and orbital in the film lives on a ``Stage``.
Bodies keep true 3D coordinates; each frame the stage turns them (yaw about
the vertical, pitch toward the viewer, an optional model rotation), projects
them with a gentle perspective, sorts them back to front, and redraws them:

* ``Ball``   — an atom: a polished sphere of nested shading contours, with an
  optional element symbol that turns with it;
* ``Rod``    — a bond between two balls, a layered cylinder; double and triple
  bonds split into parallel strands in screen space so they always read;
* ``Lobe``   — a translucent ellipsoid along a direction. The outline of a
  projected ellipsoid is computed exactly (``mu.projected_ellipse``);
* ``Blob``   — an orbital lobe: the silhouette of a computed |psi| = level
  surface (``utils.orbital_models``), shaded with nested contours;
* ``Segment`` and ``Face`` — guide lines, translucent nodal planes;
* ``Fog``    — electron density as a cloud of fine dots sampled from |psi|^2;
* overlay items that are never hidden: ``Vector`` (arrows), ``Tag`` (text or spin arrows pinned to a 3D point).

Why not ``ThreeDScene``? Cairo draws ThreeDScene surfaces as faceted meshes,
and fixed-in-frame captions in Manim CE have known pitfalls (stray glyph
copies, captions dragged by frame_center moves). The stage keeps every
caption a plain 2D object, keeps spheres perfectly smooth, and is cheap
enough to keep every model slowly turning, so no shot is ever static.

Stage state is changed only through ``Param`` animations (never ``.animate``
or Transform on the stage — those would copy a live object; see the
AnimationGroup / live-object notes in ``common.py``).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from manim import ORIGIN, UL, Animation, Circle, Dot, ManimColor, Mobject, Text, VGroup, VMobject, interpolate_color

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


class Lobe(Body):
    """A translucent ellipsoid pointing out of an origin along ``direction``.

    ``length`` and ``width`` are full length and half-width (screen units);
    ``grow`` (0..1) scales the lobe out from the origin, for regions that
    appear or retract.
    """

    def __init__(self, origin, direction, length: float, width: float, color: str, *, start: float = 0.12,
                 body_opacity: float = 0.26, rim_opacity: float = 0.75, grow: float = 1.0) -> None:
        super().__init__()
        self.origin, self.direction = origin, direction
        self.length, self.width, self.start, self.grow = float(length), float(width), float(start), float(grow)
        self.color = color
        light = mu.mix(color, cfg.WHITE, 0.45)
        self.parts = [
            Circle(radius=1.08, stroke_width=0, fill_color=color, fill_opacity=0.045),
            Circle(radius=1.0, stroke_width=0, fill_color=color, fill_opacity=body_opacity),
        ]
        self.offsets = [np.zeros(2), np.zeros(2)]
        for fraction in np.linspace(0.94, 0.12, 16):
            self.parts.append(Circle(radius=fraction, stroke_width=0, fill_color=light,
                                     fill_opacity=0.028))
            self.offsets.append(np.array([-0.16, 0.18]) * (1 - fraction))
        self.parts.append(Circle(radius=1.0, stroke_color=light, stroke_width=1.8,
                                 stroke_opacity=rim_opacity * 0.7, fill_opacity=0))
        self.offsets.append(np.zeros(2))
        self.templates = [p.points.copy() for p in self.parts]
        self.fill_alpha = [p.fill_rgbas[:, 3].copy() for p in self.parts]
        self.stroke_alpha = [p.stroke_rgbas[:, 3].copy() for p in self.parts]
        self.mob = VGroup(*self.parts)

    def axis(self) -> np.ndarray:
        return mu.unit(_vec(self.direction))

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        d = self.axis()
        grow = max(self.grow, 1e-3)
        length = self.length * grow
        width = self.width * (0.25 + 0.75 * grow)
        centre = _vec(self.origin) + d * (self.start * grow + length / 2)
        frame = mu.frame_from_axis(d)
        axes = R @ np.column_stack([frame[:, 0] * width, frame[:, 1] * width, d * length / 2])
        screen, size, depth = stage.project(centre[None, :], R)
        M = mu.projected_ellipse(axes) * size[0]
        c2 = screen[0, :2]
        for part, template, offset in zip(self.parts, self.templates, self.offsets):
            pts = template.copy()
            local = template[:, :2]
            pts[:, :2] = local @ M.T + offset @ M.T + c2
            pts[:, 2] = 0
            part.points = pts
        self.depth_key = depth[0]
        if self._alpha_cache != visibility:
            for part, fa, sa in zip(self.parts, self.fill_alpha, self.stroke_alpha):
                part.fill_rgbas[:, 3] = fa * visibility
                part.stroke_rgbas[:, 3] = sa * visibility
            self._alpha_cache = visibility


class Blob(Body):
    """An orbital lobe drawn from its computed surface points.

    ``maker()`` returns (N, 3) points in orbital units around the nucleus
    (or None while the lobe does not exist); they are scaled by ``units``
    and placed at ``origin``. The silhouette is the convex hull of the
    projected points, shaded with nested contours toward the light.
    """

    def __init__(self, maker: Callable[[], np.ndarray | None], origin, color: str, *, units: float = 0.5,
                 opacity: float = 0.9, layers: int = 24, focus: Callable[[], np.ndarray] | None = None) -> None:
        super().__init__()
        self.maker, self.origin, self.units, self.color = maker, origin, float(units), color
        self.focus = focus
        base = np.array(ManimColor(color).to_rgb())
        self.base = VMobject(stroke_color=mu.mix(color, cfg.WHITE, 0.55), stroke_width=2.6, fill_color=ManimColor(base * 0.78))
        self.layers = []
        for fraction in np.linspace(0.9, 0.14, layers):
            brightness = 0.8 + 0.4 * np.sqrt(1 - fraction ** 2)
            tone = ManimColor(np.clip(base * brightness + 0.3 * (1 - fraction) ** 2, 0, 1))
            self.layers.append((fraction, VMobject(stroke_width=0, fill_color=tone)))
        self.parts = [self.base] + [layer for _, layer in self.layers]
        self.mob = VGroup(*self.parts)
        self.opacity = opacity
        self._apply_alpha(1.0)

    def _apply_alpha(self, visibility: float) -> None:
        """Split the target opacity between the rim-to-rim base and the
        nested shading layers, so the centre reaches ``opacity`` and the
        edge stays readable instead of the stack turning solid."""
        target = self.opacity * visibility
        base = 0.48 * target
        n = len(self.layers)
        each = 1 - ((1 - target) / max(1 - base, 1e-6)) ** (1 / n) if target < 0.999 else 1.0
        self.base.set_fill(opacity=base).set_stroke(opacity=min(1.0, 0.9 * visibility))
        for _, layer in self.layers:
            layer.set_fill(opacity=max(each, 0.0))

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        local = self.maker()
        if local is None or len(local) < 4:
            for part in self.parts:
                part.points = np.zeros((0, 3))
            self.depth_key = -1e9
            return
        origin = _vec(self.origin)
        world = origin + np.asarray(local) * self.units
        screen, size, depth = stage.project(world, R)
        hull = mu.convex_hull_2d(screen[:, :2])
        if len(hull) < 3:
            for part in self.parts:
                part.points = np.zeros((0, 3))
            return
        extent = np.ptp(hull, axis=0)
        if self.focus is not None:
            # Light the lobe toward its own tip: the glow shows which way it points.
            light = stage.project(_vec(self.focus)[None, :], R)[0][0, :2]
        else:
            light = hull.mean(axis=0)
        light = light + np.array([-0.12, 0.14]) * extent
        hull = _round_outline(hull)
        closed = np.vstack([hull, hull[:1]])
        pad = np.zeros((len(closed), 1))
        # A smooth curve through the hull vertices hides the faceting of the sampled
        # surface. Each shading layer is that curve scaled toward the light point;
        # scaling is affine, so the smoothed control points can simply be scaled.
        self.base.set_points_smoothly(np.hstack([closed, pad]))
        smooth = self.base.points
        focus = np.array([light[0], light[1], 0.0])
        for fraction, layer in self.layers:
            layer.points = focus + (smooth - focus) * fraction
        self.depth_key = float(depth.mean())
        if self._alpha_cache != visibility:
            self._apply_alpha(visibility)
            self._alpha_cache = visibility


def _round_outline(hull: np.ndarray, count: int = 56, passes: int = 3) -> np.ndarray:
    """Resample a convex outline at equal arc length and relax it a little, so
    the hull of a sampled surface reads as a smooth curve, not a polygon."""
    ring = np.vstack([hull, hull[:1]])
    seg = np.linalg.norm(np.diff(ring, axis=0), axis=1)
    total = float(seg.sum())
    if total < 1e-9:
        return hull
    along = np.concatenate([[0.0], np.cumsum(seg)])
    ts = np.linspace(0, total, count, endpoint=False)
    pts = np.column_stack([np.interp(ts, along, ring[:, 0]), np.interp(ts, along, ring[:, 1])])
    for _ in range(passes):
        pts = 0.5 * pts + 0.25 * (np.roll(pts, 1, axis=0) + np.roll(pts, -1, axis=0))
    # Relaxation shrinks a convex curve slightly; restore its extent about the centre.
    centre = pts.mean(axis=0)
    spread = np.ptp(hull, axis=0) / np.maximum(np.ptp(pts, axis=0), 1e-9)
    return centre + (pts - centre) * spread


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


class Fog(Body):
    """Electron density as fine dots: fixed sample points (orbital units, from
    ``utils.orbital_models``) drawn at ``origin`` with a shared colour."""

    def __init__(self, points: np.ndarray, origin, color: str, *, units: float = 0.5, radius: float = 0.022,
                 opacity: float = 0.75) -> None:
        super().__init__()
        self.local = np.asarray(points, dtype=float)
        self.origin, self.units, self.opacity = origin, float(units), float(opacity)
        template = Circle(radius=1.0, stroke_width=0, fill_color=color, fill_opacity=1, num_components=5)
        self.template = template.points.copy()
        self.radius = radius
        self.dots = [template.copy() for _ in range(len(self.local))]
        self.mob = VGroup(*self.dots)

    def place(self, stage: "Stage", R: np.ndarray, visibility: float) -> None:
        world = _vec(self.origin) + self.local * self.units
        screen, size, depth = stage.project(world, R)
        # Nearer dots draw a little larger and brighter, which reads as depth.
        near = np.clip(0.55 + 0.45 * (depth - depth.min()) / max(np.ptp(depth), 1e-6), 0, 1)
        for dot, centre, s, n in zip(self.dots, screen, size, near):
            dot.points = self.template * (self.radius * s) + centre
            dot.fill_rgbas[:, 3] = self.opacity * visibility * n
        self.depth_key = float(depth.mean())


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
