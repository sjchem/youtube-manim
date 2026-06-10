"""Simple physics-inspired simulation helpers for animation staging."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class BallState:
    position: float = 0.0
    velocity: float = 0.0
    mass: float = 1.0


def apply_force_impulse(state: BallState, impulse: float) -> BallState:
    """Return a new state after an instantaneous impulse."""
    return BallState(
        position=state.position,
        velocity=state.velocity + impulse / state.mass,
        mass=state.mass,
    )


def step_with_friction(state: BallState, dt=0.1, friction=0.18) -> BallState:
    """Integrate one time step with linear drag."""
    drag_accel = -friction * state.velocity / state.mass
    velocity = state.velocity + drag_accel * dt
    position = state.position + velocity * dt
    return BallState(position=position, velocity=velocity, mass=state.mass)


def simulate_rolling(initial_velocity=1.0, friction=0.18, duration=5.0, dt=0.05):
    """Generate position and velocity traces for a rolling ball with drag."""
    state = BallState(velocity=initial_velocity)
    positions = []
    velocities = []
    times = np.arange(0.0, duration + dt, dt)
    for _ in times:
        positions.append(state.position)
        velocities.append(state.velocity)
        state = step_with_friction(state, dt=dt, friction=friction)
    return times, np.asarray(positions), np.asarray(velocities)


def repeated_impulses(steps=12, impulse=0.12, friction=0.06, dt=0.5):
    """Simulate small repeated habit pushes with drag between pushes."""
    state = BallState()
    states = []
    for _ in range(steps):
        state = apply_force_impulse(state, impulse)
        state = step_with_friction(state, dt=dt, friction=friction)
        states.append(state)
    return states


def barrier_crossing_check(kinetic_energy, barrier_height):
    """Whether a simplified kinetic-energy push crosses a barrier."""
    return kinetic_energy >= barrier_height


def kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity**2

