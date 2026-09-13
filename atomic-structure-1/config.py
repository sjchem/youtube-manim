"""Project-wide settings for *How We Discovered What an Atom Looks Like* (Part 1).

Everything a chapter needs to agree with every other chapter lives here: the
logical frame, the Oceanic palette with its fixed meanings, the type scale, the
narration windows, and which chapters open the 3D camera.
"""

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

PROJECT_TITLE = "How We Discovered What an Atom Looks Like"
PROJECT_PART = "Part 1"
PROJECT_SLUG = "how-we-discovered-what-an-atom-looks-like-part1"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "Evidence revealed the structure before images did."

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# A true 16-by-9 logical canvas, not merely a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette. A colour always carries the same meaning across the film.
#   cyan / blue  -> the normal, stable, currently trusted state
#   white        -> the central object or the main equation
#   green        -> a confirmed result, a model that survives
#   red / orange -> a contradiction, a failure, a warning
#   purple       -> abstraction, quantum strangeness, the extreme case
#   gold         -> the narrator's own emphasis: headings and captions
#   muted / gray -> scaffolding and secondary structure
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

# Recurring physical objects keep one colour for the whole film, so the eye
# never has to re-learn what it is looking at.
NUCLEUS_COLOR = RED
PROTON_COLOR = ORANGE
ELECTRON_COLOR = CYAN
ALPHA_COLOR = GOLD
POSITIVE_CLOUD = ORANGE
PHOTON_COLOR = PURPLE

FONT: dict[str, int] = {
    "hero": 76,
    "title": 60,
    "section": 50,
    "body": 42,
    "label": 38,
    "small": 34,
    # 30 is the smallest authored size for anything a viewer must actually read.
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

# Planning windows: 22:05, including a separate 15-second subscribe card.
# Replace these with measured delivery windows when the cloned voice is ready.
SCENE_DURATIONS: dict[str, float] = {
    "01": 65.0,
    "02": 70.0,
    "03": 75.0,
    "04": 120.0,
    "05": 120.0,
    "06": 125.0,
    "07": 115.0,
    "08": 80.0,
    "09": 125.0,
    "10": 95.0,
    "11": 95.0,
    "12": 85.0,
    "13": 80.0,
    "14": 60.0,
    "15": 15.0,
}

THREE_D_SCENES: frozenset[str] = frozenset({"01", "03", "04", "05", "06", "14"})

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "resolution": "1920,1080",
}

SEED = 20260910


def apply_project_theme(scene, bubbles: bool = True) -> None:
    """Apply the local Oceanic Next theme and optional subtle bubbles."""
    apply_oceanic_next_theme(scene)
    scene.camera.background_color = BG
    if bubbles:
        scene.add(oceanic_bubbles())
