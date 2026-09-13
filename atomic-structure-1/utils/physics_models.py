"""One dataclass per experiment in the film.

Each model owns the physics of a single chapter: what it predicts, what it
produces, and the handful of numbers the narration is allowed to say out loud.
Scenes ask these objects for trajectories and values instead of hard-coding
them, so the picture and the voice-over cannot drift apart.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from utils.math_utils import (
    ATOM_RADIUS,
    ELECTRON_CHARGE_TO_MASS,
    HYDROGEN_TO_ELECTRON_MASS,
    NUCLEUS_RADIUS,
    closest_approach,
    collapse_spiral,
    coulomb_derivative,
    hydrogen_energy_ev,
    integrate_ode,
    larmor_collapse_time,
    photon_wavelength_nm,
    rutherford_angle,
    scaled_atom_radius,
    wavelength_to_hex,
)


# ---------------------------------------------------------------------------
# Scene 4: the cathode-ray tube
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CathodeRayTube:
    """A charged beam crossing a uniform transverse field.

    Inside the plates the path is a parabola, exactly like a thrown ball in
    gravity; outside them it is a straight line along the exit velocity. That
    two-part shape is the whole visual argument that the rays carry charge.
    """

    plate_start: float = -1.2
    plate_end: float = 1.2
    deflection: float = 1.05

    @property
    def plate_length(self) -> float:
        return self.plate_end - self.plate_start

    def offset(self, x: float) -> float:
        """Transverse displacement of the beam at horizontal position `x`."""
        if x <= self.plate_start:
            return 0.0
        if x <= self.plate_end:
            fraction = (x - self.plate_start) / self.plate_length
            return float(self.deflection * fraction**2)
        # Leaving the field, the beam keeps the slope it acquired at the exit.
        exit_slope = 2.0 * self.deflection / self.plate_length
        return float(self.deflection + exit_slope * (x - self.plate_end))

    def path_points(self, x_start: float, x_end: float, samples: int = 160) -> np.ndarray:
        xs = np.linspace(x_start, x_end, samples)
        return np.column_stack((xs, [self.offset(float(x)) for x in xs]))

    @property
    def charge_to_mass(self) -> float:
        """Thomson's measured e/m for the cathode-ray particle, in C/kg."""
        return ELECTRON_CHARGE_TO_MASS

    @property
    def mass_ratio_to_hydrogen(self) -> float:
        """How many electrons it takes to weigh as much as one hydrogen atom."""
        return HYDROGEN_TO_ELECTRON_MASS


# ---------------------------------------------------------------------------
# Scenes 5 and 6: two atoms, two predictions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ThomsonAtom:
    """Positive charge smeared through the whole atom, electrons embedded in it.

    Because the charge is spread out, the field an alpha particle meets is
    feeble everywhere, and every deflection is a fraction of a degree. The film
    exaggerates that angle so the audience can see it at all, and says so.
    """

    radius: float = 1.0
    max_deflection_degrees: float = 0.9

    def deflection_angle(self, impact_parameter: float) -> float:
        """Radians. Largest for a shot that grazes the middle of the sphere."""
        reach = abs(impact_parameter) / self.radius
        if reach >= 1.0:
            return 0.0
        # Inside a uniform sphere the enclosed charge grows as r^3, so the
        # sideways impulse peaks part-way out rather than dead centre.
        shape = reach * (1.0 - reach**2)
        peak = 2.0 / (3.0 * np.sqrt(3.0))
        return float(np.deg2rad(self.max_deflection_degrees) * shape / peak)

    def path_points(
        self,
        impact_parameter: float,
        x_start: float,
        x_end: float,
        samples: int = 120,
    ) -> np.ndarray:
        """A nearly straight line with one gentle bend as it crosses the sphere."""
        angle = self.deflection_angle(impact_parameter) * np.sign(impact_parameter or 1.0)
        xs = np.linspace(x_start, x_end, samples)
        ys = []
        for x in xs:
            if x <= -self.radius:
                ys.append(impact_parameter)
                continue
            # Integrate a smoothstep slope inside the cloud. At the exit,
            # retain the acquired direction instead of flattening the trajectory.
            slope = np.tan(angle)
            if x >= self.radius:
                offset = slope * x
            else:
                progress = (x + self.radius) / (2.0 * self.radius)
                offset = slope * 2.0 * self.radius * (progress**3 - 0.5 * progress**4)
            ys.append(impact_parameter + offset)
        return np.column_stack((xs, ys))


@dataclass(frozen=True)
class RutherfordScattering:
    """All the positive charge in one point, and the trajectories that follow.

    `strength` folds the charges, the alpha particle's mass, and the Coulomb
    constant into a single number, which is all the *shape* of a trajectory
    depends on. The angles are the exact Coulomb result; only the length scale
    is chosen to make the picture readable.
    """

    strength: float = 0.42
    speed: float = 1.0
    entry_x: float = -7.0

    def deflection_angle(self, impact_parameter: float) -> float:
        return rutherford_angle(abs(impact_parameter), self.strength, self.speed)

    def closest_approach(self, impact_parameter: float) -> float:
        return closest_approach(abs(impact_parameter), self.strength, self.speed)

    def trajectory(self, impact_parameter: float, steps: int = 900, span: float = 15.0) -> np.ndarray:
        """Integrate the real repulsive Coulomb motion; returns (x, y) points."""
        state = [self.entry_x, float(impact_parameter), self.speed, 0.0]
        history = integrate_ode(
            coulomb_derivative(self.strength),
            state,
            (0.0, span / self.speed),
            steps,
        )
        return history[:, :2]

    def screen_trajectory(self, impact_parameter: float, screen_radius: float, **kwargs) -> np.ndarray:
        """The path from the source until it first reaches the detector ring.

        Clipping on radius rather than on the frame edge is what makes the
        picture coherent: a particle stops where its flash appears. The cut is
        taken after the closest approach, so the incoming leg is never mistaken
        for an arrival -- which matters for the shot that turns around and
        leaves through the side it came in.
        """
        points = self.trajectory(impact_parameter, **kwargs)
        radii = np.hypot(points[:, 0], points[:, 1])
        closest = int(np.argmin(radii))
        beyond = np.flatnonzero(radii[closest:] >= screen_radius)
        stop = closest + int(beyond[0]) + 1 if beyond.size else len(points)
        return points[: max(stop, 2)]

    @property
    def backscatter_fraction(self) -> float:
        """Roughly one alpha particle in twenty thousand came almost straight back."""
        return 1.0 / 20000.0


# ---------------------------------------------------------------------------
# Scene 7: the scale of the thing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AtomicScale:
    """Order-of-magnitude sizes, and the analogy the film draws from them."""

    atom_radius: float = ATOM_RADIUS
    nucleus_radius: float = NUCLEUS_RADIUS
    cricket_ball_radius: float = 0.036  # m, a regulation ball is about 7.2 cm across

    @property
    def radius_ratio(self) -> float:
        return float(self.atom_radius / self.nucleus_radius)

    @property
    def volume_ratio(self) -> float:
        return float(self.radius_ratio**3)

    @property
    def cricket_ball_atom_radius_km(self) -> float:
        """Scale the nucleus up to a cricket ball; how far is the atom's edge?"""
        return float(self.cricket_ball_radius * self.radius_ratio / 1000.0)


# ---------------------------------------------------------------------------
# Scene 8: the atom that should not survive
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ClassicalCollapse:
    """An accelerating charge radiates, so a classical orbit must spiral in."""

    display_radius: float = 2.6
    turns: float = 5.5

    @property
    def lifetime_seconds(self) -> float:
        return larmor_collapse_time()

    @property
    def lifetime_picoseconds(self) -> float:
        return float(self.lifetime_seconds * 1e12)

    def spiral(self, samples: int = 700) -> np.ndarray:
        return collapse_spiral(self.display_radius, self.turns, samples)


# ---------------------------------------------------------------------------
# Scenes 9 to 12: light, and the ladder behind it
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HydrogenAtom:
    """Bohr's hydrogen: allowed energies, the jumps between them, and the colours."""

    max_level: int = 6

    def energy_ev(self, n: int) -> float:
        return hydrogen_energy_ev(n)

    def level_height(self, n: int) -> float:
        """A screen height for level n, normalised so n=1 sits at 0 and n=inf at 1."""
        return float(1.0 - 1.0 / (n * n))

    def transition_energy_ev(self, n_high: int, n_low: int) -> float:
        return float(self.energy_ev(n_high) - self.energy_ev(n_low))

    def wavelength_nm(self, n_high: int, n_low: int) -> float:
        return photon_wavelength_nm(n_high, n_low)

    def color(self, n_high: int, n_low: int) -> str:
        return wavelength_to_hex(self.wavelength_nm(n_high, n_low))

    def balmer_series(self, highest: int = 6) -> list[tuple[int, float, str]]:
        """Selected Balmer jumps down to n = 2: level, wavelength and colour."""
        lines = []
        for n in range(3, highest + 1):
            wavelength = self.wavelength_nm(n, 2)
            lines.append((n, wavelength, wavelength_to_hex(wavelength)))
        return lines


# ---------------------------------------------------------------------------
# Scene 2: the dark-room analogy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HiddenObject:
    """An unseen shape in a dark room, and the balls that bounce off it.

    This is the film's opening analogy, and it is only an analogy: real alpha
    particles are deflected by a field they never touch, not by a hard surface.
    What survives the comparison is the method -- learn a shape from the way
    things come back off it.
    """

    center: tuple[float, float] = (1.1, 0.0)
    radius: float = 1.25

    def hits(self, launch_height: float) -> bool:
        return abs(launch_height - self.center[1]) < self.radius

    def impact_point(self, launch_height: float) -> np.ndarray | None:
        """Where a ball fired horizontally from the left first touches the surface."""
        if not self.hits(launch_height):
            return None
        offset = launch_height - self.center[1]
        x = self.center[0] - float(np.sqrt(self.radius**2 - offset**2))
        return np.array([x, launch_height])

    def path_points(self, launch_height: float, x_start: float = -7.2, reach: float = 15.0) -> np.ndarray:
        """The full trajectory: in, and (if it strikes) back out along the reflection."""
        impact = self.impact_point(launch_height)
        if impact is None:
            return np.array([[x_start, launch_height], [-x_start, launch_height]])
        normal = (impact - np.array(self.center)) / self.radius
        direction = np.array([1.0, 0.0])
        reflected = direction - 2.0 * float(np.dot(direction, normal)) * normal
        exit_point = impact + reflected * reach
        return np.array([[x_start, launch_height], impact, exit_point])
