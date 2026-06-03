"""Lightweight conceptual motion models for the animations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParticleStep:
    start: float
    end: float
    delta: float


def particle_motion_1d(start: float, step: float, repeats: int) -> list[ParticleStep]:
    """Return repeated 1D motion segments."""
    position = start
    steps: list[ParticleStep] = []
    for _ in range(repeats):
        new_position = position + step
        steps.append(ParticleStep(position, new_position, step))
        position = new_position
    return steps


def reverse_direction(value: float) -> float:
    """Model multiplication by -1 as a direction reversal."""
    return -value


def mirror_flip(value: float, mirrors: int = 1) -> float:
    """Apply a mirror flip repeatedly."""
    result = value
    for _ in range(mirrors):
        result = -result
    return result


def balance_torque(left_value: float, right_value: float) -> dict[str, float | bool]:
    """Conceptual balance scale values; equal opposite values balance."""
    total = left_value + right_value
    return {
        "left": left_value,
        "right": right_value,
        "net": total,
        "balanced": abs(total) < 1e-9,
    }
