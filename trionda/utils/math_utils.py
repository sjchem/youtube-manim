"""Small math helpers used by the Trionda scenes."""

from __future__ import annotations

import math

AIR_DENSITY = 1.2
AIR_DYNAMIC_VISCOSITY = 1.8e-5
BALL_DIAMETER_M = 0.22


def reynolds_number(speed_m_s: float, diameter_m: float = BALL_DIAMETER_M) -> float:
    """Return a soccer-ball-scale Reynolds number."""

    return AIR_DENSITY * speed_m_s * diameter_m / AIR_DYNAMIC_VISCOSITY


def drag_force(speed_m_s: float, cd: float, area_m2: float = math.pi * (BALL_DIAMETER_M / 2) ** 2) -> float:
    """Return idealized quadratic drag force in newtons."""

    return 0.5 * AIR_DENSITY * cd * area_m2 * speed_m_s**2


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    """Map x smoothly from 0 to 1 between two edges."""

    if edge0 == edge1:
        return 0.0
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3 - 2 * t)


def drag_crisis_cd(speed_m_s: float, critical_speed: float = 20.0, post_cd: float = 0.22, pre_cd: float = 0.48) -> float:
    """A pedagogical drag-crisis curve, not a fitted manufacturer model."""

    transition = smoothstep(critical_speed - 2.5, critical_speed + 2.5, speed_m_s)
    recovery = 0.04 * smoothstep(critical_speed + 6.0, critical_speed + 18.0, speed_m_s)
    return pre_cd * (1 - transition) + post_cd * transition + recovery


def hz_to_period_ms(frequency_hz: float) -> float:
    """Convert a sensor rate to milliseconds per sample."""

    return 1000.0 / frequency_hz
