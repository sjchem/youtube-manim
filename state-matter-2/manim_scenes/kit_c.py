"""Shared pieces for scenes 11-15 (real-gas deviations and the van der Waals equation).

* ``word_cue`` holds until a word of the current narration beat is spoken, so a
  label lands on the word that names it;
* ``CollidingSpheres`` is ``pm.HardSphereGas`` that also reports where two
  spheres touch, and ``ContactFlashes`` turns those contacts into small red
  flashes (size and repulsion are red);
* ``PairLinks`` joins nearby molecules with green lines (attraction is green),
  either live (every pair closer than a cutoff) or for a fixed list of pairs;
* ``vdw_terms`` splits the van der Waals ratio P_real / P_ideal into its two
  rival terms: the push of size and the pull of attraction;
* ``BallisticPoint`` is a point (a molecule's centre) flying among fixed
  hard spheres: it reflects off each forbidden sphere of radius d;
* ``SphereGas`` is a handful of molecules flying inside a round flask.
"""

from __future__ import annotations

import narration
from manim_scenes.common import *
from manim_scenes.common import TimedFlashes
from manim_scenes.stage3d import Body, _segments_as_points, _value


# ----------------------------------------------------------------------------
# Timing inside a beat
# ----------------------------------------------------------------------------


def word_time(key: str, index: int, word: str, nth: int = 1) -> float:
    """Seconds into the scene at which ``word`` (its ``nth`` occurrence) of beat ``index`` is spoken."""
    start_at, text = SCRIPT[key][index]
    tokens = [w.lower() for w in narration._WORD.findall(text)]
    seen = 0
    for k, token in enumerate(tokens):
        if token == word.lower():
            seen += 1
            if seen == nth:
                return start_at + k / narration.PACE
    raise ValueError(f"'{word}' not in beat {index} of scene {key}")


def word_cue(scene: Scene, started_at: float, index: int, word: str, nth: int = 1, lead: float = 0.2) -> None:
    """Hold until a word of beat ``index`` is about to be spoken (a late cue simply passes)."""
    remaining = word_time(scene._project_scene_key, index, word, nth) - lead - (float(scene.time) - started_at)
    if remaining > 2.0 / float(scene.camera.frame_rate):
        scene.wait(remaining)


def fill_to(scene: Scene, started_at: float, upto: int, *animations, margin: float = 0.06, **kwargs) -> None:
    """Play ``animations`` stretched over all the time left before beat ``upto``."""
    left = time_left(scene, started_at, upto) - margin
    if left > 2.0 / float(scene.camera.frame_rate):
        scene.play(*animations, run_time=left, **kwargs)


# ----------------------------------------------------------------------------
# Hard spheres that report their collisions
# ----------------------------------------------------------------------------


class CollidingSpheres(pm.HardSphereGas):
    """``pm.HardSphereGas`` that logs the midpoint (box coordinates) of every sphere-sphere contact."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.contacts: list[np.ndarray] = []

    def advance(self, dt: float, extent, speed: float, heat: float = 1.0) -> list[tuple[int, int, int]]:
        steps = max(1, int(np.ceil(dt / self.max_step - 1e-9)))
        h = dt / steps
        touch = (2 * self.radius) ** 2 * (1 + 1e-6)
        hits: list[tuple[int, int, int]] = []
        for _ in range(steps):
            hits += super().advance(h, extent, speed, heat)
            d = self.pos[:, None, :] - self.pos[None, :, :]
            i, j = np.nonzero(np.triu((d * d).sum(-1) <= touch, 1))
            self.contacts.extend((self.pos[i] + self.pos[j]) / 2)
        del self.contacts[:-120]
        return hits

    def drain(self) -> list[np.ndarray]:
        out, self.contacts = self.contacts, []
        return out


class ContactFlashes(TimedFlashes):
    """Small red flashes where two spheres of a ``GasBox`` (built on ``CollidingSpheres``) bounce apart."""

    def __init__(self, box: GasBox, color: str = cfg.REPEL, size: float = 0.75) -> None:
        super().__init__(color, size)
        self.box = box

    def place(self, stage, R, visibility):
        lo = self.box.region.lo()
        for point in self.box.gas.drain():
            if self.presence > 0.05:
                self.spark(lo + point, 2)
        super().place(stage, R, visibility)


# ----------------------------------------------------------------------------
# Green attraction links between nearby molecules
# ----------------------------------------------------------------------------


class PairLinks(Body):
    """Green lines joining pairs of molecules: every pair closer than ``cutoff``
    (recomputed each frame from ``points``), or a fixed list of ``pairs``.

    Drawn as one batched shape just behind the molecules (``bias``); ``count``
    holds the number of links drawn in the last frame."""

    def __init__(self, points, cutoff: float = 1.0, color: str = cfg.ATTRACT, *, pairs=None, width: float = 3.2,
                 opacity: float = 0.8, bias: float = -0.4, fade: bool = True) -> None:
        super().__init__()
        self.points, self.cutoff, self.opacity, self.bias, self.fade = points, float(cutoff), opacity, bias, fade
        self.pairs = None if pairs is None else np.asarray(pairs, dtype=int).reshape(-1, 2)
        self.glow = VMobject(stroke_color=color, stroke_width=width * 3.2, fill_opacity=0)
        self.near = VMobject(stroke_color=mu.mix(color, cfg.WHITE, 0.15), stroke_width=width, fill_opacity=0)
        self.far = VMobject(stroke_color=color, stroke_width=width * 0.7, fill_opacity=0)
        self.mob = VGroup(self.glow, self.far, self.near)
        self.count = 0

    def links(self, pts: np.ndarray) -> np.ndarray:
        if self.pairs is not None:
            return self.pairs
        d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)
        i, j = np.nonzero(np.triu(d < self.cutoff, 1))
        return np.column_stack([i, j])

    def place(self, stage, R, visibility):
        pts = np.asarray(_value(self.points), dtype=float).reshape(-1, 3)
        ij = self.links(pts) if len(pts) > 1 else np.zeros((0, 2), dtype=int)
        self.count = len(ij)
        if not len(ij):
            for m in (self.glow, self.near, self.far):
                m.points = np.zeros((0, 3))
            self.depth_key = -1e9
            return
        a, b = pts[ij[:, 0]], pts[ij[:, 1]]
        close = np.linalg.norm(a - b, axis=1) < 0.72 * self.cutoff if self.fade else np.ones(len(ij), dtype=bool)
        for mob, mask in ((self.near, close), (self.far, ~close)):
            if mask.any():
                ends = np.empty((2 * int(mask.sum()), 3))
                ends[0::2], ends[1::2] = a[mask], b[mask]
                mob.points = _segments_as_points(stage.project(ends, R)[0])
            else:
                mob.points = np.zeros((0, 3))
        self.glow.points = np.concatenate([self.near.points, self.far.points]) if len(ij) else np.zeros((0, 3))
        self.depth_key = float(stage.project(np.concatenate([a, b]), R)[2].mean())
        self.near.set_stroke(opacity=self.opacity * visibility)
        self.far.set_stroke(opacity=0.45 * self.opacity * visibility)
        self.glow.set_stroke(opacity=0.12 * self.opacity * visibility)


# ----------------------------------------------------------------------------
# The van der Waals tug of war, term by term
# ----------------------------------------------------------------------------


def vdw_terms(P_bar: float, T: float, gas: str) -> tuple[float, float, float]:
    """(size push, attraction pull, P_real / P_ideal) of the van der Waals gas at ``P_bar`` and ``T``.

    At the gas's own molar volume V, P_real / P_ideal = V / (V - b) - a / (R T V)
    = 1 + b / (V - b) - a / (R T V): size adds the first term, attraction takes the second."""
    if P_bar <= 0:
        return 0.0, 0.0, 1.0
    a, b = pm.VDW[gas]
    ratio = pm.z_vdw(P_bar, T, gas)
    Vm = ratio * pm.R_L_BAR * T / P_bar
    return b / (Vm - b), a / (pm.R_L_BAR * T * Vm), ratio


# ----------------------------------------------------------------------------
# A molecule's centre among fixed hard spheres
# ----------------------------------------------------------------------------


def ballistic_path(obstacles: np.ndarray, d: float, half: float, start, velocity, seconds: float,
                   dt: float = 1 / 240) -> np.ndarray:
    """Positions (every ``dt``) of a point flying among forbidden spheres of radius ``d`` around ``obstacles``
    inside the cube |x| <= ``half``: it reflects specularly off every sphere and wall."""
    p = np.asarray(start, dtype=float).copy()
    v = np.asarray(velocity, dtype=float).copy()
    out = [p.copy()]
    for _ in range(int(round(seconds / dt))):
        p = p + v * dt
        for axis in range(3):
            if abs(p[axis]) > half:
                p[axis] = np.sign(p[axis]) * (2 * half - abs(p[axis]))
                v[axis] = -v[axis]
        gap = p[None, :] - obstacles
        dist = np.linalg.norm(gap, axis=1)
        for k in np.nonzero(dist < d)[0]:
            n = gap[k] / max(dist[k], 1e-9)
            if np.dot(v, n) < 0:
                v = v - 2 * np.dot(v, n) * n
            p = obstacles[k] + n * d
        out.append(p.copy())
    return np.array(out)


class SphereGas:
    """``count`` molecules flying inside a sphere of (live) radius ``radius()`` about ``centre``,
    reflecting off its inside; ``points()`` is their current position (call once per frame via a Ticker)."""

    def __init__(self, count: int, seed: int, radius, centre=ORIGIN, speed: float = 1.2, size: float = 0.08) -> None:
        rng = np.random.default_rng(seed)
        self.radius = radius
        self.centre = np.asarray(centre, dtype=float)
        self.size, self.speed = float(size), float(speed)
        u = rng.normal(size=(count, 3))
        self.frac = (u / np.linalg.norm(u, axis=1, keepdims=True)) * rng.uniform(0, 1, (count, 1)) ** (1 / 3) * 0.9
        self.v = rng.normal(scale=1 / np.sqrt(3), size=(count, 3))
        self.last = None

    def step(self, clock: float) -> None:
        if self.last is None:
            self.last = clock
        dt = min(max(clock - self.last, 0.0), 0.3)
        self.last = clock
        R = float(_value(self.radius))
        limit = max(1.0 - self.size / max(R, 1e-6), 0.2)
        n = max(1, int(np.ceil(dt / (1 / 120))))
        for _ in range(n):
            self.frac += self.v * self.speed * (dt / n) / max(R, 1e-6)
            out = np.linalg.norm(self.frac, axis=1)
            hit = out > limit
            if hit.any():
                normal = self.frac[hit] / out[hit, None]
                along = (self.v[hit] * normal).sum(1, keepdims=True)
                self.v[hit] -= 2 * np.maximum(along, 0) * normal
                self.frac[hit] = normal * limit

    def points(self) -> np.ndarray:
        return self.centre + self.frac * float(_value(self.radius))


# ----------------------------------------------------------------------------
# Small builders
# ----------------------------------------------------------------------------


def bar_meter(value: Callable[[], float], at, color: str, *, top: float, height: float = 3.4, width: float = 0.72,
              smooth_s: float = 0.5) -> VGroup:
    """A vertical bar from ``at`` (its base centre) whose height follows ``value()`` (smoothed), up to ``top``."""
    base = np.asarray(at, dtype=float)
    bar = Rectangle(width=width, height=0.05, stroke_color=mu.mix(color, cfg.WHITE, 0.3), stroke_width=2,
                    fill_color=color, fill_opacity=0.85)
    glow = Rectangle(width=width + 0.22, height=0.05, stroke_width=0, fill_color=color, fill_opacity=0.14)
    group = VGroup(glow, bar)
    group.level = Knob(float(value()))

    def follow(m, dt):
        group.level.value += (float(value()) - group.level.value) * (1 - np.exp(-dt / smooth_s)) if dt > 0 else 0.0
        h = float(np.clip(group.level.value / top, 0.0, 1.0)) * height
        for part, pad in ((bar, 0.0), (glow, 0.11)):
            part.stretch_to_fit_height(max(h + pad, 0.03))
            part.move_to(base + UP * (h + pad) / 2)

    group.add_updater(follow)
    follow(group, 0)
    group.tip = lambda: base + UP * float(np.clip(group.level.value / top, 0.0, 1.0)) * height
    return group


def live_number(value: Callable[[], float], place: Callable[[Mobject], Mobject], size: int = 40,
                color: str = cfg.WHITE, decimals: int = 0, prefix: str = "", suffix: str = "") -> VGroup:
    """A number rebuilt every frame as plain text (so it never changes digit count inside a DecimalNumber).

    Fade it with ``set_attr(group, group, "alpha", v)`` rather than FadeIn/FadeOut."""
    group = VGroup()
    group.alpha = 0.0

    def rebuild(m):
        label = txt(prefix + fx(float(value()), decimals) + suffix, size, color)
        label.set_opacity(m.alpha)
        label.set_stroke(cfg.BG, width=0.75, opacity=0.85 * m.alpha, background=True)
        m.submobjects = [place(label)]

    group.add_updater(rebuild)
    rebuild(group)
    return group
