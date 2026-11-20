"""Shared pieces for scenes 18, 19 and 21 (liquefaction and the critical point).

* ``SqueezeBox`` — a ``TwoPhaseBox`` whose liquid lattice compresses with the
  vessel (``squash`` < 1) instead of losing its top layer, so a liquid being
  squeezed looks squeezed; each layer of liquid molecules fills in at random
  as the level passes it, so the first liquid appears as scattered drops;
* ``phase_chip`` — a chip naming a phase, with a small sketch of how its
  stretch of the isotherm looks (gentle rise, flat, steep);
* ``andrews_color`` — the cold-to-hot colour of an Andrews isotherm;
* van der Waals helpers in reduced units for the P-V-T surface.
"""

from __future__ import annotations

from manim_scenes.common import *


class SqueezeBox(TwoPhaseBox):
    """A liquid and its vapour whose liquid molecules pack closer when the vessel is shorter than the pool."""

    def __init__(self, *args, **kwargs) -> None:
        self.squash = 1.0
        self._rank = None
        self._rank_seed = kwargs.get("seed", cfg.SEED) + 7
        super().__init__(*args, **kwargs)

    def _liquid_points(self) -> np.ndarray:
        ch, sp = self.chamber, self._spacing
        if self._rank is None:
            self._rank = np.random.default_rng(self._rank_seed).uniform(0.0, 1.0, len(self._sites))
        s = float(np.clip(self.squash, 0.05, 1.0))
        depth = float(np.clip(self.level, 0.0, ch.height)) / s     # the pool's depth before squashing
        # A layer of sites (centred 0.5 sp above its base) fills in at random as the level rises through it.
        idx = (depth - (self._sites[:, 1] - 0.5 * sp)) / (1.1 * sp) > self._rank
        sites = self._sites[idx]
        if not len(sites):
            return np.zeros((0, 3))
        wobble = 0.16 * sp * np.sin(self.stage.clock * self._omega[idx] + self._phase[idx])
        wobble[:, 1] *= s
        base = np.column_stack([ch.cx - ch.half_x + sites[:, 0] * 2 * ch.half_x, ch.floor + sites[:, 1] * s,
                                ch.cz - ch.half_z + sites[:, 2] * 2 * ch.half_z])
        return base + wobble


def _sketch(shape: str, color: str, w: float = 0.62, h: float = 0.42) -> VGroup:
    """A tiny isotherm stretch: 'gas' (gentle rise toward small V), 'flat' or 'steep'."""
    if shape == "gas":
        xs = np.linspace(0.0, 1.0, 20)
        pts = [np.array([x * w, (0.45 / (x + 0.35) - 0.33) * h / 0.95, 0.0]) for x in xs]
    elif shape == "flat":
        pts = [np.array([0.0, 0.5 * h, 0.0]), np.array([w, 0.5 * h, 0.0])]
    else:
        ys = np.linspace(0.0, 1.0, 20)
        pts = [np.array([0.3 * w + 0.22 * w * (1 - y) ** 2.5, y * h, 0.0]) for y in ys]
    core = polyline(pts, color, width=5)
    group = VGroup(core.copy().set_stroke(width=13, opacity=0.18), core)
    frame = Rectangle(width=w, height=h, stroke_width=0, fill_opacity=0).move_to(group)
    frame.move_to([w / 2, h / 2, 0])
    return VGroup(frame, group)


def phase_chip(name: str, color: str, shape: str, size: int | None = None) -> VGroup:
    """A rounded pill: a sketch of the isotherm's shape, then the phase's name."""
    label = txt(name, size or cfg.FONT["small"], color)
    icon = _sketch(shape, color)
    row = VGroup(icon, label).arrange(RIGHT, buff=0.22)
    pill = RoundedRectangle(width=row.width + 0.6, height=max(row.height, label.height) + 0.36, corner_radius=0.22,
                            stroke_color=color, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.92)
    group = VGroup(pill, row.move_to(pill))
    group.pill, group.label, group.icon = pill, label, icon
    return group


def andrews_color(celsius_value: float) -> str:
    """Cold (13 °C, blue) to hot (48 °C, coral) along the Andrews temperatures; the critical one is purple."""
    lo, hi = min(pm.ANDREWS_C), max(pm.ANDREWS_C)
    f = (celsius_value - lo) / (hi - lo)
    return mu.mix(cfg.COLD_COLOR, cfg.HOT_COLOR, float(np.clip(f, 0, 1)))
