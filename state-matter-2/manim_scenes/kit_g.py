"""Shared pieces for the liquid-property scenes 25-28 (surface tension and viscosity).

* ``ShadedMesh`` - a translucent quad mesh on a ``Stage`` (a liquid cube that
  rounds into a sphere, a drop, the wall of a glass column). Each quad is lit
  by its view-space normal, back faces draw dimmer behind the front ones, and
  faces are batched into a few shade bins so a few hundred quads stay cheap;
* ``cube_mesh`` / ``mesh_volume_area`` - a subdivided cube and the exact volume
  and area of any closed quad mesh (so on-screen areas are measured, not typed);
* ``column_mesh`` - an open vertical cylinder of quads (glass walls, liquid columns);
* ``KeyedFace`` - a face whose draw order is chosen by a function (a liquid top
  that is in front of a ball above it and behind a ball below it);
* ``FlowDots`` - dots with per-dot radii (markers that shrink as they wrap
  around the end of a flowing layer);
* ``fill_to`` - keep moving until the next narration beat.
"""

from __future__ import annotations

from manim_scenes.common import *
from manim_scenes.stage3d import _value

LIGHT = mu.unit([-0.45, 0.78, 0.5])
GLOSS = mu.unit(LIGHT + np.array([0.0, 0.0, 1.0]))


def _polygons(screen: np.ndarray) -> np.ndarray:
    """(n, k, 3) closed polygons -> VMobject points with one subpath each."""
    if len(screen) == 0:
        return np.zeros((0, 3))
    p, q = screen, np.roll(screen, -1, axis=1)
    quads = np.stack([p, p + (q - p) / 3, p + 2 * (q - p) / 3, q], axis=2)
    return quads.reshape(-1, 3)


class ShadedMesh(Body):
    """A lit, translucent quad mesh. ``verts`` is an (n, 3) array or a function
    returning one (a live, morphing shape); ``quads`` (m, 4) index outward-wound
    faces. ``side`` draws "both" halves, only the "front" (facing the viewer) or
    only the "back"; ``key`` (a function) overrides the depth used to sort the
    mesh among other bodies. ``alpha`` may be tweened."""

    def __init__(self, verts, quads, color: str, *, opacity: float = 0.5, back: float = 0.5, side: str = "both",
                 bins: int = 15, edge_opacity: float = 0.12, gloss: float = 0.6, bias: float = 0.0,
                 key: Callable[[], float] | None = None, edge_color: str | None = None) -> None:
        super().__init__()
        self.verts, self.quads = verts, np.asarray(quads, dtype=int)
        self.opacity, self.back, self.side, self.bins = float(opacity), float(back), side, int(bins)
        self.edge_opacity, self.gloss, self.bias, self.key = float(edge_opacity), float(gloss), float(bias), key
        self.alpha = 1.0
        rgb = np.array(ManimColor(color).to_rgb())
        white = np.array(ManimColor(cfg.WHITE).to_rgb())
        self.front_layers = []
        for k in range(self.bins):
            b = 1.5 * (k + 0.5) / self.bins             # diffuse 0..1, then a glossy highlight up to 1.5
            tone = np.clip(rgb * (0.42 + 0.7 * min(b, 1.0)), 0, 1)
            tone = tone + (white - tone) * self.gloss * max(b - 1.0, 0.0) / 0.5
            self.front_layers.append(VMobject(stroke_width=0, fill_color=ManimColor(np.clip(tone, 0, 1)),
                                              fill_opacity=self.opacity))
        self.back_layers = [VMobject(stroke_width=0, fill_color=ManimColor(np.clip(rgb * s, 0, 1)),
                                     fill_opacity=self.opacity) for s in (0.3, 0.42, 0.55)]
        self.lines = VMobject(stroke_color=edge_color or mu.mix(color, cfg.WHITE, 0.45), stroke_width=1.2,
                              fill_opacity=0)
        self.mob = VGroup(*self.back_layers, *self.front_layers, self.lines)

    def place(self, stage, R, visibility):
        verts = np.asarray(_value(self.verts), dtype=float).reshape(-1, 3)
        screen, _, depth = stage.project(verts, R)
        view = verts @ R.T
        q = self.quads
        a, b, c, d = view[q[:, 0]], view[q[:, 1]], view[q[:, 2]], view[q[:, 3]]
        normal = np.cross(c - a, d - b)
        normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-9)
        centre = (a + b + c + d) / 4
        eye = np.array([0.0, 0.0, stage.distance])
        facing = np.einsum("ij,ij->i", normal, eye - centre) > 0
        lam = np.clip(normal @ LIGHT, 0.0, 1.0)
        polys = screen[q]
        vis = visibility * self.alpha
        front = facing if self.side != "back" else np.zeros(len(q), dtype=bool)
        rear = ~facing if self.side != "front" else np.zeros(len(q), dtype=bool)
        spec = np.clip(normal @ GLOSS, 0.0, 1.0) ** 18
        bright = np.minimum(lam + 0.5 * spec, 1.5)
        level = np.clip((bright / 1.5 * self.bins).astype(int), 0, self.bins - 1)
        for k, layer in enumerate(self.front_layers):
            layer.points = _polygons(polys[front & (level == k)])
            layer.set_fill(opacity=self.opacity * vis)
        back_level = np.clip((lam * 3).astype(int), 0, 2)
        for k, layer in enumerate(self.back_layers):
            layer.points = _polygons(polys[rear & (back_level == k)])
            layer.set_fill(opacity=self.opacity * self.back * vis)
        if self.edge_opacity > 0:
            self.lines.points = _polygons(polys[front])
            self.lines.set_stroke(opacity=self.edge_opacity * vis)
        else:
            self.lines.points = np.zeros((0, 3))
        self.depth_key = float(self.key()) if self.key is not None else float(depth.mean()) + self.bias


def cube_mesh(n: int = 8) -> tuple[np.ndarray, np.ndarray]:
    """Vertices of the cube [-1, 1]^3 cut into n x n quads per face, and outward-wound quads."""
    index: dict[tuple, int] = {}
    pts: list[np.ndarray] = []
    quads: list[list[int]] = []

    def vid(p: np.ndarray) -> int:
        k = tuple(np.round(p, 6))
        if k not in index:
            index[k] = len(pts)
            pts.append(p)
        return index[k]

    e = np.eye(3)
    for axis in range(3):
        for sign in (1, -1):
            u, v = e[(axis + 1) % 3], e[(axis + 2) % 3]
            if sign < 0:
                u, v = v, u

            def grid(i: int, j: int) -> np.ndarray:
                return sign * e[axis] + u * (-1 + 2 * i / n) + v * (-1 + 2 * j / n)

            for i in range(n):
                for j in range(n):
                    quads.append([vid(grid(i, j)), vid(grid(i + 1, j)), vid(grid(i + 1, j + 1)), vid(grid(i, j + 1))])
    return np.array(pts), np.array(quads)


def mesh_volume_area(points: np.ndarray, quads: np.ndarray) -> tuple[float, float]:
    """Enclosed volume and surface area of a closed, outward-wound quad mesh (two triangles per quad)."""
    a, b, c, d = (points[quads[:, k]] for k in range(4))
    volume = (np.einsum("ij,ij->i", a, np.cross(b, c)) + np.einsum("ij,ij->i", a, np.cross(c, d))).sum() / 6
    area = (np.linalg.norm(np.cross(b - a, c - a), axis=1) + np.linalg.norm(np.cross(c - a, d - a), axis=1)).sum() / 2
    return float(volume), float(area)


def column_mesh(segments: int = 28) -> np.ndarray:
    """Quads (as index rows) of an open vertical tube with ``segments`` around: vertices
    0..segments-1 are the bottom ring, segments..2*segments-1 the top ring."""
    return np.array([[k, (k + 1) % segments, segments + (k + 1) % segments, segments + k] for k in range(segments)])


def column_points(centre, radius: float, bottom: float, top: float, segments: int = 28) -> np.ndarray:
    """Vertices for ``column_mesh``: a ring at ``bottom`` and a ring at ``top`` (heights in stage units)."""
    c = np.asarray(centre, dtype=float)
    a = np.linspace(0, 2 * np.pi, segments, endpoint=False)
    ring = np.column_stack([np.cos(a) * radius, np.zeros_like(a), -np.sin(a) * radius])
    low = ring + np.array([c[0], bottom, c[2]])
    high = ring + np.array([c[0], top, c[2]])
    return np.vstack([low, high])


def ring_points(centre, radius: float, y: float, samples: int = 40) -> np.ndarray:
    c = np.asarray(centre, dtype=float)
    a = np.linspace(0, 2 * np.pi, samples, endpoint=False)
    return np.column_stack([c[0] + np.cos(a) * radius, np.full_like(a, y), c[2] - np.sin(a) * radius])


class KeyedFace(Face):
    """A face whose place in the draw order comes from ``key()``."""

    def __init__(self, corners, color: str, key: Callable[[], float], opacity: float = 0.3,
                 edge_opacity: float = 0.6, width: float = 2.4) -> None:
        super().__init__(corners, color, opacity=opacity, edge_opacity=edge_opacity)
        self.key = key
        self.poly.set_stroke(width=width)

    def place(self, stage, R, visibility):
        super().place(stage, R, visibility)
        self.depth_key = float(self.key())


class FlowDots(Dots):
    """Dots whose radii are scaled per dot by ``scale()`` (an array, e.g. a fade at a wrap-around)."""

    def __init__(self, points, color: str, scale: Callable[[], np.ndarray], *, radius: float = 0.05,
                 alpha: float = 1.0, bias: float = 0.0) -> None:
        super().__init__(points, color, radius=radius, alpha=alpha)
        self.scale, self.bias = scale, bias

    def place(self, stage, R, visibility):
        pts = np.asarray(_value(self.points), dtype=float).reshape(-1, 3)
        if len(pts) == 0:
            for layer in self.layers:
                for m in layer:
                    m.points = np.zeros((0, 3))
            return
        screen, size, depth = stage.project(pts, R)
        self.depth_key = float(depth.mean())
        radii = self.radius * size * np.asarray(self.scale(), dtype=float)
        mid = float(np.median(depth))
        a = self.alpha * visibility
        for b, mask in enumerate((depth < mid, depth >= mid)):
            base, middle, glint = self.layers[b]
            c, r = screen[mask], radii[mask]
            base.points = self._circles(c, r)
            middle.points = self._circles(c + np.array([-0.2, 0.2, 0.0]) * r[:, None], r * 0.72)
            glint.points = self._circles(c + np.array([-0.38, 0.38, 0.0]) * r[:, None], r * 0.24)
            base.set_fill(opacity=a)
            middle.set_fill(opacity=a)
            glint.set_fill(opacity=0.6 * a)


class SortedDots(Dots):
    """Dots drawn at a fixed place in the draw order (``key``), e.g. a dim crowd always at the back."""

    def __init__(self, points, color: str, *, radius: float = 0.05, alpha: float = 1.0, key: float = 0.0) -> None:
        super().__init__(points, color, radius=radius, alpha=alpha)
        self.key = float(key)

    def place(self, stage, R, visibility):
        super().place(stage, R, visibility)
        self.depth_key = self.key


def fill_to(scene: Scene, started: float, upto: int, *anims: Animation, margin: float = 0.08, **kwargs) -> None:
    """Play ``anims`` (or simply hold, live stages moving) for all the time left before beat ``upto``."""
    left = time_left(scene, started, upto) - margin
    if left <= 0.1:
        return
    if anims:
        scene.play(*anims, run_time=left, **kwargs)
    else:
        scene.wait(left)


def hop_path(a, b, lift: float = 0.6, samples: int = 24) -> np.ndarray:
    """A parabolic arc from ``a`` to ``b`` rising ``lift`` above the straight line."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    s = np.linspace(0, 1, samples)[:, None]
    return a + (b - a) * s + np.array([0.0, 1.0, 0.0]) * lift * 4 * s * (1 - s)


__all__ = [name for name in dir() if not name.startswith("_")]
