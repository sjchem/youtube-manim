"""Project-wide settings for Visual Calculus Part 2: From Derivatives to Integrals."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import config as manim_config

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent

for _path in (str(PROJECT_ROOT), str(REPO_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles  # noqa: E402

PROJECT_TITLE = "Visual Calculus: From Derivatives to Integrals"
PROJECT_PART = "Part 2"
PROJECT_SLUG = "visual-calculus-derivatives-integrals-part2"
SERIES_LABEL = "Visualized Mathematics"
VIDEO_SUBTITLE = "Two sides of the same idea."

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# Use a true 16-by-9 logical canvas, not only a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette. A color always carries the same meaning throughout the film.
BG = "#041A2F"
PANEL = "#0A2540"
PANEL_2 = "#0D2B4A"
WHITE = "#F4FAFF"
MUTED = "#A7BCCB"
CYAN = "#8ED4FF"
BLUE = "#42C6FF"
GREEN = "#78D98B"
GOLD = "#FFD166"
ORANGE = "#FF9F43"
RED = "#FF6B6B"
PURPLE = "#B69CFF"
GRAY = "#78909C"

FONT: dict[str, int] = {
    "hero": 76,
    "title": 60,
    "section": 50,
    "body": 42,
    "label": 38,
    "small": 34,
    # 30 is the minimum authored size for information students must read.
    # At 1080p this stays legible on a phone without crowding the frame.
    "tiny": 30,
}

TIMING: dict[str, float] = {
    "quick": 0.45,
    "normal": 0.85,
    "slow": 1.4,
    "hold": 1.0,
    "transition": 0.55,
}

# Part 2 total: 1054 seconds = 17:34. Calibrated against narration_script.md
# at ~105 words per minute; verify with `python utils/timing_audit.py`.
SCENE_DURATIONS: dict[str, float] = {
    "01": 89.0,
    "02": 84.0,
    "03": 56.0,
    "04": 112.0,
    "05": 65.0,
    "06": 71.0,
    "07": 56.0,
    "08": 96.0,
    "09": 74.0,
    "10": 70.0,
    "11": 75.0,
    "12": 61.0,
    "13": 130.0,
    "14": 15.0,
}

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "resolution": "1920,1080",
}

SEED = 20260831


def apply_project_theme(scene, bubbles: bool = True) -> None:
    """Apply the local Oceanic Next theme and optional subtle bubbles."""
    apply_oceanic_next_theme(scene)
    scene.camera.background_color = BG
    if bubbles:
        scene.add(oceanic_bubbles())
