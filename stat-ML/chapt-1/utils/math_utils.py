"""Mathematical utilities for the statistics animations."""

from __future__ import annotations

import numpy as np


def noisy_sine_data(
    n: int = 60,
    x_range: tuple[float, float] = (-6.5, 6.5),
    amplitude: float = 1.5,
    freq: float = 0.65,
    noise_std: float = 0.40,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (xs, ys_noisy, ys_true) for a noisy sine wave dataset."""
    rng = np.random.default_rng(seed)
    xs = rng.uniform(x_range[0], x_range[1], n)
    ys_true = amplitude * np.sin(freq * xs)
    ys_noisy = ys_true + rng.normal(0, noise_std, n)
    return xs, ys_noisy, ys_true


def linear_data(
    n: int = 12,
    slope: float = 0.6,
    intercept: float = 0.2,
    x_range: tuple[float, float] = (-3.5, 3.5),
    noise_std: float = 0.45,
    seed: int = 7,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (xs, ys) drawn from a noisy linear relationship."""
    rng = np.random.default_rng(seed)
    xs = rng.uniform(x_range[0], x_range[1], n)
    ys = slope * xs + intercept + rng.normal(0, noise_std, n)
    return xs, ys


def population_dots(
    n: int = 220,
    center: tuple[float, float] = (0.0, 0.0),
    spread: tuple[float, float] = (3.2, 2.0),
    seed: int = 3,
) -> np.ndarray:
    """Return (N, 2) array of population dot positions."""
    rng = np.random.default_rng(seed)
    xs = rng.normal(center[0], spread[0], n)
    ys = rng.normal(center[1], spread[1], n)
    return np.column_stack([xs, ys])


def gaussian_pdf(xs: np.ndarray, mu: float = 0.0, sigma: float = 1.0) -> np.ndarray:
    return np.exp(-0.5 * ((xs - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


def moving_average(xs: np.ndarray, ys: np.ndarray, n_eval: int = 80, bandwidth: float = 1.2) -> tuple[np.ndarray, np.ndarray]:
    """Kernel-smoothed moving average via Gaussian kernel."""
    x_eval = np.linspace(xs.min(), xs.max(), n_eval)
    y_smooth = np.empty(n_eval)
    for i, x0 in enumerate(x_eval):
        weights = gaussian_pdf(xs, mu=x0, sigma=bandwidth)
        y_smooth[i] = np.sum(weights * ys) / (np.sum(weights) + 1e-12)
    return x_eval, y_smooth


def overfit_poly_points(
    xs: np.ndarray,
    ys: np.ndarray,
    n_eval: int = 120,
) -> tuple[np.ndarray, np.ndarray]:
    """Interpolating polynomial (degree = n-1) — used to visualise overfitting."""
    degree = min(len(xs) - 1, 9)
    coeffs = np.polyfit(xs, ys, degree)
    poly   = np.poly1d(coeffs)
    x_eval = np.linspace(xs.min(), xs.max(), n_eval)
    y_eval = poly(x_eval)
    # Clamp extreme extrapolation for a cleaner visual
    y_eval = np.clip(y_eval, ys.min() - 1.5, ys.max() + 1.5)
    return x_eval, y_eval


def confidence_band(
    xs_eval: np.ndarray,
    slope: float,
    intercept: float,
    noise_std: float = 0.45,
    n_obs: int = 12,
) -> tuple[np.ndarray, np.ndarray]:
    """±1 SE confidence band around a fitted line."""
    y_fit  = slope * xs_eval + intercept
    x_bar  = 0.0
    sxx    = n_obs * xs_eval.var() + 1e-9
    se     = noise_std * np.sqrt(1 / n_obs + (xs_eval - x_bar) ** 2 / sxx)
    return y_fit - se, y_fit + se
