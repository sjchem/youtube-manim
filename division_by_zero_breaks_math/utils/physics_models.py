"""Render-friendly particle helpers with optional manim-physics support."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from manim import ORIGIN, Dot, VGroup
from manim import config as manim_config

try:  # Optional import. The scenes work without it.
    from manim_physics import SpaceScene  # type: ignore

    HAS_MANIM_PHYSICS = True
except Exception:  # pragma: no cover - depends on local optional plugin state.
    SpaceScene = object  # type: ignore
    HAS_MANIM_PHYSICS = False


@dataclass(frozen=True)
class ParticleSpec:
    count: int = 36
    radius: float = 0.035
    spread: float = 2.5
    seed: int = 7


def particle_cloud(color, spec: ParticleSpec = ParticleSpec()) -> VGroup:
    """Create a deterministic particle cloud for collapse and glitch effects."""

    rng = Random(spec.seed)
    particles = VGroup()
    for _ in range(spec.count):
        dot = Dot(radius=spec.radius, color=color)
        dot.move_to(
            [
                rng.uniform(-spec.spread, spec.spread),
                rng.uniform(-spec.spread * 0.55, spec.spread * 0.55),
                0,
            ]
        )
        particles.add(dot)
    return particles


def center_targets(count: int):
    """Return repeated center targets for Transform animations."""

    return [ORIGIN.copy() for _ in range(count)]
