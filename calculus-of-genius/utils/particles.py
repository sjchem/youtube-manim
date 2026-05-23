from __future__ import annotations

import numpy as np
from manim import *

from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, PURPLE_GLOW, RED_GLOW

try:
    from manim_physics import *  # noqa: F401,F403

    MANIM_PHYSICS_AVAILABLE = True
except Exception as exc:  # pragma: no cover - depends on local install
    print(f"[calculus-of-genius] manim_physics unavailable, using native fallback particles: {exc}")
    MANIM_PHYSICS_AVAILABLE = False


class RandomWalker(VGroup):
    """Small bounded Brownian particle system for chaos metaphors."""

    def __init__(
        self,
        count: int = 45,
        bounds: tuple[float, float, float, float] = (-2.0, 2.0, -1.5, 1.5),
        color: str = BLUE_GLOW,
        seed: int = 1,
        step: float = 0.45,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.bounds = bounds
        self.step = step
        self.rng = np.random.default_rng(seed)
        x_min, x_max, y_min, y_max = bounds
        for _ in range(count):
            dot = Dot(
                point=np.array([self.rng.uniform(x_min, x_max), self.rng.uniform(y_min, y_max), 0]),
                radius=0.025,
                color=color,
                fill_opacity=0.75,
            )
            dot.velocity = self.rng.normal(0, 0.45, 3) * np.array([1, 1, 0])
            self.add(dot)
        self.add_updater(self._update_particles)

    def _update_particles(self, mob: VGroup, dt: float) -> None:
        x_min, x_max, y_min, y_max = self.bounds
        for dot in mob:
            jitter = self.rng.normal(0, self.step, 3) * np.array([1, 1, 0])
            dot.velocity = 0.82 * dot.velocity + jitter * dt
            dot.shift(dot.velocity * dt)
            x, y, _ = dot.get_center()
            if x < x_min or x > x_max:
                dot.velocity[0] *= -1
            if y < y_min or y > y_max:
                dot.velocity[1] *= -1


class AttractorParticleSystem(VGroup):
    """Native attractor-based particles, used as the stable fallback physics metaphor."""

    def __init__(
        self,
        count: int = 64,
        attractors: list[np.ndarray] | None = None,
        bounds: tuple[float, float, float, float] = (-3, 3, -2, 2),
        color: str = GREEN_GLOW,
        seed: int = 4,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.bounds = bounds
        self.rng = np.random.default_rng(seed)
        self.attractors = attractors or [LEFT, RIGHT, UP * 0.8]
        x_min, x_max, y_min, y_max = bounds
        for _ in range(count):
            p = Dot(
                point=np.array([self.rng.uniform(x_min, x_max), self.rng.uniform(y_min, y_max), 0]),
                radius=self.rng.uniform(0.018, 0.035),
                color=color,
                fill_opacity=self.rng.uniform(0.45, 0.9),
            )
            p.velocity = self.rng.normal(0, 0.22, 3) * np.array([1, 1, 0])
            self.add(p)
        self.add_updater(self._update_particles)

    def _update_particles(self, mob: VGroup, dt: float) -> None:
        x_min, x_max, y_min, y_max = self.bounds
        for dot in mob:
            pos = dot.get_center()
            force = np.zeros(3)
            for attractor in self.attractors:
                delta = attractor - pos
                dist = max(np.linalg.norm(delta), 0.25)
                force += delta / (dist**2.0)
            swirl = np.array([-force[1], force[0], 0]) * 0.22
            dot.velocity = 0.93 * dot.velocity + (0.32 * force + swirl) * dt
            dot.shift(dot.velocity * dt)
            x, y, _ = dot.get_center()
            if x < x_min or x > x_max:
                dot.velocity[0] *= -0.8
            if y < y_min or y > y_max:
                dot.velocity[1] *= -0.8


class IdeaParticle(Dot):
    def __init__(self, point: np.ndarray, color: str = BLUE_GLOW, label: str | None = None, **kwargs) -> None:
        super().__init__(point=point, radius=0.07, color=color, **kwargs)
        self.label = label


def create_idea_collision_animation(scene: Scene, particles: VGroup, center: np.ndarray = ORIGIN) -> VGroup:
    molecule = VGroup()
    for i, p in enumerate(particles):
        angle = TAU * i / max(len(particles), 1)
        target = center + np.array([np.cos(angle), np.sin(angle), 0]) * 0.48
        molecule.add(Line(center, target, color=PURPLE_GLOW, stroke_width=2, stroke_opacity=0.55))
    core = Dot(center, radius=0.12, color=GOLD_GLOW)
    molecule.add(core)
    scene.play(*[p.animate.move_to(molecule[i].get_end()) for i, p in enumerate(particles)], run_time=1.3, lag_ratio=0.05)
    scene.play(FadeIn(molecule), run_time=0.7)
    return molecule


def create_edge_of_chaos_particles(center: np.ndarray = ORIGIN, count: int = 72, seed: int = 9) -> AttractorParticleSystem:
    attractors = [
        center + np.array([0.0, 0.7, 0]),
        center + np.array([-0.9, -0.5, 0]),
        center + np.array([0.9, -0.45, 0]),
    ]
    return AttractorParticleSystem(
        count=count,
        attractors=attractors,
        bounds=(center[0] - 1.65, center[0] + 1.65, center[1] - 1.15, center[1] + 1.15),
        color=GREEN_GLOW,
        seed=seed,
    )


def optional_charge_field() -> VGroup:
    """Return a tiny manim-physics field if available, otherwise an empty group."""
    if not MANIM_PHYSICS_AVAILABLE:
        return VGroup()
    try:
        charge_a = Charge(-1, LEFT * 0.8)  # type: ignore[name-defined]
        charge_b = Charge(1, RIGHT * 0.8)  # type: ignore[name-defined]
        field = ElectricField(charge_a, charge_b)  # type: ignore[name-defined]
        field.set_opacity(0.22)
        return VGroup(field, charge_a, charge_b)
    except Exception:
        return VGroup()
