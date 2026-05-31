"""Simplified physics models used by the Manim scenes.

The values are storytelling models, not CFD or lab-grade collision data.
They are designed to keep force directions and surface comparisons honest.
"""

import math

import numpy as np

from constants import BALL_MASS_KG, BALL_RADIUS_M, CD, G, MAGNUS_K, RHO_AIR


def drag_force(v: np.ndarray, cd: float = CD) -> np.ndarray:
    v = np.array(v, dtype=float)
    speed = np.linalg.norm(v)
    area = math.pi * BALL_RADIUS_M**2
    return -0.5 * RHO_AIR * cd * area * speed * v


def magnus_force(v: np.ndarray, omega: np.ndarray, k: float = MAGNUS_K) -> np.ndarray:
    v3 = np.array([v[0], v[1], 0.0], dtype=float)
    omega3 = np.array(omega, dtype=float)
    return k * np.cross(omega3, v3)[:2]


def spin_projectile_path(v0=(27.0, 8.0), omega_z=-160.0, y0=1.0, duration=1.15, dt=0.02) -> np.ndarray:
    position = np.array([0.0, y0], dtype=float)
    velocity = np.array(v0, dtype=float)
    points = []
    for _ in np.arange(0, duration, dt):
        points.append(position.copy())
        fg = np.array([0.0, -BALL_MASS_KG * G])
        acceleration = (fg + drag_force(velocity) + magnus_force(velocity, np.array([0.0, 0.0, omega_z]))) / BALL_MASS_KG
        velocity += acceleration * dt
        position += velocity * dt
        if position[1] < 0:
            position[1] = 0
            break
    return np.array(points)


def bounce_model(v_in: np.ndarray, omega_in: float, surface_type: str = "clay") -> tuple[np.ndarray, float]:
    if surface_type == "clay":
        alpha, beta, gamma, e = 0.58, 0.58, 0.14, 0.76
    elif surface_type == "grass":
        alpha, beta, gamma, e = 0.88, 0.66, 0.03, 0.72
    else:
        alpha, beta, gamma, e = 0.82, 0.72, 0.05, 0.82
    vx, vy = float(v_in[0]), float(v_in[1])
    return np.array([alpha * vx, -e * vy]), beta * omega_in + gamma * vx
