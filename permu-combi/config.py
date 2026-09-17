"""Project-wide settings for 'Permutations & Combinations Explained Visually'."""

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

PROJECT_TITLE = "Permutations & Combinations Explained Visually"
PROJECT_PART = "Counting Without Listing"
PROJECT_SLUG = "permutations-and-combinations-explained-visually"
SERIES_LABEL = "Visualized Mathematics"
VIDEO_SUBTITLE = "When does changing the order create a new outcome?"

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# A true 16-by-9 logical canvas, not only a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette. A colour always carries the same meaning across the film.
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

# Semantic roles. The whole film teaches through this one visual grammar:
#   available -> chosen -> spent, and ranked slots versus one enclosing ring.
AVAILABLE = CYAN        # an object still in the pool, free to be picked
CHOSEN = GOLD           # an object in flight, or already placed in a slot
SPENT = GRAY            # an object that has been used and dimmed out
ORDERED = ORANGE        # ranked positions: order matters -> permutation
UNORDERED = GREEN       # one enclosing ring: order does not matter -> combination
RESULT = WHITE          # the central equation or headline number
ABSTRACT = PURPLE       # scale, huge counts, the step into abstraction
WRONG = RED             # overcounting, a locked padlock, a contradiction

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

# Programme target: 1605 seconds = 26:45, including the end card.
# Verify pacing without rendering frames:  python -m utils.timing_audit
SCENE_DURATIONS: dict[str, float] = {
    "01": 92.0,
    "02": 177.0,
    "03": 140.0,
    "04": 160.0,
    "05": 88.0,
    "06": 180.0,
    "07": 195.0,
    "08": 90.0,
    "09": 180.0,
    "10": 88.0,
    "11": 82.0,
    "12": 46.0,
    "13": 72.0,
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

SEED = 20260915


def apply_project_theme(scene, bubbles: bool = True) -> None:
    """Apply the local Oceanic Next theme and optional subtle bubbles."""
    apply_oceanic_next_theme(scene)
    scene.camera.background_color = BG
    if bubbles:
        scene.add(oceanic_bubbles())
