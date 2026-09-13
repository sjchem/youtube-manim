"""Numerical machinery shared by the chapters.

Nothing here knows about Manim. These are the equations and the integrator; the
scenes turn their output into pictures. Keeping the split sharp means a number
spoken in the narration and a number drawn on screen come from the same place.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants (CODATA-rounded, in SI unless stated otherwise)
# ---------------------------------------------------------------------------

PLANCK = 6.62607015e-34  # J s
LIGHT_SPEED = 2.99792458e8  # m/s
ELEMENTARY_CHARGE = 1.602176634e-19  # C
ELECTRON_MASS = 9.1093837015e-31  # kg
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m
CLASSICAL_ELECTRON_RADIUS = 2.8179403262e-15  # m
BOHR_RADIUS = 5.29177210903e-11  # m
RYDBERG_ENERGY = 2.1798723611e-18  # J, the hydrogen ionisation energy
JOULE_PER_EV = ELEMENTARY_CHARGE

# Sizes the film quotes out loud. These are order-of-magnitude figures, which is
# exactly how the evidence supports them.
ATOM_RADIUS = 1.0e-10  # m
NUCLEUS_RADIUS = 1.0e-15  # m
ELECTRON_CHARGE_TO_MASS = 1.75882001076e11  # C/kg, Thomson's measured e/m
PROTON_TO_ELECTRON_MASS = 1836.15267343
# A hydrogen atom is a proton plus an electron, which is the comparison the
# film actually makes out loud, and it rounds to the familiar 1837.
HYDROGEN_TO_ELECTRON_MASS = PROTON_TO_ELECTRON_MASS + 1.0


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------


def clamp(value: float, low: float, high: float) -> float:
    return float(min(max(value, low), high))


def integrate_ode(
    derivative: Callable[[float, np.ndarray], np.ndarray],
    state: Sequence[float],
    t_span: tuple[float, float],
    steps: int,
) -> np.ndarray:
    """Fixed-step RK4. Returns an array of states, one row per step boundary."""
    t0, t1 = t_span
    dt = (t1 - t0) / steps
    current = np.array(state, dtype=float)
    trajectory = np.empty((steps + 1, current.size), dtype=float)
    trajectory[0] = current
    t = t0
    for index in range(steps):
        k1 = derivative(t, current)
        k2 = derivative(t + dt / 2, current + dt / 2 * k1)
        k3 = derivative(t + dt / 2, current + dt / 2 * k2)
        k4 = derivative(t + dt, current + dt * k3)
        current = current + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        trajectory[index + 1] = current
        t += dt
    return trajectory


# ---------------------------------------------------------------------------
# Coulomb scattering
# ---------------------------------------------------------------------------


def coulomb_derivative(strength: float) -> Callable[[float, np.ndarray], np.ndarray]:
    """State [x, y, vx, vy] under a repulsive 1/r^2 force from the origin.

    `strength` collects charge, mass, and 1/(4 pi eps0) into one number, which
    is all the geometry of the trajectory depends on.
    """

    def derivative(_t: float, state: np.ndarray) -> np.ndarray:
        position = state[:2]
        distance = float(np.hypot(position[0], position[1]))
        # A softening floor keeps a numerically exact head-on shot finite; a real
        # alpha particle stops and reverses at the distance of closest approach.
        safe = max(distance, 1e-4)
        acceleration = strength * position / safe**3
        return np.array([state[2], state[3], acceleration[0], acceleration[1]])

    return derivative


def rutherford_angle(impact_parameter: float, strength: float, speed: float) -> float:
    """Exact Coulomb scattering angle in radians: tan(theta/2) = k / (b v^2)."""
    if impact_parameter <= 1e-9:
        return float(np.pi)
    return float(2.0 * np.arctan(strength / (impact_parameter * speed**2)))


def closest_approach(impact_parameter: float, strength: float, speed: float) -> float:
    """Distance of closest approach for a repulsive Coulomb encounter."""
    half = 0.5 * strength / speed**2
    return float(half + np.hypot(half, impact_parameter))


# ---------------------------------------------------------------------------
# Classical collapse: the problem the film opens with
# ---------------------------------------------------------------------------


def larmor_collapse_time(initial_radius: float = BOHR_RADIUS) -> float:
    """How long classical electromagnetism gives a circling electron to live.

    Integrating the Larmor radiated power against the orbital energy gives
    t = r0^3 / (4 c re^2), about 1.6e-11 s from the Bohr radius. The film quotes
    this only as an order of magnitude, which is all the estimate deserves.
    """
    return float(initial_radius**3 / (4.0 * LIGHT_SPEED * CLASSICAL_ELECTRON_RADIUS**2))


def collapse_radius(fraction_elapsed: float, initial_radius: float = 1.0) -> float:
    """Orbit radius after a given fraction of the collapse time: r = r0 (1-t/T)^(1/3)."""
    remaining = clamp(1.0 - fraction_elapsed, 0.0, 1.0)
    return float(initial_radius * remaining ** (1.0 / 3.0))


def collapse_spiral(
    initial_radius: float,
    turns: float,
    samples: int = 700,
    final_radius_fraction: float = 0.035,
) -> np.ndarray:
    """The in-spiral as (x, y) points, shrinking the way the radiation law says.

    Angle advances faster as the orbit tightens, because a smaller orbit is a
    faster one. That acceleration is the part an audience actually feels.
    """
    fractions = np.linspace(0.0, 1.0 - final_radius_fraction**3, samples)
    radii = np.array([collapse_radius(f, initial_radius) for f in fractions])
    # Kepler-like speed-up: angular rate scales as r^(-3/2).
    rates = (radii / initial_radius) ** -1.5
    angles = np.cumsum(rates)
    angles = angles / angles[-1] * (turns * 2.0 * np.pi)
    return np.column_stack((radii * np.cos(angles), radii * np.sin(angles)))


# ---------------------------------------------------------------------------
# Hydrogen: energies, transitions, and the colours they produce
# ---------------------------------------------------------------------------


def hydrogen_energy_joules(n: int) -> float:
    """E_n = -2.18e-18 J / n^2."""
    return float(-RYDBERG_ENERGY / (n * n))


def hydrogen_energy_ev(n: int) -> float:
    return float(hydrogen_energy_joules(n) / JOULE_PER_EV)


def transition_energy(n_high: int, n_low: int) -> float:
    """Energy released, in joules, when an electron falls from n_high to n_low."""
    return float(hydrogen_energy_joules(n_low) - hydrogen_energy_joules(n_high)) * -1.0


def photon_wavelength_nm(n_high: int, n_low: int) -> float:
    """The emitted wavelength in nanometres, from Delta E = h nu and c = lambda nu."""
    energy = abs(transition_energy(n_high, n_low))
    return float(PLANCK * LIGHT_SPEED / energy * 1e9)


def wavelength_to_hex(wavelength_nm: float, gamma: float = 0.85) -> str:
    """An approximate sRGB rendering of a single visible wavelength.

    Piecewise linear in the classic Bruton style, with the intensity rolled off
    at both ends of the visible band. It is a perceptual convenience for the
    prism and the line spectrum, not a colorimetric claim.
    """
    w = float(wavelength_nm)
    if w < 380 or w > 780:
        return "#101820"
    if w < 440:
        red, green, blue = -(w - 440) / 60.0, 0.0, 1.0
    elif w < 490:
        red, green, blue = 0.0, (w - 440) / 50.0, 1.0
    elif w < 510:
        red, green, blue = 0.0, 1.0, -(w - 510) / 20.0
    elif w < 580:
        red, green, blue = (w - 510) / 70.0, 1.0, 0.0
    elif w < 645:
        red, green, blue = 1.0, -(w - 645) / 65.0, 0.0
    else:
        red, green, blue = 1.0, 0.0, 0.0

    if w < 420:
        factor = 0.3 + 0.7 * (w - 380) / 40.0
    elif w > 700:
        factor = 0.3 + 0.7 * (780 - w) / 80.0
    else:
        factor = 1.0

    channels = [int(round(255 * (value * factor) ** gamma)) for value in (red, green, blue)]
    return "#{:02X}{:02X}{:02X}".format(*(clamp_channel(c) for c in channels))


def clamp_channel(value: int) -> int:
    return int(min(max(value, 0), 255))


# ---------------------------------------------------------------------------
# Scale
# ---------------------------------------------------------------------------


def scaled_atom_radius(nucleus_display_radius_m: float) -> float:
    """If the nucleus were this big, how far away would the edge of the atom be?"""
    return float(nucleus_display_radius_m * ATOM_RADIUS / NUCLEUS_RADIUS)
