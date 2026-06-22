"""Project-wide settings for the World Cup Magnus effect animation."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(1, str(REPO_ROOT))

from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles

apply_oceanic_next_theme()

PROJECT_TITLE = "Why the World Cup Ball Curves in Mid-Air"
PROJECT_SLUG = "worldcup-magnus-effect"

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.7

COLORS = {
    "background": "#08111A",
    "background_2": "#0D1B2A",
    "panel": "#102235",
    "line": "#1F3443",
    "line_soft": "#2C4558",
    "cyan": "#5FB3B3",
    "blue": "#6699CC",
    "green": "#99C794",
    "orange": "#F99157",
    "red": "#EC5F67",
    "purple": "#C594C5",
    "white": "#D8DEE9",
    "muted": "#65737E",
    "gold": "#FAC863",
    "grass": "#123C35",
    "grass_2": "#0E2C2A",
}

CYAN = COLORS["cyan"]
BLUE = COLORS["blue"]
GREEN = COLORS["green"]
ORANGE = COLORS["orange"]
RED = COLORS["red"]
PURPLE = COLORS["purple"]
WHITE = COLORS["white"]
MUTED = COLORS["muted"]
GOLD = COLORS["gold"]
BG = COLORS["background"]

FONT_SIZES = {
    "title": 52,
    "subtitle": 30,
    "equation": 50,
    "label": 25,
    "small": 28,
    "tiny": 16,
}

TIMING = {
    "pace_scale": 1.18,
    "quick": 0.35,
    "normal": 0.75,
    "slow": 1.25,
    "hold": 0.7,
    "scene_hold": 1.0,
}

SCENE_DURATIONS = {
    "01": 45.0,
    "02": 45.0,
    "03": 50.0,
    "04": 50.0,
    "05": 55.0,
    "06": 50.0,
    "07": 55.0,
    "08": 60.0,
    "09": 10.0,
}

VISUAL = {
    "glow_opacity": 0.18,
    "glow_layers": 4,
    "stroke_width": 5,
    "arrow_stroke": 7,
    "ball_radius": 0.32,
}

RENDER = {
    "preview_quality": "l",
    "youtube_quality": "qh",
    "fps": 30,
    "resolution": "1920,1080",
}

REFERENCE_IMAGE = PROJECT_ROOT / "image" / "FIFA-World-Cup-all-official-match-balls-from-1930-to-2026-graphic-16x9.avif"
TRIONDA_IMAGE = PROJECT_ROOT / "image" / "Trionda.png"
REFERENCE_IMAGE_CANDIDATES = [
    PROJECT_ROOT / "image" / "Worldcup_ball.png",
    REFERENCE_IMAGE,
]
