"""Conceptual physics models for the Magnus effect animation.

The numerical model is intentionally lightweight. It is not a match predictor;
it gives the scenes physically sensible trajectories and force directions.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt

from utils.math_utils import left_normal


@dataclass(frozen=True)
class FreeKickParams:
    """Minimal 2D top-view free-kick model."""

    mass: float = 0.43
    diameter: float = 0.22
    air_density: float = 1.2
    drag_coefficient: float = 0.25
    magnus_coefficient: float = 0.30
    spin_sign: float = 1.0
    dt: float = 0.025
    duration: float = 1.15
    initial_speed: float = 26.0
    launch_lateral_speed: float = -2.25


@dataclass(frozen=True)
class TrajectorySample:
    """One step of the top-view flight path."""

    t: float
    x: float
    y: float
    vx: float
    vy: float
    magnus_ax: float
    magnus_ay: float


def ball_area(diameter: float) -> float:
    """Return frontal area for a soccer ball."""
    radius = diameter / 2.0
    return pi * radius * radius


def aerodynamic_scale(params: FreeKickParams, speed: float) -> float:
    """Return dynamic-pressure area divided by mass."""
    return 0.5 * params.air_density * ball_area(params.diameter) * speed * speed / params.mass


def simulate_free_kick_2d(params: FreeKickParams = FreeKickParams()) -> list[TrajectorySample]:
    """Integrate a simple top-view shot with drag and a lateral Magnus force."""
    x = 0.0
    y = -1.95
    vx = params.initial_speed
    vy = params.launch_lateral_speed
    samples: list[TrajectorySample] = []
    steps = int(params.duration / params.dt)

    for step in range(steps + 1):
        t = step * params.dt
        speed = max(1e-6, sqrt(vx * vx + vy * vy))
        nx, ny = left_normal((vx, vy))
        scale = aerodynamic_scale(params, speed)
        drag_ax = -params.drag_coefficient * scale * vx / speed
        drag_ay = -params.drag_coefficient * scale * vy / speed
        magnus_ax = params.spin_sign * params.magnus_coefficient * scale * nx
        magnus_ay = params.spin_sign * params.magnus_coefficient * scale * ny

        samples.append(TrajectorySample(t, x, y, vx, vy, magnus_ax, magnus_ay))

        vx += (drag_ax + magnus_ax) * params.dt
        vy += (drag_ay + magnus_ay) * params.dt
        x += vx * params.dt
        y += vy * params.dt

    return samples


def straight_reference(samples: list[TrajectorySample]) -> list[tuple[float, float]]:
    """Return the no-Magnus straight reference using the first velocity."""
    if not samples:
        return []
    first = samples[0]
    return [(s.x, first.y + first.vy / max(first.vx, 1e-6) * s.x) for s in samples]


def trajectory_points(samples: list[TrajectorySample]) -> list[tuple[float, float]]:
    """Return x-y points from samples."""
    return [(sample.x, sample.y) for sample in samples]


def force_vectors(samples: list[TrajectorySample], every: int = 8) -> list[tuple[float, float, float, float]]:
    """Return sparse force vectors as x, y, ax, ay tuples."""
    vectors = []
    for sample in samples[2::every]:
        vectors.append((sample.x, sample.y, sample.magnus_ax, sample.magnus_ay))
    return vectors


def drag_crisis_profile(critical_speed_kmh: float = 43.0) -> list[tuple[float, float]]:
    """Return a schematic drag coefficient curve vs speed in km/h."""
    points: list[tuple[float, float]] = []
    for speed in range(20, 101, 2):
        before = 0.48 - 0.002 * (speed - 20)
        drop = 0.18 / (1.0 + pow(2.71828, -(speed - critical_speed_kmh) / 2.6))
        after_rise = 0.0016 * max(0, speed - critical_speed_kmh)
        cd = before - drop + after_rise
        points.append((float(speed), cd))
    return points


def world_cup_ball_milestones() -> list[dict[str, str | int]]:
    """Return concise ball-history milestones for the montage."""
    return [
        {"year": 1930, "name": "Tiento / T-Model", "note": "leather"},
        {"year": 1970, "name": "Telstar", "note": "32 panels"},
        {"year": 2010, "name": "Jabulani", "note": "8 panels"},
        {"year": 2014, "name": "Brazuca", "note": "6 panels"},
        {"year": 2022, "name": "Al Rihla", "note": "20 panels"},
        {"year": 2026, "name": "Trionda", "note": "4 panels"},
    ]
