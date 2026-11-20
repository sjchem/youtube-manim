"""Shared helpers for scenes 02, 08, 09 and 10 (agent A).

* ``rule_chip`` — a numbered postulate chip of the kinetic molecular theory
  (scene 08 lays out six; scene 09 brings two back and ``crack``s them);
* ``Vec3`` — a tweenable 3D point (a camera that flies along a path);
* ``ShiftGrid`` — a floor grid that slides with such a camera;
* ``Bouncers`` — a flat box of dots bouncing off its walls (2D icons);
* ``ticking`` — a plain 2D group that keeps its own clock (live icons).
"""

from __future__ import annotations

from manim_scenes.common import *
from manim_scenes.stage3d import _segments_as_points

RULE_COLOR = cfg.LIMIT        # idealised assumptions are purple


# ----------------------------------------------------------------------------
# Postulate chips
# ----------------------------------------------------------------------------


def rule_chip(number: int, body: str | Mobject, color: str = RULE_COLOR, size: int | None = None,
              width: float | None = None) -> VGroup:
    """A rounded pill: a numbered badge, then a short (possibly two-line) rule."""
    size = size or cfg.FONT["small"]
    label = body if isinstance(body, Mobject) else txt(body, size, cfg.WHITE)
    badge_ring = Circle(radius=0.3, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.28)
    numeral = txt(str(number), size, cfg.WHITE).move_to(badge_ring)
    badge = VGroup(badge_ring, numeral)
    inner = VGroup(badge, label).arrange(RIGHT, buff=0.26)
    w = max(inner.width + 0.56, width or 0.0)
    pill = RoundedRectangle(width=w, height=max(inner.height, 0.6) + 0.36, corner_radius=0.24,
                            stroke_color=color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.92)
    inner.move_to(pill).align_to(pill, LEFT).shift(RIGHT * 0.28)
    glow = pill.copy().set_fill(opacity=0).set_stroke(color, width=14, opacity=0.0)
    group = VGroup(glow, pill, inner)
    group.glow, group.pill, group.badge, group.label, group.numeral = glow, pill, badge, label, numeral
    group.tone = color
    return group


def chip_focus(chip_: VGroup, on: bool) -> list[Animation]:
    """Brighten the chip being explained, quieten the others."""
    if on:
        return [chip_.glow.animate.set_stroke(opacity=0.22), chip_.pill.animate.set_stroke(opacity=1.0)]
    return [chip_.glow.animate.set_stroke(opacity=0.0), chip_.pill.animate.set_stroke(opacity=0.45)]


def crack(chip_: VGroup, color: str = cfg.WARNING, seed: int = 0) -> tuple[VGroup, list[Animation]]:
    """A jagged red crack across a chip; returns the crack and the animations that turn the chip red."""
    rng = np.random.default_rng(cfg.SEED + 900 + seed)
    pill = chip_.pill
    left, right = pill.get_left()[0] + 0.15, pill.get_right()[0] - 0.15
    top, bottom = pill.get_top()[1], pill.get_bottom()[1]
    xs = np.linspace(left + 0.4, right - 0.4, 7)
    pts = [np.array([xs[0] - 0.3, top - 0.02, 0])]
    for k, x in enumerate(xs):
        frac = k / (len(xs) - 1)
        y = top + (bottom - top) * frac + rng.uniform(-0.14, 0.14)
        pts.append(np.array([x, float(np.clip(y, bottom + 0.05, top - 0.05)), 0]))
    pts.append(np.array([xs[-1] + 0.3, bottom + 0.02, 0]))
    line = VMobject(stroke_color=color, stroke_width=6).set_points_as_corners(pts)
    glow = line.copy().set_stroke(color, width=16, opacity=0.25)
    mark = VGroup(glow, line)
    anims = [Create(mark), pill.animate.set_stroke(color, opacity=1.0), chip_.glow.animate.set_stroke(color, opacity=0.25),
             chip_.badge[0].animate.set_stroke(color).set_fill(color, opacity=0.3)]
    return mark, anims


# ----------------------------------------------------------------------------
# A camera that flies: every body reads ``point - camera``
# ----------------------------------------------------------------------------


class Vec3:
    """A tweenable 3D vector (``Param`` in vector mode)."""

    def __init__(self, value) -> None:
        self.v = np.asarray(value, dtype=float).copy()

    def to(self, holder: Mobject, value, **kwargs) -> Param:
        return Param(holder, lambda: self.v, lambda v: setattr(self, "v", np.asarray(v, dtype=float)),
                     np.asarray(value, dtype=float), mode="vector", **kwargs)

    def rel(self, point) -> Callable[[], np.ndarray]:
        p = np.asarray(point, dtype=float)
        return lambda: p - self.v


class ShiftGrid(Grid):
    """A ``Grid`` whose lines slide by ``-offset()`` (a camera flying over the floor)."""

    def __init__(self, offset: Callable[[], np.ndarray], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.offset = offset

    def place(self, stage, R, visibility):
        shift = np.asarray(self.offset(), dtype=float)
        screen, _, depth = stage.project(self.corners - shift, R)
        self.depth_key = float(depth.mean())
        self.panel.set_points_as_corners([*screen, screen[0]])
        self.minor.points = _segments_as_points(stage.project(self.minor_pts - shift, R)[0])
        if len(self.major_pts):
            self.major.points = _segments_as_points(stage.project(self.major_pts - shift, R)[0])
        self.panel.set_fill(opacity=self.fill_opacity * visibility)
        self.minor.set_stroke(opacity=self.opacity * visibility)
        self.major.set_stroke(opacity=min(self.opacity * 1.4, 1.0) * visibility)


# ----------------------------------------------------------------------------
# Live 2D icons
# ----------------------------------------------------------------------------


def ticking(group: VGroup, fn: Callable[[float], None]) -> VGroup:
    """Give a plain group its own clock: ``fn(t)`` runs every frame with the elapsed seconds."""
    group.clock = 0.0

    def tick(m, dt):
        m.clock += dt
        fn(m.clock)

    group.add_updater(tick)
    fn(0.0)
    return group


class Bouncers(VGroup):
    """Dots bouncing elastically inside a flat rectangle (an icon of a gas).

    Positions fold a phase that grows linearly in time, so motion is exact and seeded."""

    def __init__(self, centre, width: float, height: float, count: int = 14, *, color: str = cfg.MOLECULE,
                 radius: float = 0.07, speed: float = 0.9, seed: int = 0) -> None:
        super().__init__()
        rng = np.random.default_rng(cfg.SEED + 700 + seed)
        self.centre = np.asarray(centre, dtype=float)
        self.w, self.h, self.r = width, height, radius
        self.phase0 = rng.uniform(0, 2, (count, 2))
        ang = rng.uniform(0, 2 * np.pi, count)
        mag = rng.rayleigh(1.0, count) * speed
        self.vel = np.column_stack([np.cos(ang), np.sin(ang)]) * mag[:, None]
        self.dots = [bead(ORIGIN, color, radius) for _ in range(count)]
        self.add(*self.dots)
        self.clock = 0.0
        self.rate = 1.0
        self.add_updater(lambda m, dt: m.step(dt))
        self.step(0.0)

    def position(self, k: int) -> np.ndarray:
        span = np.array([self.w - 2 * self.r, self.h - 2 * self.r])
        frac = pm.fold(self.phase0[k] + self.vel[k] * self.clock / span)
        xy = self.centre[:2] - span / 2 + frac * span
        return np.array([xy[0], xy[1], 0.0])

    def step(self, dt: float) -> None:
        self.clock += dt * self.rate
        for k, d in enumerate(self.dots):
            d.move_to(self.position(k))


def arrow2d(tail, tip, color: str, width: float = 0.08, tip_len: float = 0.26, opacity: float = 1.0) -> VGroup:
    """A static filled arrow in the film's style (the same outline as a stage Vector)."""
    p, q = np.asarray(tail, dtype=float), np.asarray(tip, dtype=float)
    body = VMobject(stroke_color=mu.shade(color, 0.55), stroke_width=1.5, fill_color=color, fill_opacity=opacity)
    halo = VMobject(stroke_width=0, fill_color=color, fill_opacity=0.12 * opacity)
    outline = arrow_outline(p, q, width, tip_len)
    if outline is not None:
        body.set_points_as_corners(outline)
        halo.set_points_as_corners(arrow_outline(p, q, width * 1.8, tip_len * 1.08))
    return VGroup(halo, body)


def ghost_arrow(tail, tip, color: str = cfg.MUTED, width: float = 0.12, tip_len: float = 0.34) -> DashedVMobject:
    """A dashed outline arrow: what the ideal model would have given."""
    outline = arrow_outline(np.asarray(tail, dtype=float), np.asarray(tip, dtype=float), width, tip_len)
    shape = VMobject(stroke_color=color, stroke_width=3, fill_opacity=0).set_points_as_corners(outline)
    return DashedVMobject(shape, num_dashes=28, dashed_ratio=0.55)
