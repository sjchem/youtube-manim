"""A shaded, turning hot-air balloon with a transparent teaching cutaway."""
from __future__ import annotations

import numpy as np
from manim import ManimColor, VGroup, VMobject

import config as cfg
from manim_scenes.stage3d import Body, Block, Curve, Disc, Dots, Face, Param, Segment, Stage
from utils import math_utils as mu


def envelope_radius(u: float) -> float:
    """Rounded crown, broad shoulder and a narrow, open skirt."""
    u = float(np.clip(u, 0, 1))
    return float(0.12 * u + 1.75 * max(np.sin(np.pi * u), 0.0) ** 0.65 * (1.12 - 0.56 * u))


def envelope_point(u: float, angle: float) -> np.ndarray:
    radius = envelope_radius(u) * (0.985 - 0.015 * np.cos(12 * angle))
    return np.array([radius * np.cos(angle), 1.95 - 3.5 * u, radius * np.sin(angle)])


class FabricPatch(Face):
    """A cloth patch whose light and reflection change with the camera view."""

    def __init__(self, corners, color: str, u: float, angle: float, cutaway: bool = False) -> None:
        super().__init__(corners, color, opacity=0.12 if cutaway else 1.0, edge_opacity=0.0)
        self.rgb = np.array(ManimColor(color).to_rgb())
        eps = 1e-4
        slope = (envelope_radius(u + eps) - envelope_radius(u - eps)) / (2 * eps)
        self.normal = mu.unit([np.cos(angle), slope / 3.5, np.sin(angle)])
        self.cutaway = cutaway
        self.keep_in_frame = True

    def place(self, stage: Stage, R: np.ndarray, visibility: float) -> None:
        super().place(stage, R, visibility)
        # Slight overlap closes antialiasing cracks without drawing a mesh grid.
        if not self.cutaway:
            centre = self.poly.points.mean(axis=0)
            self.poly.points = centre + (self.poly.points - centre) * 1.012
        normal = R @ self.normal
        light = mu.unit([-0.55, 0.8, 0.95])
        half_vector = mu.unit(light + np.array([0, 0, 1]))
        diffuse = 0.34 + 0.66 * max(0.0, float(normal @ light))
        sheen = max(0.0, float(normal @ half_vector)) ** 22
        rgb = np.clip(self.rgb * diffuse + np.array([1.0, 0.88, 0.67]) * 0.24 * sheen, 0, 1)
        color = ManimColor(rgb)
        self.poly.set_fill(color, opacity=self.opacity * visibility)
        self.poly.set_stroke(width=0, opacity=0)


class BurnerFlame(Body):
    """A small, smoothly flickering flame at the open skirt."""

    def __init__(self) -> None:
        super().__init__()
        self.layers = [VMobject(stroke_width=0, fill_color=color, fill_opacity=alpha)
                       for color, alpha in (("#E55D32", 0.85), ("#FFA940", 0.95), ("#FFE7A0", 1.0))]
        self.mob = VGroup(*self.layers)
        self.keep_in_frame = True

    def place(self, stage: Stage, R: np.ndarray, visibility: float) -> None:
        point, scale, depth = stage.project(np.array([[0.0, -1.86, 0.03]]), R)
        base, size = point[0], scale[0]
        height = 0.65 + 0.045 * np.sin(11 * stage.clock) + 0.025 * np.sin(17 * stage.clock)
        lean = 0.025 * np.sin(7 * stage.clock)
        for layer, fraction, alpha in zip(self.layers, (1.0, 0.68, 0.38), (0.85, 0.95, 1.0)):
            w, h = 0.115 * fraction, height * fraction
            points = np.array([[0, 0, 0], [-w, h * 0.2, 0], [-w * 0.65, h * 0.58, 0],
                               [lean, h, 0], [w * 0.65, h * 0.55, 0], [w, h * 0.2, 0], [0, 0, 0]])
            layer.set_points_smoothly(points * size + base)
            layer.set_fill(opacity=alpha * visibility)
        self.depth_key = float(depth[0]) + 0.03


class HotAirBalloon(Stage):
    """True 3D cloth, seams, suspension cables and an open wicker basket.

    Two transparent gores are a cutaway for the molecular explanation;
    the real envelope remains closed apart from its bottom opening.
    """

    def __init__(self, at, scale: float = 1.0) -> None:
        super().__init__(at, zoom=scale, yaw=-0.28, pitch=0.12, spin=0.045, sway=0.025)
        palette = ["#EC8052", "#F6C56E", "#D8F0E8", "#D8F0E8", "#E47B4F", "#45A6AF",
                   "#F0B35D", "#D46648", "#F2C16D", "#3D919F", "#E98750", "#F3C56F"]
        bodies = []
        us = np.linspace(0, 1, 21)
        angles = np.linspace(0, 2 * np.pi, 25)
        for k, (a, b) in enumerate(zip(angles[:-1], angles[1:])):
            gore = k // 2
            for u, v in zip(us[:-1], us[1:]):
                corners = [envelope_point(u, a), envelope_point(v, a), envelope_point(v, b), envelope_point(u, b)]
                bodies.append(FabricPatch(corners, palette[gore], (u + v) / 2, (a + b) / 2, cutaway=gore in (2, 3)))
        self.envelope = tuple(bodies)
        for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            seam = Curve(np.array([envelope_point(u, angle) for u in np.linspace(0, 1, 65)]),
                         "#FFDFAD", width=1.1, glow=False, opacity=0.4, bias=0.005)
            bodies.append(seam)
        bodies.append(Disc([0, -1.55, 0], 0.12, "#34241D", normal=(0, 1, 0), opacity=0.95, stroke="#F5BD71"))

        basket = Block([0, -2.2, 0], [0.7, 0.44, 0.5], "#B77E43", edge="#553B28")
        basket.keep_in_frame = True
        bodies.append(basket)
        # Dark inset and a raised rim make the basket read as an open 3D volume.
        bodies.append(Face([[-0.31, -1.974, -0.21], [0.31, -1.974, -0.21],
                            [0.31, -1.974, 0.21], [-0.31, -1.974, 0.21]], "#3B291D", opacity=1, edge_opacity=0))
        corners = [np.array([x, -1.96, z]) for x, z in ((-0.35, -0.25), (0.35, -0.25), (0.35, 0.25), (-0.35, 0.25))]
        for a, b in zip(corners, corners[1:] + corners[:1]):
            bodies.append(Segment(a, b, "#EDBF7C", width=4, opacity=1))
        for sx in (-1, 1):
            for sz in (-1, 1):
                bodies.append(Segment([sx * 0.1, -1.5, sz * 0.07], [sx * 0.3, -1.97, sz * 0.21],
                                      "#E9D6AF", width=2.3, opacity=0.9))
        for y in np.linspace(-2.36, -2.05, 6):
            for z in (-0.253, 0.253):
                bodies.append(Segment([-0.34, y, z], [0.34, y, z], "#D5A565", width=1.4, opacity=0.72))
            for x in (-0.353, 0.353):
                bodies.append(Segment([x, y, -0.24], [x, y, 0.24], "#D5A565", width=1.4, opacity=0.72))
        for x in np.linspace(-0.29, 0.29, 8):
            for z in (-0.254, 0.254):
                bodies.append(Segment([x, -2.4, z], [x, -2.0, z], "#624128", width=0.8, opacity=0.65))
        bodies.append(BurnerFlame())

        rng = np.random.default_rng(cfg.SEED + 180)
        heights = rng.uniform(0.28, 0.78, 18)
        phi = rng.uniform(0, 2 * np.pi, len(heights))
        radii = np.array([envelope_radius(u) for u in heights]) * np.sqrt(rng.uniform(0.05, 0.65, len(heights)))
        points = np.column_stack([radii * np.cos(phi), 1.95 - 3.5 * heights, radii * np.sin(phi)])
        phase = rng.uniform(0, 2 * np.pi, points.shape)
        self.air = Dots(lambda: points + 0.055 * np.sin(self.clock * 1.3 + phase), "#FFAC6C", radius=0.065)
        self.air.presence = 0.0
        bodies.append(self.air)
        self.leak = 0.0
        signs = np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])

        def escaping_air():
            p = self.leak
            return np.column_stack([signs[:, 0] * (0.06 + 1.1 * p), np.full(4, -1.55 - 1.2 * p),
                                    signs[:, 1] * (0.04 + 0.25 * p)])

        self.escaping = Dots(escaping_air, "#FFAC6C", radius=0.065, alpha=0)
        bodies.append(self.escaping)
        self.add_body(*bodies)

    def release_air(self, **kwargs) -> Param:
        def set_progress(value):
            self.leak = float(value)
            self.escaping.alpha = float(np.sin(np.pi * np.clip(value, 0, 1)))
        return Param(self, lambda: self.leak, set_progress, 1.0, **kwargs)
