"""Project configuration for "Why 6 Is Perfect and 7 Is Mysterious"."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import config as manim_config

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from themes.oceanic_next import oceanic_bubbles as _repo_oceanic_bubbles
from themes.oceanic_next import apply_oceanic_next_theme as _repo_apply_oceanic_next_theme

FRAME_WIDTH = 14.222222
FRAME_HEIGHT = 8.0
FRAME_RATE = 30

FONT = "DejaVu Sans"
TITLE_FONT = "DejaVu Serif"

OCEANIC_BG = "#041A2F"
PANEL = "#081F35"
PANEL_STROKE = "#1E5570"
GRID = "#264F63"
MUTED = "#A7ADBA"
WHITE = "#F5FAFF"
CYAN = "#5FB3B3"
BLUE = "#6699CC"
GREEN = "#99C794"
GOLD = "#FAC863"
ORANGE = "#F99157"
RED = "#EC5F67"
PURPLE = "#C594C5"
GRAY = "#65737E"

TITLE_SIZE = 62
SUBTITLE_SIZE = 34
EQUATION_SIZE = 64
LABEL_SIZE = 32
SMALL_SIZE = 24

SAFE_WIDTH = 12.4
SAFE_HEIGHT = 6.6

SCENE_DURATIONS = {
    "01": "0:00-0:45",
    "02": "0:45-1:25",
    "03": "1:25-2:10",
    "04": "2:10-2:50",
    "05": "2:50-3:35",
    "06": "3:35-4:25",
    "07": "4:25-5:15",
    "08": "5:15-6:05",
    "09": "6:05-6:25",
}


def apply_oceanic_next_theme(scene=None) -> None:
    """Apply the shared Oceanic Next theme and project frame settings."""

    manim_config.frame_width = FRAME_WIDTH
    manim_config.frame_height = FRAME_HEIGHT
    manim_config.frame_rate = FRAME_RATE
    manim_config.background_color = OCEANIC_BG
    if scene is not None:
        _repo_apply_oceanic_next_theme(scene)
        scene.camera.background_color = OCEANIC_BG


def oceanic_bubbles():
    """Expose the repo bubble layer through local configuration."""

    return _repo_oceanic_bubbles()
