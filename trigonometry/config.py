"""Project-wide settings for the complete visual trigonometry course."""

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

PROJECT_TITLE = "Visual Trigonometry — From Triangles to Euler's Formula"
PROJECT_SLUG = "visualized-trigonometry"
SERIES_LABEL = "Visualized Mathematics"
VIDEO_SUBTITLE = "Trigonometry without memorizing"

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
    "body": 40,
    "label": 34,
    "small": 28,
    "tiny": 23,
}

TIMING: dict[str, float] = {
    "pace_scale": 1.0,
    "quick": 0.45,
    "normal": 0.85,
    "slow": 1.4,
    "hold": 1.0,
    "transition": 0.55,
}

# Expanded course total: 2715 seconds = 45:15.
SCENE_DURATIONS: dict[str, float] = {
    "01": 95.0,
    "02": 90.0,
    "03": 180.0,
    "04": 140.0,
    "05": 180.0,
    "06": 240.0,
    "07": 125.0,
    "08": 165.0,
    "09": 115.0,
    "10": 210.0,
    "11": 300.0,
    "12": 240.0,
    "13": 110.0,
    "14": 270.0,
    "15": 180.0,
    "16": 60.0,
    "17": 15.0,
}

# Authored animation time before narration synchronization. These calibrated
# values include per-scene frame-quantization allowances for both the 15 FPS
# preview and 30 FPS master. Changing SCENE_DURATIONS still redistributes motion
# instead of creating a static hold at the end.
AUTHORED_DURATIONS: dict[str, float] = {
    "01": 50.15,
    "02": 42.05,
    "03": 34.22,
    "04": 48.87,
    "05": 31.37,
    "06": 38.30,
    "07": 48.01,
    "08": 95.53,
    "09": 87.31,
    "10": 29.01,
    "11": 43.55,
    "12": 37.50,
    "13": 55.26,
    "14": 59.04,
    "15": 42.70,
    "16": 21.06,
    "17": 3.45,
}

SCENE_PACE: dict[str, float] = {
    key: (duration - TIMING["transition"]) / AUTHORED_DURATIONS[key]
    for key, duration in SCENE_DURATIONS.items()
}

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "resolution": "1920,1080",
}

SEED = 20260802


def apply_project_theme(scene, bubbles: bool = True) -> None:
    """Apply the local Oceanic Next theme and optional subtle bubbles."""
    apply_oceanic_next_theme(scene)
    scene.camera.background_color = BG
    if bubbles:
        scene.add(oceanic_bubbles())
