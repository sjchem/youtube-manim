"""Statistical and conceptual models used across scenes."""

from __future__ import annotations

import numpy as np


def bias_variance_shots(
    scenario: str,
    n: int = 9,
    seed: int = 21,
) -> np.ndarray:
    """Return (n, 2) dart positions for bias-variance dartboard scenarios.

    scenario:
        'high_bias'     – tight cluster offset from centre
        'high_variance' – spread randomly around centre
        'both_bad'      – spread AND offset
        'ideal'         – tight cluster near centre
    """
    rng = np.random.default_rng(seed)
    if scenario == "high_bias":
        pts = rng.normal(loc=[1.2, -1.0], scale=[0.18, 0.15], size=(n, 2))
    elif scenario == "high_variance":
        pts = rng.normal(loc=[0.0, 0.0], scale=[1.1, 1.1], size=(n, 2))
    elif scenario == "both_bad":
        pts = rng.normal(loc=[1.1, 0.9], scale=[0.85, 0.85], size=(n, 2))
    else:  # ideal
        pts = rng.normal(loc=[0.0, 0.0], scale=[0.22, 0.20], size=(n, 2))
    return pts


def pipeline_stages() -> list[dict]:
    """Ordered stages for the 'statistics as thinking layer' pipeline."""
    return [
        {"label": "Raw Data",       "icon": "dots",    "color": "#65737E"},
        {"label": "Statistics",     "icon": "sigma",   "color": "#5FB3B3"},
        {"label": "Model",          "icon": "network", "color": "#6699CC"},
        {"label": "Prediction",     "icon": "arrow",   "color": "#99C794"},
    ]


def stat_tools() -> list[dict]:
    """Key statistics concepts shown in the synthesis scene."""
    return [
        {"text": "Uncertainty",  "color": "#C594C5"},
        {"text": "Signal",       "color": "#5FB3B3"},
        {"text": "Estimation",   "color": "#FAC863"},
        {"text": "Generalize",   "color": "#6699CC"},
        {"text": "Evaluation",   "color": "#99C794"},
        {"text": "Inference",    "color": "#F99157"},
    ]


def course_parts() -> list[dict]:
    """Series structure for the opening roadmap."""
    return [
        {"part": "Part 1", "title": "Foundations",          "chapters": "Ch 1–7",   "color": "#5FB3B3"},
        {"part": "Part 2", "title": "Inference & Learning", "chapters": "Ch 8–15",  "color": "#99C794"},
        {"part": "Part 3", "title": "Evaluation",           "chapters": "Ch 16–20", "color": "#C594C5"},
        {"part": "Part 4", "title": "Advanced ML",          "chapters": "Ch 21–28", "color": "#FAC863"},
    ]
