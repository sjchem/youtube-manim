"""Small deterministic models behind the film's motion."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class WaveParameters:
    amplitude: float = 1.0
    angular_frequency: float = 1.0
    phase: float = 0.0
    vertical_shift: float = 0.0

    def value(self, theta: float | np.ndarray) -> float | np.ndarray:
        return self.amplitude * np.sin(self.angular_frequency * theta + self.phase) + self.vertical_shift

    @property
    def period(self) -> float:
        return np.inf if self.angular_frequency == 0 else 2 * np.pi / abs(self.angular_frequency)


def combine_tones(theta: float | np.ndarray, amplitudes: tuple[float, ...], frequencies: tuple[float, ...], phases: tuple[float, ...] | None = None) -> float | np.ndarray:
    if len(amplitudes) != len(frequencies):
        raise ValueError("amplitudes and frequencies must have equal length")
    phase_values = phases or tuple(0.0 for _ in amplitudes)
    if len(phase_values) != len(amplitudes):
        raise ValueError("phases and amplitudes must have equal length")
    result = np.zeros_like(theta, dtype=float) if isinstance(theta, np.ndarray) else 0.0
    for amplitude, frequency, phase in zip(amplitudes, frequencies, phase_values, strict=True):
        result = result + amplitude * np.sin(frequency * theta + phase)
    return result
