"""Project-wide visual and render settings for Chapter 4."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PROJECT_TITLE = "Probability Basics Every ML Learner Must Know"
PROJECT_SUBTITLE = "Statistics for ML - Part 1, Chapter 4"
SAFE_FRAME_WIDTH = 13.4
SAFE_FRAME_HEIGHT = 7.2

COLORS = {
    "background": "#041A2F",
    "background_2": "#07243B",
    "panel": "#0B2A3E",
    "panel_alt": "#10384F",
    "line": "#36576B",
    "text": "#F4FAFF",
    "muted": "#A7BCCB",
    "blue": "#42C6FF",
    "cyan": "#8ED4FF",
    "green": "#78D98B",
    "gold": "#FFD166",
    "red": "#FF6B6B",
    "orange": "#FF9F43",
    "purple": "#B69CFF",
    "gray": "#78909C",
}

FONT_SIZES = {
    "title": 46,
    "subtitle": 30,
    "equation": 48,
    "label": 28,
    "small": 22,
    "tiny": 17,
}

TIMING = {
    "pace_scale": 1.28,
    "quick": 0.4,
    "normal": 0.8,
    "slow": 1.2,
    "pause": 0.55,
}

SCENE_DURATIONS = {
    "01": 68,
    "02": 74,
    "03": 76,
    "04": 80,
    "05": 70,
    "06": 76,
    "07": 82,
    "08": 78,
    "09": 70,
    "10": 28,
}

RENDER = {
    "preview_quality": "l",
    "youtube_quality": "qh",
    "fps": 30,
    "resolution": "1920,1080",
}

BG = COLORS["background"]
TEXT = COLORS["text"]
WHITE = TEXT
MUTED = COLORS["muted"]
BLUE = COLORS["blue"]
CYAN = COLORS["cyan"]
GREEN = COLORS["green"]
GOLD = COLORS["gold"]
YELLOW = GOLD
RED = COLORS["red"]
ORANGE = COLORS["orange"]
PURPLE = COLORS["purple"]
GRAY = COLORS["gray"]


def apply_project_theme(scene: Scene) -> None:
    """Apply the local Oceanic Next theme, falling back cleanly if unavailable."""
    try:
        from themes.oceanic_next import apply_oceanic_next_theme

        apply_oceanic_next_theme(scene)
    except Exception:
        scene.camera.background_color = BG
