"""Shared visual language for the zero-power explainer."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import config as manim_config

# Reuse the repository-level theme helper from ../themes.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from themes import apply_oceanic_next_theme as _apply_repo_oceanic_next_theme

# Oceanic Next palette values used for custom mobjects in this project.
BACKGROUND_COLOR = "#061018"
PANEL_COLOR = "#182330"
PANEL_STROKE = "#2B3A4A"
TEXT_COLOR = "#D8DEE9"
MUTED_TEXT = "#A7ADBA"
WORD_COLOR = "#A9D6E5"
QUESTION_COLOR = "#FFD166"
ACCENT_CYAN = "#5FB3B3"
ACCENT_BLUE = "#6699CC"
ACCENT_TEAL = "#99C794"
ACCENT_YELLOW = "#FAC863"
ACCENT_ORANGE = "#F99157"
ACCENT_RED = "#EC5F67"
ACCENT_PURPLE = "#C594C5"

FRAME_WIDTH = 14.222222
FRAME_HEIGHT = 8.0

FONT = "DejaVu Sans"
WORD_FONT = "DejaVu Serif"
TITLE_FONT_SIZE = 58
EQUATION_FONT_SIZE = 64
LABEL_FONT_SIZE = 30
SMALL_FONT_SIZE = 24

SCENE_DURATIONS = {
    "scene_01_hook": "35-45 seconds",
    "scene_02_power_ladder": "about 60 seconds",
    "scene_03_exponent_law": "about 55 seconds",
    "scene_04_empty_product": "about 45 seconds",
    "scene_05_graph_view": "about 45 seconds",
    "scene_06_final_summary": "about 40 seconds",
}

OCEANIC_NEXT = {
    "background": BACKGROUND_COLOR,
    "panel": PANEL_COLOR,
    "panel_stroke": PANEL_STROKE,
    "text": TEXT_COLOR,
    "muted": MUTED_TEXT,
    "word": WORD_COLOR,
    "question": QUESTION_COLOR,
    "cyan": ACCENT_CYAN,
    "blue": ACCENT_BLUE,
    "teal": ACCENT_TEAL,
    "yellow": ACCENT_YELLOW,
    "orange": ACCENT_ORANGE,
    "red": ACCENT_RED,
    "purple": ACCENT_PURPLE,
}


def apply_oceanic_next_theme(scene=None) -> dict[str, str]:
    """Apply the repo Oceanic Next theme and return this project's palette."""

    manim_config.frame_width = FRAME_WIDTH
    manim_config.frame_height = FRAME_HEIGHT
    manim_config.frame_rate = 30

    if scene is not None:
        _apply_repo_oceanic_next_theme(scene)
    else:
        manim_config.background_color = BACKGROUND_COLOR

    return OCEANIC_NEXT.copy()
