"""Small rendering and data helpers for scenes."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np

from utils.math_utils import game_win_probability

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"


def ensure_output_dir(subdir: str | None = None) -> Path:
    """Create and return the output directory or one of its children."""

    path = OUTPUT_DIR if subdir is None else OUTPUT_DIR / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path


def probability_curve(samples: int = 201) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return p, G(p), and amplification arrays."""

    p_values = np.linspace(0, 1, samples)
    g_values = np.array([game_win_probability(float(p)) for p in p_values])
    return p_values, g_values, g_values - p_values


def write_frame_names(prefix: str, count: int) -> Iterable[str]:
    """Yield zero-padded frame names."""

    for index in range(count):
        yield f"{prefix}_{index:04d}.png"
