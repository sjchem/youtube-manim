"""Shared pieces for scenes 16, 17, 20 and 22 (compressibility, the Boyle
temperature, van der Waals loops, critical temperatures).

* ``at_word`` holds until a word of the current narration beat is spoken, so a
  curve is drawn as its gas is named;
* ``Trace`` is a curve on 2D axes that grows to a tweenable end with a glowing
  bead at its tip;
* ``PairLinks`` draws green attraction links between near neighbours of a gas
  cloud on a 3D stage;
* ``z_color`` is the compressibility colour scale (green below 1, white at 1,
  red above); ``band`` tints a rectangle of a plot.
"""

from __future__ import annotations

import narration
from manim_scenes.common import *
from manim_scenes.stage3d import Body


# ----------------------------------------------------------------------------
# Timing inside a beat
# ----------------------------------------------------------------------------


def word_time(key: str, index: int, word: str, nth: int = 1) -> float:
    """Seconds into the scene at which ``word`` (its ``nth`` occurrence) of beat ``index`` is spoken."""
    start_at, text = SCRIPT[key][index]
    tokens = [w.lower() for w in narration._WORD.findall(text)]
    target = word.lower()
    seen = 0
    for k, token in enumerate(tokens):
        if token == target:
            seen += 1
            if seen == nth:
                return start_at + k / narration.PACE
    raise ValueError(f"'{word}' not in beat {index} of scene {key}")


def at_word(scene: Scene, started_at: float, index: int, word: str, nth: int = 1, lead: float = 0.0) -> None:
    """Hold until a word of beat ``index`` is spoken (never raises: a late cue simply passes)."""
    key = scene._project_scene_key
    remaining = word_time(key, index, word, nth) - lead - (float(scene.time) - started_at)
    if remaining > 2.0 / float(scene.camera.frame_rate):
        scene.wait(remaining)


def fill_until(scene: Scene, started_at: float, upto: int, *animations, margin: float = 0.06, **kwargs) -> None:
    """Play ``animations`` stretched over all the time left before beat ``upto``."""
    left = time_left(scene, started_at, upto) - margin
    if left > 2.0 / float(scene.camera.frame_rate):
        scene.play(*animations, run_time=left, **kwargs)


# ----------------------------------------------------------------------------
# Colour
# ----------------------------------------------------------------------------


def z_color(z: float, low: float = 0.3, high: float = 0.06) -> str:
    """Compressibility colour: green where attraction wins (Z < 1), white at 1, red where size wins."""
    if z < 1:
        return mu.mix(cfg.WHITE, cfg.ATTRACT, float(np.clip((1 - z) / low, 0, 1)) ** 0.6)
    return mu.mix(cfg.WHITE, cfg.SIZE, float(np.clip((z - 1) / high, 0, 1)) ** 0.6)


def band(axes: Axes, x0: float, x1: float, y0: float, y1: float, color: str, opacity: float = 0.1) -> Polygon:
    """A tinted rectangle in data coordinates."""
    return Polygon(axes.c2p(x0, y0), axes.c2p(x1, y0), axes.c2p(x1, y1), axes.c2p(x0, y1), stroke_width=0,
                   fill_color=color, fill_opacity=opacity)


# ----------------------------------------------------------------------------
# A curve that grows along its x range, with a bead at its tip
# ----------------------------------------------------------------------------


class Trace:
    """``ys`` sampled at ascending (or descending) ``xs`` on ``axes``; ``end`` is a Knob
    holding the x reached so far. ``curve`` and ``bead`` are live mobjects."""

    def __init__(self, axes: Axes, xs, ys, color: str, *, width: float = 6.0, bead_radius: float = 0.1,
                 start: float | None = None) -> None:
        self.axes, self.color, self.width = axes, color, width
        self.xs, self.ys = np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)
        self.rising = self.xs[-1] > self.xs[0]
        self.end = Knob(self.xs[0] if start is None else start)
        self.bead_alpha = 1.0
        self.bead_radius = bead_radius
        self.curve = live(VGroup(), self._build)
        self.bead = live(VGroup(), self._bead)

    def y_at(self, x: float) -> float:
        if self.rising:
            return float(np.interp(x, self.xs, self.ys))
        return float(np.interp(x, self.xs[::-1], self.ys[::-1]))

    def tip(self) -> np.ndarray:
        return self.axes.c2p(self.end.value, self.y_at(self.end.value))

    def _points(self) -> list[np.ndarray]:
        x = self.end.value
        keep = self.xs <= x if self.rising else self.xs >= x
        pts = [self.axes.c2p(a, b) for a, b in zip(self.xs[keep], self.ys[keep])]
        pts.append(self.tip())
        return pts

    def _build(self) -> VGroup:
        pts = self._points()
        if len(pts) < 2 or np.linalg.norm(pts[-1] - pts[0]) < 1e-3:
            return VGroup()
        core = VMobject(stroke_color=self.color, stroke_width=self.width, fill_opacity=0).set_points_as_corners(pts)
        glow = core.copy().set_stroke(self.color, width=self.width * 3.2, opacity=0.14)
        return VGroup(glow, core)

    def _bead(self) -> VGroup:
        if self.bead_alpha <= 0.01:
            return VGroup()
        dot = glow_dot(self.tip(), self.color, radius=self.bead_radius)
        if self.bead_alpha < 0.99:
            for part in dot.family_members_with_points():
                part.set_fill(opacity=float(part.get_fill_opacity()) * self.bead_alpha)
        return dot

    def grow(self, x: float, **kwargs) -> Param:
        return self.end.to(self.curve, x, **kwargs)

    def fade_bead(self, value: float, **kwargs) -> Param:
        return set_attr(self.curve, self, "bead_alpha", value, **kwargs)

    def parts(self) -> VGroup:
        return VGroup(self.curve, self.bead)

    def stop(self) -> None:
        self.curve.clear_updaters()
        self.bead.clear_updaters()


# ----------------------------------------------------------------------------
# Attraction links between near neighbours of a gas cloud
# ----------------------------------------------------------------------------


def _pairs_as_points(screen: np.ndarray) -> np.ndarray:
    p, q = screen[0::2], screen[1::2]
    quads = np.stack([p, p + (q - p) / 3, p + 2 * (q - p) / 3, q], axis=1)
    return quads.reshape(-1, 3)


class PairLinks(Body):
    """Green links between active molecules closer than ``cutoff`` (stage units).

    Drawn just behind the cloud so the molecules sit on the ends of their links.
    ``alpha`` (tween with ``set_attr``) sets the strength of the cue. Add it to
    the stage *after* the cloud so it reads this frame's positions."""

    def __init__(self, cloud, cutoff: float = 0.5, color: str = cfg.ATTRACT, width: float = 3.0,
                 alpha: float = 0.0) -> None:
        super().__init__()
        self.cloud, self.cutoff, self.alpha = cloud, float(cutoff), float(alpha)
        self.bias = -1e-3
        self.core = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
        self.glow = VMobject(stroke_color=color, stroke_width=width * 3.4, fill_opacity=0)
        self.mob = VGroup(self.glow, self.core)

    def pairs(self) -> np.ndarray:
        pts = self.cloud.world[self.cloud.gas.active]
        if len(pts) < 2:
            return np.zeros((0, 2, 3))
        d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)
        i, j = np.nonzero(np.triu(d < self.cutoff, k=1))
        return np.stack([pts[i], pts[j]], axis=1)

    def place(self, stage, R, visibility):
        pairs = self.pairs()
        a = self.alpha * visibility
        if not len(pairs) or a <= 0.004:
            self.core.points = np.zeros((0, 3))
            self.glow.points = np.zeros((0, 3))
            self.depth_key = self.cloud.depth_key
            return
        screen, _, depth = stage.project(pairs.reshape(-1, 3), R)
        path = _pairs_as_points(screen)
        self.core.points = path
        self.glow.points = path.copy()
        self.core.set_stroke(opacity=0.85 * a)
        self.glow.set_stroke(opacity=0.16 * a)
        self.depth_key = self.cloud.depth_key


# ----------------------------------------------------------------------------
# Small 2D pieces
# ----------------------------------------------------------------------------


def legend_row(name: str, color: str, size: int | None = None, length: float = 0.6) -> VGroup:
    swatch = Line(ORIGIN, RIGHT * length, stroke_color=color, stroke_width=7)
    label = txt(name, size or cfg.FONT["label"], color)
    return VGroup(swatch, label).arrange(RIGHT, buff=0.2)


def minus(text: str) -> str:
    """Typographic minus signs for on-screen numbers."""
    return text.replace("-", "−")
