"""Simple data models for airflow, drag, and connected-ball scenes."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from utils.math_utils import drag_crisis_cd, reynolds_number


@dataclass(frozen=True)
class DragSample:
    speed: float
    cd: float
    reynolds: float


def drag_curve_samples(critical_speed: float, count: int = 54) -> list[DragSample]:
    """Return samples for an illustrative drag-crisis curve."""

    speeds = np.linspace(5.0, 38.0, count)
    return [
        DragSample(float(v), drag_crisis_cd(float(v), critical_speed=critical_speed), reynolds_number(float(v)))
        for v in speeds
    ]


def airflow_streamlines(center_x: float, center_y: float, radius: float, rough: bool) -> list[list[tuple[float, float, float]]]:
    """Generate stylized 2D streamlines around a ball."""

    lines: list[list[tuple[float, float, float]]] = []
    offsets = [-1.55, -1.05, -0.55, 0.0, 0.55, 1.05, 1.55]
    for i, offset in enumerate(offsets):
        sign = 1 if offset >= 0 else -1
        clearance = max(0.35, abs(offset))
        bend = radius * (0.44 if rough else 0.7) / clearance
        wake = 1.35 if rough else 2.25
        wiggle = 0.0 if rough else 0.12 * ((i % 2) * 2 - 1)
        points = [
            (center_x - 4.0, center_y + offset, 0),
            (center_x - 1.2, center_y + offset + sign * bend * 0.16, 0),
            (center_x + 0.15, center_y + offset + sign * bend * 0.34, 0),
            (center_x + wake, center_y + offset + sign * bend * 0.18 + wiggle, 0),
            (center_x + 4.0, center_y + offset + wiggle * 1.8, 0),
        ]
        lines.append(points)
    return lines


def sensor_pulse_points(count: int = 16) -> list[tuple[float, float]]:
    """Return deterministic pulse samples for a 500 Hz IMU visualization."""

    return [(i / 15, 0.42 * math.sin(i * 1.7) + 0.12 * math.sin(i * 4.4)) for i in range(count)]


def offside_tracking_points() -> dict[str, tuple[float, float, float]]:
    """Return a compact static football-tracking setup."""

    return {
        "attacker": (2.15, 0.65, 0),
        "defender": (1.35, 0.25, 0),
        "passer": (-2.3, -0.55, 0),
        "ball": (-1.75, -0.42, 0),
        "offside_line_top": (1.35, 1.7, 0),
        "offside_line_bottom": (1.35, -1.7, 0),
    }
