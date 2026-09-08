"""Project-wide settings for 'What Does a Function Actually Do?'."""

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

PROJECT_TITLE = "What Does a Function Actually Do?"
PROJECT_PART = "Foundations"
PROJECT_SLUG = "what-does-a-function-actually-do"
SERIES_LABEL = "Visualized Mathematics"
VIDEO_SUBTITLE = "Input, rule, output — the idea underneath all of it."

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# A true 16-by-9 logical canvas, not only a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette. A color always carries the same meaning across the film.
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

# Semantic roles, so every scene colors the same idea the same way.
INPUT_COLOR = GOLD        # whatever enters a machine
RULE_COLOR = CYAN         # the machine / the rule itself
OUTPUT_COLOR = GREEN      # whatever leaves a machine
BROKEN_COLOR = RED        # ambiguity, contradiction, "not a function"
ABSTRACT_COLOR = PURPLE   # abstraction, higher dimensions, the big picture

FONT: dict[str, int] = {
    "hero": 76,
    "title": 60,
    "section": 50,
    "body": 42,
    "label": 38,
    "small": 34,
    # 30 is the minimum authored size for anything a viewer must actually read.
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

# Programme target: 1174 seconds = 19:34, including the end card.
# Voice timing still needs checking against the generated audio. Verify with:
#   python -m utils.timing_audit
SCENE_DURATIONS: dict[str, float] = {
    "01": 66.0,
    "02": 95.0,
    "03": 88.0,
    "04": 82.0,
    "05": 105.0,
    "06": 65.0,
    "07": 125.0,
    "08": 105.0,
    "09": 115.0,
    "10": 80.0,
    "11": 95.0,
    "12": 88.0,
    "13": 50.0,
    "14": 15.0,
}

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "2560,1440",
}

SEED = 20260906


def apply_project_theme(scene, bubbles: bool = True) -> None:
    """Apply the local Oceanic Next theme and optional subtle bubbles."""
    apply_oceanic_next_theme(scene)
    scene.camera.background_color = BG
    if bubbles:
        scene.add(oceanic_bubbles())
