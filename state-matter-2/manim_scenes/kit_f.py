"""Kit F — shared pieces for scenes 23 and 24 (vapour pressure and boiling).

* ``FluxExchange`` — the film's ``VapourExchange`` with physical velocities:
  a molecule that escapes leaves the surface with a flux-weighted upward
  speed, and vapour molecules keep re-thermalising (they collide with one
  another), so the vapour settles to a clean plateau where evaporation and
  condensation balance. ``fill(n)`` starts a vessel already at equilibrium.
* ``Escapes`` — molecules hopping out of the surface of an *open* vessel:
  inside a thin attraction layer each one is slowed by the pull of the liquid;
  slow ones fall back, fast ones break free (gold flash) and drift away
  through the open top.
* ``Bubbles`` — boiling: vapour bubbles nucleate on the floor of a pool, grow
  as they rise and burst at the surface.
* ``GlassLid`` / ``SteelLid`` — a lid that drops onto a ``TwoPhaseBox``.
"""

from __future__ import annotations

from manim_scenes.common import *

SIGMA = 1 / np.sqrt(3)          # IdealGas velocity units: rms speed 1, so each component has sigma 1/sqrt(3)


# ----------------------------------------------------------------------------
# Evaporation and condensation with physical velocities
# ----------------------------------------------------------------------------


class FluxExchange(VapourExchange):
    """Evaporation at ``rate`` per second, capture with probability ``capture`` per surface hit.

    Escaping molecules leave with a flux-weighted (Rayleigh) upward speed and
    vapour molecules are re-thermalised at ``mix`` per second (collisions), so
    the vapour count relaxes to ``rate / (capture * floor hits per molecule)``
    without a long tail of slow, lingering molecules."""

    def __init__(self, box: TwoPhaseBox, rate: float, capture: float = 1.0, seed: int = cfg.SEED + 3,
                 mix: float = 0.7) -> None:
        super().__init__(box, rate, capture, seed)
        self.mix = float(mix)

    def _velocity(self) -> np.ndarray:
        ux, uz = self.rng.normal(0.0, SIGMA, 2)
        return np.array([ux, self.rng.rayleigh(SIGMA), uz])

    def _release(self, i: int, age: float) -> None:
        box, gas, cloud = self.box, self.box.gas, self.box.cloud
        region = box.region
        fx, fz = self.rng.uniform(0.06, 0.94, 2)
        gas.u[i] = self._velocity()
        step = gas.u[i] * cloud.speed * cloud.heat * gas.slow[i] * age / region.extent()
        gas.phase[i] = np.array([fx, 0.02, fz]) + step
        gas.active[i] = True
        cloud.born[i] = cloud.time - age
        if age < 0.4:
            box.up_flashes.spark(region.point(fx, 0.0, fz), 1)

    def _tick(self) -> None:
        cloud, gas = self.box.cloud, self.box.gas
        now = cloud.time
        dt = max(now - self._last, 0.0)
        self._last = now
        if not self.enabled or dt <= 0:
            return
        if self.mix > 0:
            moving = np.nonzero(gas.active)[0]
            hit = moving[self.rng.random(len(moving)) < 1 - np.exp(-self.mix * dt)]
            if len(hit):
                gas.u[hit] = self.rng.normal(0.0, SIGMA, (len(hit), 3))
        self.owed += self.rate * dt
        n = int(self.owed)
        self.owed -= n
        idle = np.nonzero(~gas.active)[0]
        n = min(n, len(idle))
        if n:
            for i in self.rng.choice(idle, n, replace=False):
                # A long step (the still-frame tools) spreads the departures over it.
                self._release(int(i), float(self.rng.uniform(0, min(dt, 4.0))) if dt > 0.2 else 0.0)
                self.up.append(now)
        cut = now - 12.0
        self.up = [t for t in self.up if t > cut]
        self.down = [t for t in self.down if t > cut]

    def fill(self, n: int) -> None:
        """Start with ``n`` vapour molecules spread through the space above the liquid."""
        gas, cloud = self.box.gas, self.box.cloud
        idle = np.nonzero(~gas.active)[0][:max(int(n), 0)]
        for i in idle:
            gas.u[i] = self.rng.normal(0.0, SIGMA, 3)
            gas.phase[i] = self.rng.uniform(0.0, 2.0, 3)
            gas.active[i] = True
            cloud.born[i] = -1e9
        cloud.world = gas.positions(self.box.region.lo(), self.box.region.extent())

    def floor_hits(self) -> float:
        """Surface hits per second per vapour molecule (thermal average)."""
        cloud = self.box.cloud
        return float(np.sqrt(2 / np.pi) * SIGMA * cloud.speed * cloud.heat / (2 * self.box.region.height))

    def plateau(self, rate: float | None = None) -> float:
        """Vapour count at which condensation balances evaporation at ``rate``."""
        return (self.rate if rate is None else rate) / (self.capture * self.floor_hits())


# ----------------------------------------------------------------------------
# Shaded spheres with a size per point (things that grow, shrink or vanish)
# ----------------------------------------------------------------------------


class Specks(Body):
    """Small shaded spheres from ``source() -> (points (n, 3), scales (n,))``.

    ``depth`` pins the draw order (e.g. inside a pool); otherwise they sort by mean depth."""

    def __init__(self, source: Callable, color: str, radius: float = 0.07, depth: float | None = None) -> None:
        super().__init__()
        self.source, self.radius, self.fixed_depth = source, float(radius), depth
        self.template = Circle(radius=1.0, num_components=6).points.copy()
        self.base = VMobject(stroke_width=0, fill_color=mu.shade(color, 0.55), fill_opacity=1)
        self.middle = VMobject(stroke_width=0, fill_color=color, fill_opacity=1)
        self.glint = VMobject(stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.6)
        self.mob = VGroup(self.base, self.middle, self.glint)

    def _circles(self, c: np.ndarray, r: np.ndarray) -> np.ndarray:
        if len(c) == 0:
            return np.zeros((0, 3))
        pts = self.template[None, :, :] * r[:, None, None] + c[:, None, :]
        pts[:, :, 2] = 0
        return pts.reshape(-1, 3)

    def place(self, stage, R, visibility):
        pts, scales = self.source()
        pts = np.asarray(pts, dtype=float).reshape(-1, 3)
        scales = np.asarray(scales, dtype=float).reshape(-1)
        keep = scales > 0.02
        pts, scales = pts[keep], scales[keep]
        if not len(pts):
            for m in self.mob:
                m.points = np.zeros((0, 3))
            self.depth_key = -1e9 if self.fixed_depth is None else self.fixed_depth
            return
        screen, size, depth = stage.project(pts, R)
        self.depth_key = float(depth.mean()) if self.fixed_depth is None else self.fixed_depth
        r = self.radius * size * scales
        self.base.points = self._circles(screen, r)
        self.middle.points = self._circles(screen + np.array([-0.2, 0.2, 0.0]) * r[:, None], r * 0.72)
        self.glint.points = self._circles(screen + np.array([-0.38, 0.38, 0.0]) * r[:, None], r * 0.24)
        for m, a in ((self.base, 1.0), (self.middle, 1.0), (self.glint, 0.6)):
            m.set_fill(opacity=a * visibility)


# ----------------------------------------------------------------------------
# Escapes from an open surface
# ----------------------------------------------------------------------------


class Escapes:
    """Molecules leaving the surface of an open ``TwoPhaseBox``, one hop at a time.

    Each hop starts at a random point of the surface with an upward speed. In
    the attraction layer (``layer`` thick) the pull of the liquid slows it;
    a hop slower than the escape speed rises less than ``layer`` and falls
    back (light blue); a faster one breaks free with a gold flash and drifts
    up and out of the vessel as vapour (cyan), shrinking away above the rim.
    ``rate`` hops per second (``fast`` is the share that escapes); ``burst``
    sends vapour up from a point (a bursting bubble)."""

    def __init__(self, box: TwoPhaseBox, rate: float = 0.0, fast: float = 0.3, layer: float = 0.42,
                 pull: float = 6.0, seed: int = cfg.SEED + 11, size: float = 0.075) -> None:
        self.box, self.rate, self.fast, self.layer, self.pull = box, float(rate), float(fast), float(layer), float(pull)
        self.fade_span = 1.0          # escapers shrink away over this height above the rim
        self.rng = np.random.default_rng(seed)
        self.hops: list[list] = []        # [born, x, z, v0, drift_x, drift_z, escapes]
        self.owed = 0.0
        self._last = None
        self.v_escape = float(np.sqrt(2 * self.pull * self.layer))
        self.back = Specks(self._returners, mu.mix(cfg.LIQUID_EDGE, cfg.WHITE, 0.15), size)
        self.free = Specks(self._escapers, cfg.VAPOUR, size)
        box.stage.add_body(Ticker(self._tick), self.back, self.free)

    def tween_rate(self, value: float, **kwargs) -> Param:
        return set_attr(self.box.stage, self, "rate", value, **kwargs)

    def _height(self, age: float, v0: float) -> float:
        """Height above the surface: decelerated in the layer, free beyond it."""
        g, d = self.pull, self.layer
        if v0 <= self.v_escape:
            return max(v0 * age - 0.5 * g * age * age, 0.0)
        t_out = (v0 - np.sqrt(v0 * v0 - 2 * g * d)) / g
        if age <= t_out:
            return v0 * age - 0.5 * g * age * age
        return d + np.sqrt(v0 * v0 - 2 * g * d) * (age - t_out)

    def _spawn(self, now: float, at=None, escapes: bool | None = None) -> None:
        ch = self.box.chamber
        if at is None:
            x = ch.cx + self.rng.uniform(-0.88, 0.88) * ch.half_x
            z = ch.cz + self.rng.uniform(-0.88, 0.88) * ch.half_z
        else:
            x, z = float(at[0]), float(at[2])
        if escapes is None:
            escapes = self.rng.random() < self.fast
        if escapes:
            v0 = self.v_escape * self.rng.uniform(1.15, 1.5)
        else:
            v0 = self.v_escape * self.rng.uniform(0.45, 0.92)
        # Sideways drift, leaning inward so a molecule leaves through the open top, not a wall.
        drift = self.rng.normal(0.0, 0.1, 2) - 0.22 * np.array([(x - ch.cx) / ch.half_x, (z - ch.cz) / ch.half_z])
        self.hops.append([now, x, z, v0, drift[0], drift[1], bool(escapes), False])

    def burst(self, point, count: int = 2) -> None:
        now = self.box.stage.clock
        for _ in range(count):
            self._spawn(now, point, True)
            self.hops[-1][7] = True       # already free: no flash at the surface

    def _tick(self) -> None:
        now = self.box.stage.clock
        if self._last is None:
            self._last = now
        dt = max(now - self._last, 0.0)
        self._last = now
        self.owed += self.rate * min(dt, 1.0)
        while self.owed >= 1.0:
            self.owed -= 1.0
            self._spawn(now - (self.rng.uniform(0, dt) if dt > 0.2 else 0.0))
        surface = self.box.surface_y()
        top = self.box.chamber.top() + self.fade_span
        keep = []
        for hop in self.hops:
            born, x, z, v0, dx, dz, escapes, flashed = hop
            age = now - born
            h = self._height(age, v0)
            if escapes and not flashed and h >= self.layer:
                hop[7] = True
                if age - (self.layer / max(v0, 1e-6)) < 0.5:
                    self.box.up_flashes.spark(np.array([x + dx * age, surface + self.layer, z + dz * age]), 1)
            done = (not escapes and age > 0.2 and h <= 0.0) or surface + h > top
            if not done:
                keep.append(hop)
        self.hops = keep

    def _points(self, escaping: bool):
        now = self.box.stage.clock
        surface = self.box.surface_y()
        rim = self.box.chamber.top()
        pts, scales = [], []
        for born, x, z, v0, dx, dz, escapes, _ in self.hops:
            if escapes != escaping:
                continue
            age = max(now - born, 0.0)
            h = self._height(age, v0)
            y = surface + h
            pts.append((x + dx * age * (1.0 if escapes else 0.3), y, z + dz * age * (1.0 if escapes else 0.3)))
            scales.append(float(np.clip(1.0 - (y - rim) / self.fade_span, 0.0, 1.0)) * min(age / 0.12, 1.0))
        return np.array(pts).reshape(-1, 3), np.array(scales)

    def _returners(self):
        return self._points(False)

    def _escapers(self):
        return self._points(True)


# ----------------------------------------------------------------------------
# Boiling: bubbles of vapour inside the liquid
# ----------------------------------------------------------------------------


class Bubbles(Body):
    """Vapour bubbles in the pool of a ``TwoPhaseBox``.

    They nucleate at a few fixed sites on the floor (``rate`` per second in
    all), grow as they rise (more liquid evaporates into them and the
    pressure of the liquid above falls), speed up as they grow, and burst at
    the surface with a cyan ripple; ``on_pop(point)`` lets the vapour escape.
    Drawn inside the pool: between the liquid's molecules and its surface."""

    def __init__(self, box: TwoPhaseBox, rate: float = 0.0, sites: int = 7, r0: float = 0.035,
                 r_max: float = 0.2, grow: float = 0.12, rise: float = 0.55, seed: int = cfg.SEED + 13,
                 on_pop: Callable | None = None) -> None:
        super().__init__()
        self.box, self.rate, self.r0, self.r_max, self.grow, self.rise = box, float(rate), r0, r_max, grow, rise
        self.size = 1.0
        self.on_pop = on_pop
        self.rng = np.random.default_rng(seed)
        ch = box.chamber
        self.sites = np.column_stack([ch.cx + self.rng.uniform(-0.75, 0.75, sites) * ch.half_x,
                                      ch.cz + self.rng.uniform(-0.75, 0.75, sites) * ch.half_z])
        self.items: list[list] = []      # [x, z, height above floor, phase]
        self.owed = 0.0
        self._last = None
        self.circle = Circle(radius=1.0, num_components=8).points.copy()
        self.fill = VMobject(stroke_width=0, fill_color=cfg.VAPOUR, fill_opacity=0.2)
        self.rim = VMobject(stroke_color=mu.mix(cfg.LIQUID_EDGE, cfg.WHITE, 0.5), stroke_width=2.2, fill_opacity=0)
        self.glint = VMobject(stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.55)
        self.mob = VGroup(self.fill, self.rim, self.glint)
        self.pops = TimedFlashes(mu.mix(cfg.VAPOUR, cfg.WHITE, 0.3), 1.3)
        box.stage.add_overlay(self.pops)

    def tween_rate(self, value: float, **kwargs) -> Param:
        return set_attr(self.box.stage, self, "rate", value, **kwargs)

    def radius(self, height: float) -> float:
        return min(self.r0 + self.grow * height, self.r_max) * self.size

    def _advance(self, stage) -> None:
        now = stage.clock
        if self._last is None:
            self._last = now
        dt = min(max(now - self._last, 0.0), 1.5)
        self._last = now
        ch = self.box.chamber
        depth = float(self.box.level)
        self.owed += self.rate * dt
        while self.owed >= 1.0:
            self.owed -= 1.0
            x, z = self.sites[self.rng.integers(len(self.sites))]
            start = self.rng.uniform(0.0, 0.3) if dt < 0.2 else self.rng.uniform(0.0, max(depth - 0.2, 0.01))
            self.items.append([x + self.rng.normal(0, 0.03), z + self.rng.normal(0, 0.03), start,
                               self.rng.uniform(0, 2 * np.pi)])
        keep = []
        for item in self.items:
            r = self.radius(item[2])
            item[2] += self.rise * (0.45 + 0.55 * r / (self.r_max * self.size + 1e-9)) * dt
            if item[2] + self.radius(item[2]) >= depth:
                point = np.array([item[0], ch.floor + depth, item[1]])
                self.pops.spark(point, 1)
                if self.on_pop is not None:
                    self.on_pop(point)
                continue
            keep.append(item)
        self.items = keep

    def place(self, stage, R, visibility):
        self._advance(stage)
        self.depth_key = -650.0
        if not self.items:
            for m in self.mob:
                m.points = np.zeros((0, 3))
            return
        ch = self.box.chamber
        t = stage.clock
        centres = np.array([[x + 0.03 * np.sin(2.6 * t + p), ch.floor + h, z + 0.03 * np.cos(2.2 * t + p)]
                            for x, z, h, p in self.items])
        radii = np.array([self.radius(h) for _, _, h, _ in self.items])
        screen, size, _ = stage.project(centres, R)
        rr = radii * size
        rings = self.circle[None, :, :] * rr[:, None, None] + screen[:, None, :]
        rings[:, :, 2] = 0
        self.fill.points = rings.reshape(-1, 3)
        self.rim.points = rings.reshape(-1, 3).copy()
        glints = self.circle[None, :, :] * (rr * 0.22)[:, None, None] + (screen + np.array([-0.4, 0.42, 0]) * rr[:, None])[:, None, :]
        glints[:, :, 2] = 0
        self.glint.points = glints.reshape(-1, 3)
        self.fill.set_fill(opacity=0.22 * visibility)
        self.rim.set_stroke(opacity=0.85 * visibility)
        self.glint.set_fill(opacity=0.5 * visibility)


# ----------------------------------------------------------------------------
# Lids and the hot plate
# ----------------------------------------------------------------------------


def sink_heater(box: GasBox) -> None:
    """Draw a box's hot plate, glow and coil beneath its pool (a pool sorts by fixed depth keys, so a plate
    sorted by its own depth would cover the liquid's molecules)."""
    for k, part in enumerate(p for p in box.parts if p is not None):
        if isinstance(part, Block) or part is getattr(box, "glow", None) or part is getattr(box, "coil", None):
            part.bias = -5e3 + 10 * k


class GlassLid(GlassWall):
    """A glass lid that rides ``lift`` above the top of a vessel (tween ``lift`` to 0 to seal it)."""

    def __init__(self, box: GasBox, lift: float = 1.0) -> None:
        self.lift = float(lift)
        ch = box.chamber

        def corners():
            y = ch.top() + self.lift
            return [np.array([ch.cx + sx * (ch.half_x + 0.04), y, ch.cz + sz * (ch.half_z + 0.04)])
                    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]

        super().__init__(corners, (0, 1, 0), opacity=0.12, edge_opacity=0.9)
        self.box = box
        self.presence = 0.0
        box.stage.add_body(self)

    def lower(self, **kwargs) -> list[Param]:
        stage = self.box.stage
        return [set_attr(stage, self, "lift", 0.0, **kwargs), stage.fade(self, 1.0, **kwargs)]


class SteelLid:
    """A pressure-cooker lid: a steel plate with a weighted valve, dropped onto a vessel from ``lift``."""

    def __init__(self, box: GasBox, lift: float = 1.6) -> None:
        self.box, self.lift = box, float(lift)
        ch = box.chamber
        plate = Block(lambda: np.array([ch.cx, ch.top() + self.lift + 0.08, ch.cz]),
                      (2 * ch.half_x + 0.2, 0.16, 2 * ch.half_z + 0.2), cfg.STEEL)
        stem = Block(lambda: np.array([ch.cx, ch.top() + self.lift + 0.3, ch.cz]), (0.12, 0.3, 0.12), "#6F8496")
        weight = Block(lambda: np.array([ch.cx, ch.top() + self.lift + 0.5, ch.cz]), (0.42, 0.2, 0.42), "#B98B3E")
        self.parts = [plate, stem, weight]
        for p in self.parts:
            p.presence = 0.0
        box.stage.add_body(*self.parts)

    def drop(self, **kwargs) -> list[Param]:
        stage = self.box.stage
        return [set_attr(stage, self, "lift", 0.0, **kwargs), *[stage.fade(p, 1.0, **kwargs) for p in self.parts]]

    def raise_off(self, **kwargs) -> list[Param]:
        stage = self.box.stage
        return [set_attr(stage, self, "lift", 1.6, **kwargs), *[stage.fade(p, 0.0, **kwargs) for p in self.parts]]
