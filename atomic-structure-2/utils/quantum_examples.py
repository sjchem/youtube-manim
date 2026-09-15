"""SI calculations used by the film's three linked worked examples.

The momentum and wavelength example is nonrelativistic. The hydrogen energies
use a fixed nucleus, matching the normalized hydrogen states in physics_models.
"""

from __future__ import annotations

from scipy.constants import (
    Rydberg,
    alpha,
    c,
    electron_mass,
    elementary_charge,
    h,
    hbar,
    physical_constants,
)


def electron_wavelength(speed: float) -> float:
    """Return h/(m_e v), in metres, for a positive nonrelativistic speed."""
    if speed <= 0:
        raise ValueError("Speed must be positive")
    return h / (electron_mass * speed)


def minimum_momentum_spread(position_spread: float) -> float:
    """The lower bound hbar/(2 sigma_x), in kg m/s, reached by our Gaussian."""
    if position_spread <= 0:
        raise ValueError("Position spread must be positive")
    return hbar / (2 * position_spread)


def hydrogen_energy(n: int) -> float:
    """Bound-state energy in eV relative to a separated electron and proton."""
    if n < 1 or int(n) != n:
        raise ValueError("Principal quantum number must be a positive integer")
    return -Rydberg * h * c / elementary_charge / n**2


# ---------------------------------------------------------------------------
# Bohr's own numbers
#
# Chapter 3 puts these on screen as the model's promise, and chapters 4, 6 and 7
# spend them: the n = 1 speed becomes a de Broglie wavelength, that wavelength
# turns out to be exactly one circumference, and the classical trajectory
# additionally assigns exact position and momentum vectors at each instant.
# ---------------------------------------------------------------------------


def bohr_radius(n: int = 1) -> float:
    """Orbit radius n^2 a0, in metres, for the hydrogen Bohr model."""
    if n < 1 or int(n) != n:
        raise ValueError("Principal quantum number must be a positive integer")
    return n * n * physical_constants["Bohr radius"][0]


def bohr_speed(n: int = 1) -> float:
    """Orbital speed alpha c / n, in metres per second."""
    if n < 1 or int(n) != n:
        raise ValueError("Principal quantum number must be a positive integer")
    return alpha * c / n


def bohr_momentum(n: int = 1) -> float:
    """Nonrelativistic m_e v for the Bohr orbit: a magnitude, not an uncertainty."""
    return electron_mass * bohr_speed(n)


def de_broglie_wavelength(mass: float, speed: float) -> float:
    """h/(m v), in metres, for any nonrelativistic mass and speed."""
    if mass <= 0 or speed <= 0:
        raise ValueError("Mass and speed must be positive")
    return h / (mass * speed)

def two_slit_probability(y, coherence: float = 1.0, wavenumber: float = 3.2,
                         envelope: float = 1.75):
    """Unnormalized intensity for equal Gaussian amplitudes in a far-field model.

    A1 = sqrt(g/2) exp(iky), A2 = sqrt(g/2) exp(-iky).
    The real detector-state overlap multiplies only the cross term.
    Distinguishable paths retain the same diffraction envelope.
    Coordinates are schematic screen units, not apparatus calibration.
    """
    import numpy as np
    if not 0 <= coherence <= 1 or envelope <= 0:
        raise ValueError("Coherence must lie in [0, 1], and envelope must be positive")
    y = np.asarray(y)
    g = np.exp(-y**2 / (2 * envelope**2))
    return g * (1 + coherence * np.cos(2 * wavenumber * y))


def hydrogen_1s_cumulative(radius):
    """Probability inside R/a0 for 1s: integral of 4r² exp(-2r).

    This is a spherical volume integral, not a disk integral through a slice.
    """
    import numpy as np
    r = np.asarray(radius, dtype=float)
    if np.any(r < 0):
        raise ValueError("Radius must be nonnegative")
    return -np.expm1(-2 * r) - np.exp(-2 * r) * (2 * r + 2 * r**2)


def hydrogen_1s_probability_radius(fraction: float = 0.9) -> float:
    """Radius in a0 enclosing a requested fraction of 1s probability."""
    from scipy.optimize import brentq
    if not 0 < fraction < 1:
        raise ValueError("Fraction must lie strictly between zero and one")
    return brentq(lambda r: hydrogen_1s_cumulative(r) - fraction, 0, 100)
