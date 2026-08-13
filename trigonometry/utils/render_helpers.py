"""Safe-frame helpers for mobile-readable compositions."""

from __future__ import annotations

from manim import Mobject

import config as cfg


def fit_to_safe_frame(mobject: Mobject, padding: float = 0.25) -> Mobject:
    max_width = cfg.SAFE_WIDTH - 2 * padding
    max_height = cfg.SAFE_HEIGHT - 2 * padding
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def is_inside_safe_frame(mobject: Mobject, tolerance: float = 0.05) -> bool:
    return mobject.width <= cfg.SAFE_WIDTH + tolerance and mobject.height <= cfg.SAFE_HEIGHT + tolerance
