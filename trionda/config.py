"""Project-wide configuration for the Trionda Manim animation."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import config

PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TRIONDA_IMAGE = PROJECT_DIR / "image" / "Trionda.png"

from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles  # noqa: E402

VIDEO_TITLE = "The Secret Material Inside the 2026 World Cup Ball"

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
PIXEL_WIDTH = 1920
PIXEL_HEIGHT = 1080
FRAME_RATE = 30

BG = "#061018"
PANEL = "#0B2030"
GRID = "#21384B"
MUTED = "#8FA7B5"
WHITE = "#F5FBFF"
CYAN = "#7FDBFF"
BLUE = "#4AA3FF"
GREEN = "#74F29A"
RED = "#FF5C6A"
ORANGE = "#FFB057"
PURPLE = "#B88CFF"
GOLD = "#FFD166"
GRAY = "#607080"
BLACKISH = "#031018"

COLORS = {
    "normal": CYAN,
    "stable": BLUE,
    "main": WHITE,
    "valid": GREEN,
    "warning": ORANGE,
    "error": RED,
    "abstract": PURPLE,
    "muted": MUTED,
    "grid": GRID,
    "panel": PANEL,
    "gold": GOLD,
}

FONT_SIZES = {
    "title": 58,
    "subtitle": 34,
    "caption": 40,
    "label": 28,
    "small": 22,
    "equation": 58,
}

TIMING = {
    "pace_scale": 1.0,
}

SCENE_DURATIONS = {
    "01": 42,
    "02": 44,
    "03": 45,
    "04": 45,
    "05": 54,
    "06": 48,
    "07": 45,
    "08": 45,
    "09": 12,
}

REFERENCES = [
    "FIFA launch release: https://inside.fifa.com/organisation/media-releases/fifa-celebrates-launch-official-match-ball-world-cup-26-trionda",
    "adidas technology release: https://news.adidas.com/innovations/adidas-unveils--trionda----the-official-match-ball-of-the-fifa-world-cup26-/s/27042e3a-12ba-482d-8839-8a96e056b33e",
    "FIFA connected ball technology: https://inside.fifa.com/innovation/innovating-the-game/connected-ball-technology",
    "Goff et al. 2026: https://www.mdpi.com/2076-3417/16/6/2808",
    "Scientific American: https://www.scientificamerican.com/article/the-surprising-math-and-physics-behind-the-2026-trionda-world-cup-soccer-ball/",
]


def apply_manim_config() -> None:
    """Set deterministic 16:9 render defaults."""

    config.background_color = BG
    config.frame_width = FRAME_WIDTH
    config.frame_height = FRAME_HEIGHT
    config.pixel_width = PIXEL_WIDTH
    config.pixel_height = PIXEL_HEIGHT
    config.frame_rate = FRAME_RATE


apply_manim_config()
